from django.db import models
from django.utils.dateformat import DateFormat
from django.utils.formats import date_format
import datetime
from django.http import Http404
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.fields import StreamField, RichTextField
from django.utils.functional import cached_property
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel
from wagtailmetadata.models import MetadataPageMixin


from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel
from wagtail.snippets.models import register_snippet
from taggit.models import Tag as TaggitTag
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail.admin.panels import FieldPanel, InlinePanel
from modelcluster.tags import ClusterTaggableManager
from wagtail.fields import StreamField
from wagtail.contrib.forms.panels import FormSubmissionsPanel
from .blocks import BodyBlock
from wagtail.search import index
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page
from wagtail_newsletter.models import NewsletterPageMixin
# Create your models here.


class FormField(AbstractFormField):
    page = ParentalKey('FormPage', on_delete=models.CASCADE, related_name='form_fields')

class FormPage(AbstractEmailForm):
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro'),
        InlinePanel("form_fields", label="Form fields"),
        FieldPanel("thank_you_text"),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("from_address", classname="col6"),
                        FieldPanel("to_address", classname="col6"),
                    ]
                ),
                FieldPanel("subject"),
            ],
            "Email",
        ),
    ]

class BlogPage(RoutablePageMixin, Page):

    def get_sitemap_urls(self, request=None):
        output = []
        posts = self.get_posts
        for post in posts:
            post_date = post.post_date
            url =self.get_full_url(request) + self.reverse_subpage(
                'post_by_date_slug',
                args=(
                    post_date.year,
                    '{0:02}'.format(post_date.month),
                    '{0:02}'.format(post_date.day),
                    post.slug,
                    )
                )

            output.append({
                'location': url,
                'lastmod': post.last_published_at
            })

        return output 
    
    

    def get_context(self, request, *args, **kwargs):
        context = super(BlogPage, self).get_context(request, *args, **kwargs)
        context['blog_page'] = self
        context['posts'] = self.posts
        return context

    def get_posts(self):
            return PostPage.objects.descendant_of(self).live().order_by("-post_date")

    @route(r"^(\d{4})/$")
    @route(r"^(\d{4})/(\d{2})/$")
    @route(r"^(\d{4})/(\d{2})/(\d{2})/$")
    def post_by_date(self, request, year, month=None, day=None, *args, **kwargs):
        self.filter_type = 'date'
        self.filter_term = year
        self.posts = self.get_posts().filter(post_date__year=year)
        if month:
            df = DateFormat(datetime.date(int(year), int(month), 1))
            self.filter_term = df.format('F Y')
            self.posts = self.posts.filter(post_date__month=month)
        if day:
            self.filter_term = date_format(datetime.date(int(year), int(month), int(day)))
            self.posts = self.posts.filter(post_date__day=day)
        return self.render(request) 

    @route(r"^search/$")
    def post_search(self, request, *args, **kwargs):
        search_query = request.GET.get("q", None)
        self.posts = self.get_posts()
        if search_query:
            self.filter_term = search_query
            self.filter_type = 'search'
            self.posts = self.posts.search(search_query)
        return self.render(request)  

    @route(r"^(\d{4})/(\d{2})/(\d{2})/(.+)/$") 
    def post_by_date_slug(self, request, year, month, day, slug, *args, **kwargs):
        post_page = self.get_posts().filter(slug=slug).first()
        if not post_page:
            raise Http404
        return post_page.serve(request)

    def get_paginated_posts(self,request, qs):
        paginator = Paginator(qs,2)
        page = request.GET.get("page")
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.object_list.none()

        return posts

    @route(r'^tag/(?P<tag>[-\w]+)/$')
    def post_by_tag(self, request, tag, *args, **kwargs):
        self.filter_type= 'tag'
        self.filter_term = tag
        self.posts = self.get_posts().filter(tags__slug=tag)
        return self.render(request)

    @route(r'^category/(?P<category>[-\w]+)/$')
    def post_by_category(self, request, category, *args, **kwargs):
        self.filter_type = 'category'
        self.filter_term = category
        self.posts = self.get_posts().filter(categories__blog_category__slug=category)
        return self.render(request)

    @route(r'^$')
    def post_list(self, request, *args, **kwargs):
        self.posts = self.get_posts()
        return self.render(request)

class PostPage(MetadataPageMixin, Page):

    def get_sitemap_urls(self, request=None):
        return []

    search_fields = Page.search_fields + [
        index.SearchField('title'),
        index.SearchField('body'),
    ]
    header_image=models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['blog_page'] = self.blog_page
        return context

    @cached_property
    def blog_page(self):
        return self.get_parent().specific

    @cached_property
    def canonical_url(self):
        from blog.templatetags.blogapp_tags import post_page_date_slug_url

        blog_page =self.blog_page
        return post_page_date_slug_url(self, blog_page)

    tags = ClusterTaggableManager(through="blog.PostPageTag", blank=True)
    body = StreamField(BodyBlock(), blank=True, use_json_field=True)
    content_panels = Page.content_panels + [
        FieldPanel("header_image"),
        InlinePanel("categories", label="category"),
        FieldPanel("tags"),
        FieldPanel("body"),
    
    ]

    post_date = models.DateTimeField(
        verbose_name="Post date", default=datetime.datetime.today
    )

    settings_panels = Page.settings_panels + [
        FieldPanel("post_date"),
    ]
    
    def canonical_url(self):
        from anansi_app.blog.templatetags.blogapp_tags import post_page_date_slug_url

        blog_page = self.get_parent().specific
        return post_page_date_slug_url(self, blog_page)

    @route(r"^search/$")
    def post_search(self, request, *args, **kwargs):
        search_query = request.GET.get("q", None)
        self.posts =self.get_posts()
        if search_query:
            self.posts = self.posts.search(search_query)
        return self.render(request)

@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=80)

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

@register_snippet
class Tag(TaggitTag):
    class Meta:
        proxy = True

class PostPageBlogCategory(models.Model):
    page= ParentalKey(
        "blog.PostPage", on_delete=models.CASCADE, related_name="categories"
    )
    blog_category = models.ForeignKey(
        "blog.BlogCategory", on_delete=models.CASCADE, related_name="post_pages"
    )
    panels = [
        FieldPanel("blog_category"),
    ]

    class Meta:
        unique_together = ("page", "blog_category")

class PostPageTag(TaggedItemBase):
    content_object = ParentalKey("PostPage", related_name="post_tags")

class ArticlePage(NewsletterPageMixin, Page):
    body = RichTextField()
    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]
    newsletter_template = "blog/article_page_newsletter.html"


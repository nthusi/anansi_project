from wagtail.models import Site
from anansi_app.blog.models import BlogPage

def blog_page(request):
    Anansi = Site.find_for_request(request)
    context = {
        'blog_page': BlogPage.objects.in_site(Anansi).first()
    }
    return context 
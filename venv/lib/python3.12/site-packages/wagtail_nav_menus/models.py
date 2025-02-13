import json
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.urls import NoReverseMatch
from django.utils.translation import gettext_lazy as _
from wagtail.fields import StreamField
from wagtail import blocks
from wagtail.models import Site
from wagtail.admin.panels import FieldPanel
from .loading import get_class
from .utils import date_handler
from .defaults import (
    WAGTAIL_NAV_MENU_TYPES_DEFAULT,
    WAGTAIL_NAV_MENU_CHOICES_DEFAULT,
)


NAV_MENU_CHOICES = getattr(
    settings, "WAGTAIL_NAV_MENU_CHOICES", WAGTAIL_NAV_MENU_CHOICES_DEFAULT
)


class AbstractPageBlock(blocks.StructBlock):
    override_title = blocks.CharBlock(required=False)
    open_in_new_tab = blocks.BooleanBlock(required=False)

    class Meta:
        icon = "link"
        template = "nav_menus/menu_link.html"


class InternalPageBlock(AbstractPageBlock):
    page = blocks.PageChooserBlock()

    class Meta:
        # Translators: Navigation Menu Item Type
        verbose_name = _("Internal Page Block")

    def get_serializable_data(self, obj):
        page = obj["page"]
        result = obj
        result["page"] = page.serializable_data()
        result["page"]["url"] = page.url
        return result


class ExternalPageBlock(AbstractPageBlock):
    link = blocks.URLBlock()

    class Meta:
        # Translators: Navigation Menu Item Type
        verbose_name = _("External Page Block")


class DjangoURLBlock(AbstractPageBlock):
    """A link that is generated from a Django reverse URL lookup"""

    url_name = blocks.CharBlock()

    class Meta:
        # Translators: Navigation Menu Item Type
        verbose_name = _("Django URL Block")

    def get_serializable_data(self, obj):
        url_name = obj["url_name"]
        result = obj
        try:
            result["url"] = reverse(url_name)
        except NoReverseMatch:
            result["url"] = "Not Found"
        return result


URL_REGEX = r"^(?!www\.|(?:http|ftp)s?://|[A-Za-z]:\\|//).*"


class RelativeURLBlock(AbstractPageBlock):
    link = blocks.RegexBlock(
        regex=URL_REGEX, error_mesage={"invalid": "Not a relative URL"}
    )

    class Meta:
        # Translators: Navigation Menu Item Type
        verbose_name = _("Relative URL Block")


NAV_MENU_TYPES = getattr(
    settings, "WAGTAIL_NAV_MENU_TYPES", WAGTAIL_NAV_MENU_TYPES_DEFAULT
)

nav_content = []
for name, module_label, class_name in NAV_MENU_TYPES:
    nav_content.append(
        (name, get_class(module_label, class_name)()),
    )


NAV_CATEGORY_TYPES = getattr(settings, "WAGTAIL_NAV_MENU_CATEGORY_TYPES", [])
custom_category_content = []
for name, module_label, class_name in NAV_CATEGORY_TYPES:
    custom_category_content.append(
        (name, get_class(module_label, class_name)()),
    )


class NavCategoryBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    sub_nav = blocks.StreamBlock(nav_content + custom_category_content)

    class Meta:
        icon = "list-ul"
        template = "nav_menus/nav_category.html"
        # Translators: Content Block Name
        verbose_name = _("Navigation Menu Category Block")


def site_default():
    return Site.objects.filter(is_default_site=True).first()


def site_default_id():
    """Not sure why this is needed for migrations, there is probably a better way."""
    site = site_default()
    if site:
        return site.id


class AbstractNavMenu(models.Model):
    site = models.ForeignKey(
        "wagtailcore.Site",
        db_index=True,
        on_delete=models.CASCADE,
        default=site_default_id,
    )
    name = models.CharField(
        max_length=50,
        choices=NAV_MENU_CHOICES,
    )
    menu = StreamField(
        [
            ("nav_category", NavCategoryBlock()),
        ]
        + nav_content,
        use_json_field=True,
    )

    panels = [
        FieldPanel("site"),
        FieldPanel("name"),
        FieldPanel("menu"),
    ]

    class Meta:
        # Translators: Model Name (singular)
        verbose_name = _("Navigation Menu")
        # Translators: Model Name (plural)
        verbose_name_plural = _("Navigation Menus")
        unique_together = (
            "site",
            "name",
        )
        abstract = True
        app_label = "wagtail_nav_menus"

    def __str__(self):
        return self.name

    def stream_field_to_json(self, stream_field):
        """Recursive function to turn the menu stream field into json"""
        row = {}
        row["type"] = stream_field.block_type
        if hasattr(stream_field.block, "get_serializable_data"):
            row["value"] = stream_field.block.get_serializable_data(stream_field.value)
        else:
            row["value"] = stream_field.value
        if row["type"] == "image" and row["value"]:
            image = row["value"]
            row["value"] = {
                "id": image.pk,
                "title": image.title,
                "url": image.file.url,
            }
        elif row["type"] == "nav_category":
            sub_nav = []
            for sub_stream_field in stream_field.value["sub_nav"]:
                sub_nav.append(self.stream_field_to_json(sub_stream_field))
            row["value"]["sub_nav"] = sub_nav
        return row

    def to_json(self):
        """JSON representation of menu stream field"""
        result = []
        for stream_field in self.menu:
            result.append(self.stream_field_to_json(stream_field))
        return json.dumps(result, default=date_handler)


class NavMenu(AbstractNavMenu):
    pass

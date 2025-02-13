WAGTAIL_NAV_MENU_TYPES_DEFAULT = [
    ("page_link", "wagtail_nav_menus.models", "InternalPageBlock"),
    ("external_link", "wagtail_nav_menus.models", "ExternalPageBlock"),
    ("django_url", "wagtail_nav_menus.models", "DjangoURLBlock"),
    ("relative_url", "wagtail_nav_menus.models", "RelativeURLBlock"),
    ("image", "wagtail.images.blocks", "ImageChooserBlock"),
    ("html", "wagtail.blocks", "RawHTMLBlock"),
]

WAGTAIL_NAV_MENU_CHOICES_DEFAULT = [
    ("top", "Top"),
    ("footer", "Footer"),
]

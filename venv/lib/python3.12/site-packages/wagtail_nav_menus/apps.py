from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class Config(AppConfig):
    name = "wagtail_nav_menus"
    # Translators: Backend Library Name
    verbose_name = _("Wagtail Navigation Menus")

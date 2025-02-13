from django.utils.translation import gettext_lazy as _
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register
from .models import NavMenu


class NavMenuAdmin(ModelAdmin):
    model = NavMenu
    menu_label = _("Nav Menu")
    menu_icon = "link"
    menu_order = 5000  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = True  # or True to add your model to the Settings sub-menu
    list_display = ("name", "site")


modeladmin_register(NavMenuAdmin)

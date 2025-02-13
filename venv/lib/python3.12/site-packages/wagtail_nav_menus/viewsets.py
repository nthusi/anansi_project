from rest_framework import viewsets
from wagtail.models import Site
from wagtail_nav_menus.models import NavMenu
from wagtail_nav_menus.serializers import NavMenuSerializer


class NavMenuViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = NavMenu.objects.all()
    serializer_class = NavMenuSerializer

    def get_queryset(self):
        site_hostname = self.request.GET.get("site", None)
        site = Site.find_for_request(self.request)
        if site_hostname:
            try:
                site = Site.objects.get(hostname=site_hostname)
            except Site.DoesNotExist:
                pass
        qs = super().get_queryset()
        if site:
            qs = qs.filter(site=site)
        return qs

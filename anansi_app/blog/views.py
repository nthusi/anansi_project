from django.shortcuts import render
from django.views.generic import TemplateView
from wagtail.models import Site
import json
import os
from django.conf import settings

class RobotsView(TemplateView):

    content_type = 'text/plain'
    template_name = 'robots.txt'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = context['view'].request
        context['Anansi'] = Site.find_for_request(request)
        return context

# Create your views here.



def get_webpack_bundle():
    manifest_path = os.path.join(settings.BASE_DIR, "static", "manifest.json")
    
    if os.path.exists(manifest_path):
        with open(manifest_path) as f:
            manifest = json.load(f)
        return manifest.get("app.css", "")  # Change "app.css" if needed
    
    return ""

def my_view(request):
    css_bundle = get_webpack_bundle()
    return render(request, "base.html", {"css_bundle": css_bundle})

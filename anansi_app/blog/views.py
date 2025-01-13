from django.shortcuts import render
from django.views.generic import TemplateView
from wagtail.models import Site

class RobotsView(TemplateView):

    content_type = 'text/plain'
    template_name = 'robots.txt'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = context['view'].request
        context['Anansi'] = Site.find_for_request(request)
        return context

# Create your views here.

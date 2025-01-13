from django import template
from readtime import of_html
from django.template import Library, loader

register = Library()
register = template.Library()
def read(html):
    return of_html(html)

register.filter('readtime', read)
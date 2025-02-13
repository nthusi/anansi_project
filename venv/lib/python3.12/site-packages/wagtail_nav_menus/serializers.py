from rest_framework import serializers
from wagtail.api.v2.serializers import StreamField as StreamFieldSerializer
from .models import NavMenu


class NavMenuSerializer(serializers.ModelSerializer):
    menu = StreamFieldSerializer()

    class Meta:
        model = NavMenu
        fields = ("site", "name", "menu")

# # -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django import forms
from django.contrib import admin

from .models import Menu, Carousel, Artwork, Text, Configuration


class CustomModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % obj.name


class MenuAdminForm(forms.ModelForm):
    # parent = CustomModelChoiceField(queryset=Menu.objects.all(), required=False)

    class Meta:
        model = Menu
        fields = '__all__'


class ArtworkAdminForm(forms.ModelForm):
    menu = CustomModelChoiceField(queryset=Menu.objects.all(), required=False)
    carousel = CustomModelChoiceField(queryset=Carousel.objects.all(), required=False)

    class Meta:
        model = Artwork
        fields = '__all__'


class TextAdminForm(forms.ModelForm):
    menu = CustomModelChoiceField(queryset=Menu.objects.all())

    class Meta:
        model = Text
        fields = '__all__'


class CarouselAdminForm(forms.ModelForm):
    menu = CustomModelChoiceField(queryset=Menu.objects.all())

    class Meta:
        model = Carousel
        fields = '__all__'


class ConfigurationAdminForm(forms.ModelForm):
    class Meta:
        model = Configuration
        fields = '__all__'


class MenuAdmin(admin.ModelAdmin):
    form = MenuAdminForm
    list_display = ('pk', 'name', 'order')
    list_editable = ('order',)
    list_filter = ()
admin.site.register(Menu, MenuAdmin)


class CarouselAdmin(admin.ModelAdmin):
    form = CarouselAdminForm
    list_display = ('pk', 'name', 'menu', 'order', 'is_visible')
    list_editable = ('order', 'is_visible')
admin.site.register(Carousel, CarouselAdmin)


class ArtworkAdmin(admin.ModelAdmin):
    form = ArtworkAdminForm
    list_display = ('pk', 'name', 'carousel', 'menu', 'admin_thumbnail', 'order', 'is_visible', 'is_background')
    list_filter = ('carousel', 'menu', 'is_visible')
    list_editable = ('order', 'is_visible', 'is_background')
admin.site.register(Artwork, ArtworkAdmin)


class TextAdmin(admin.ModelAdmin):
    form = TextAdminForm
    list_display = ('pk', 'menu', 'order', 'text', 'order', 'is_visible')
    list_filter = ('menu', 'is_visible')
    list_editable = ('order', 'is_visible')
admin.site.register(Text, TextAdmin)


class ConfigurationAdmin(admin.ModelAdmin):
    form = ConfigurationAdminForm
    list_display = ('pk', 'page_name', 'admin_thumbnail')
    list_filter = ('page_name',)
    list_editable = ('page_name',)
admin.site.register(Configuration, ConfigurationAdmin)


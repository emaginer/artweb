# # -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.utils.translation import ugettext_noop as _
from django.utils.safestring import mark_safe
from django.db import models

from colorfield.fields import ColorField
from math import ceil


class Menu(models.Model):
    menu_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, help_text=_('Nom du menu (Accueil, Sculpture, Atelier...)'), verbose_name='Nom du menu')
    order = models.IntegerField(verbose_name=_('Ordre d\'apparition'), blank=False, null=False)
    # parent = models.ForeignKey('self', null=True, blank=True, default=None, help_text=_('Menu dans lequel ce menu doit apparaître'), on_delete=models.SET_NULL)

    class Meta:
        unique_together = ('name',)
        ordering = ('order',)

    def __str__(self):
        return self.name

    @property
    def content(self):
        carousels = self.carousels.filter(is_visible=True)
        texts = self.texts.filter(is_visible=True)
        artworks = self.artworks.filter(is_visible=True)
        content = [{'type': 'carousel', "obj": c} for c in carousels] + [{'type': 'text', "obj": t} for t in texts] + [{'type': 'image', "obj": a} for a in artworks]
        content.sort(key=lambda x: x['obj'].order, reverse=False)
        return content

    @property
    def background(self):
        bg = self.artworks.filter(is_background=True)
        return bg.first() if bg else None


class Carousel(models.Model):
    carousel_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True, help_text=_('Le nom sera affiché avant le carousel'), verbose_name='Nom du carrousel')
    menu = models.ForeignKey(Menu, null=True, related_name='carousels', help_text=_('Menu dans lequel sera affiché le carousel'), on_delete=models.SET_NULL)
    order = models.IntegerField(default=0, verbose_name=_('Ordre d\'apparition'))
    is_visible = models.BooleanField(default=True, help_text=_('Coché si le carousel doit être affichée sur le site'))

    class Meta:
        ordering = ('order',)
        verbose_name = 'Carrousel'
        verbose_name_plural = 'Carrousels'

    def __str__(self):
        return str(self.menu) + ' - ' + str(self.name)
    
    @property
    def artworks_(self):
        return self.artworks.filter(is_visible=True)


class Artwork(models.Model):
    artwork_id = models.AutoField(primary_key=True)
    carousel = models.ForeignKey(Carousel, null=True, blank=True, related_name='artworks', help_text=_('Carousel dans lequel l\'image est affichée'), verbose_name='Carrousel', on_delete=models.SET_NULL)
    menu = models.ForeignKey(Menu, null=True, blank=True, related_name='artworks', help_text=_('Menu dans lequel sera affiché l\'image en dehors d\'un caroussel'), on_delete=models.SET_NULL)
    is_visible = models.BooleanField(default=True, help_text=_('Coché si l\'image doit être affichée sur le site'), verbose_name='Est visible ?')
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name='Nom')
    description = models.CharField(max_length=255, null=True, blank=True, verbose_name='Description')
    picture = models.ImageField(blank=True, upload_to='img', verbose_name='Photo')

    order = models.IntegerField(default=0, verbose_name='Ordre d\'apparition')
    is_background = models.BooleanField(default=False, help_text=_('Coché pour que l\'image soit le fond de la barre de menu'), verbose_name='Mis en fond ?')
    # color = ColorField(default='#FFF', help_text=_('Couleur pour les textes affichés sur l\'image'), verbose_name='Couleur du texte du menu')
    # bg_color = ColorField(default='#FFF', help_text=_('Couleur de base du fond du site si cette image est en barre de menu'), verbose_name='Couleur du fond')
    # opacity = models.FloatField(default=1, help_text=_('Opacité de la couleur de fond d\'écran - 1 = opaque, 0 = invisible'))

    def admin_thumbnail(self):
        return mark_safe('<img height="30px" src="%s" />' % (self.picture.url))
    admin_thumbnail.short_description = 'Apercu'
    admin_thumbnail.allow_tags = True

    class Meta:
        ordering = ('order',)
        verbose_name = 'Image'
        verbose_name_plural = 'Images'

    def __str__(self):
        return str(self.carousel) + ' ' + str(self.name)


class Text(models.Model):
    text_id = models.AutoField(primary_key=True)
    text = models.TextField(verbose_name='Texte')
    menu = models.ForeignKey(Menu, null=True, related_name='texts', help_text=_('Texte à afficher dans le menu correspondant'), on_delete=models.SET_NULL)
    order = models.IntegerField(default=0, verbose_name='Ordre d\'apparition')
    is_visible = models.BooleanField(default=True, help_text=_('Coché si le texte doit être affiché sur le site'), verbose_name='Est visible ?')

    class Meta:
        ordering = ('order',)
        verbose_name = 'Texte'
        verbose_name_plural = 'Textes'

    def __str__(self):
        return str(self.menu) + ' ' + str(self.text)


class Configuration(models.Model):
    conf_id = models.AutoField(primary_key=True)
    page_name = models.CharField(null=True, blank=True, max_length=255)
    favicon = models.ImageField(blank=True, upload_to='img', verbose_name='Favicon')

    def admin_thumbnail(self):
        return u'<img height="30px" src="%s" />' % (self.favicon.url)
    admin_thumbnail.short_description = 'Apercu'
    admin_thumbnail.allow_tags = True

    class Meta:
        verbose_name = 'Configuration'
        verbose_name_plural = 'Configurations'

    def __str__(self):
        return str(self.page_name)


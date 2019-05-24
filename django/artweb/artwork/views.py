# # -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render

from rest_framework import generics
from .models import Menu, Configuration


@csrf_protect
def index(request):
    menus = Menu.objects.order_by('order').prefetch_related('carousels', 'texts', 'artworks')
    return render(request, 'index.html', {"menus": menus, "conf": Configuration.objects.first()})

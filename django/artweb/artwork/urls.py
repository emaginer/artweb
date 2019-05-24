# # -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.urls import path
from .views import index

urlpatterns = [
    path('', index, name='index')
]

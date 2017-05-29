#! /usr/bin/env python
# -*- coding: utf-8 -*-
# S.D.G

# Imports
from django.conf.urls import url
from .views import home

__author__ = 'Ben Johnston'
__revision__ = '0.1'
__date__ = 'Monday 29 May  13:44:59 AEST 2017'
__license__ = 'MPL v2.0'

urlpatterns = [
    url(r'^', home, name='home'),
]

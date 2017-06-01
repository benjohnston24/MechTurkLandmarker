#-*- coding: utf-8 -*-
import os
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.staticfiles.templatetags.staticfiles import static
from MechTurkLandmarker.settings import STATIC_ROOT, PAGE_TITLE 
import traceback
import sys

# Create your views here.
def home(request):


    return render(request, 'FaceMarker/index.html',
            {
                'page_title': PAGE_TITLE,
                'eg_img': static('lmrk_P1.jpg'),
                'display_img': static('template_face.png'),
                'config': static('config.json'),
            })

import os
from django.shortcuts import render
from MechTurkLandmarker.settings import PAGE_TITLE 

# Create your views here.
def home(request):

    return render(request, 'FaceMarker/index.html',
            {'page_title': PAGE_TITLE})

import os

from django.shortcuts import render

def map(request):
    return render(request, 'web/map.html', {'mapID': os.getenv('mapid')})
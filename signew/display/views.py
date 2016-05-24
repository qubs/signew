from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Display, Slide

def index(request):
    displays = Display.objects.all()
    context = { 'display_list': displays }
    return render(request, 'display/index.html', context)

def show(request, display_id):
    display = Display.objects.get(pk=display_id)
    context = { 'display': display, 'slide_list': display.slides.all() }
    return render(request, 'display/show.html', context)

#    Copyright 2016 the Queen's University Biological Station and
#    the Signew project authors.

#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.


import hashlib

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader

from .models import Display, Slide


def hash_display_slides(display_slides):
    return hashlib.sha256(str(list(display_slides)).encode('utf-8')).hexdigest()


def index(request):
    displays = Display.objects.all()
    context = { 'display_list': displays }
    return render(request, 'display/index.html', context)

def show(request, display_id):
    display = Display.objects.get(pk=display_id)
    context = { 'display': display, 'slide_list': display.slides.all() }
    return render(request, 'display/show.html', context)


def show_hash(request, display_id):
    display = Display.objects.get(pk=display_id)
    return JsonResponse({
        'display': display.id,
        'hash': hash_display_slides(display.slides.values())
    })

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


from django.db import models
from sortedm2m.fields import SortedManyToManyField
from ckeditor.fields import RichTextField
from colorful.fields import RGBColorField


class Slide(models.Model):
    URL_IMAGE = 'URLI'
    URL_PAGE = 'URLP'
    HOSTED_IMAGE = 'HSTI'
    HOSTED_PAGE = 'HSTP'
    SLIDE_TYPE_CHOICES = (
        (URL_IMAGE, 'URL to Image'),
        (URL_PAGE, 'URL to Page'),
        (HOSTED_IMAGE, 'Hosted Image'),
        (HOSTED_PAGE, 'Hosted Page'),
    )

    slide_name = models.CharField(max_length=255)
    slide_type = models.CharField(max_length=4, choices=SLIDE_TYPE_CHOICES)
    slide_url = models.URLField(blank=True, null=True)
    live_load = models.BooleanField(default=False)
    caption = RichTextField(blank=True, null=True)
    background_color = RGBColorField(blank=True, null=True)
    slide_data = models.TextField(blank=True, null=True)
    slide_file = models.FileField(blank=True, null=True)
    timing = models.PositiveIntegerField(default=5000)

    def __str__(self):
        return self.slide_name


class Display(models.Model):
    display_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    slides = SortedManyToManyField(Slide)

    def __str__(self):
        return self.display_name

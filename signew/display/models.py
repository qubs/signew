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
    date_created = models.DateTimeField()
    date_updated = models.DateTimeField()
    slides = SortedManyToManyField(Slide)

    def __str__(self):
        return self.display_name

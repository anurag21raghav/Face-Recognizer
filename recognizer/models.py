import os
from django.db import models
from django.utils import timezone

# Create your models here.

def get_image_path(instance, filename):
	return os.path.join('photos', str(instance.id), filename)

class Image(models.Model):
	user = models.ForeignKey('auth.User')
	name = models.CharField(max_length=200, default="N/A")
	image = models.ImageField(upload_to=get_image_path, blank=True, null=True)
	upload_date = models.DateTimeField(
		default=timezone.now)
	

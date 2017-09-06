from django.conf.urls import include, url
from django.contrib import admin


from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
import os
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
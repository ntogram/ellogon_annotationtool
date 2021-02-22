from django.conf.urls import url
from django.urls import path
from .views import index
import sys
import os




urlpatterns = [

    path('', index),  # for the empty url
    url(r'^.*/$', index)  # for all other urls
]

from django.contrib import admin
from django.urls import re_path, path
from .views import index, shirt_detail_page


urlpatterns = [
    re_path('^$', index),
    path('shirt/<int:shirt_id>/', shirt_detail_page),
]

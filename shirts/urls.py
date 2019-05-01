from django.contrib import admin
from django.urls import re_path, path
from .views import index, shirt_detail_page, upload, get_comment, like_comment, add_comment, download_image, \
    manual_upload, constructor, constructor_upload, order_view


urlpatterns = [
    re_path('^$', index, name="index"),
    path('shirt/<int:shirt_id>/', shirt_detail_page),
    path('upload/', upload, name="shirts.views.upload"),
    path('shirt/get_comment/', get_comment),
    path('shirt/like_comment/', like_comment),
    path('shirt/add_comment/', add_comment),
    path('shirt/download/<int:shirt_id>/', download_image),
    path('manual/', manual_upload),
    path('shirt/constructor/', constructor),
    path('shirt/constructor_upload/', constructor_upload),
    path('shirt/order/', order_view, name="order_view")
]

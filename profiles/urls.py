from django.contrib import admin
from django.urls import re_path, include, path
from django.contrib.auth.views import LoginView, PasswordResetView, LogoutView
from .views import activate, signup


urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', include('django.contrib.auth.urls')),
    path('', include('django_registration.backends.activation.urls')),
    path('signup/', signup, name='signup'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            activate, name='activate'),
]

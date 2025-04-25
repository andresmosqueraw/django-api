from django.contrib import admin
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^login$', views.login),
    re_path(r'^register$', views.register),
    re_path(r'^profile$', views.profile),
]
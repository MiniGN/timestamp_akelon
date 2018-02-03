from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^SendTimestamp/', views.SendTimestamp, name='SendTimestamp'),
    url(r'^async_update_panels/', views.async_update_panels, name='async_update_panels'),
    url(r'^async_update_navbar/', views.async_update_navbar, name='async_update_navbar'),

]
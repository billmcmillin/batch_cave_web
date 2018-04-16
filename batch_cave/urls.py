"""batch_cave URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from converter import views

urlpatterns = [
    url(r'^$', views.home_page, name='home_page'),
    url(r'^conversions/$', views.index, name='index'),
    url(r'^conversions/index$', views.index, name='index'),
    # ex: /conversions/create
    url(r'^conversions/create/$', views.create, name='create'),
url(r'^download/(?P<conversion_id>[0-9]+)/$', views.download, name='download'),
    url(r'^download_original/(?P<conversion_id>[0-9]+)/$', views.download_original, name='download_original'),
    url(r'^download_original_mrk/(?P<conversion_id>[0-9]+)/$',views.download_original_mrk, name='download_original_mrk'),
    url(r'^download_result_mrk/(?P<conversion_id>[0-9]+)/$', views.download_result_mrk, name='download_result_mrk'),
]

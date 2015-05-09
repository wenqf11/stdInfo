#coding: utf-8
from django.conf.urls import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'stdInfo.views.home', name='home'),
    url(r'^$', 'postgraduate.views.index'),
    url(r'^basic_info$', 'postgraduate.views.get_basic_info'),
)


#coding: utf-8
__author__ = 'vince'
from django.conf.urls import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'stdInfo.views.home', name='home'),
    url(r'^$', 'student.views.index'),
    url(r'^change_password/$', 'student.views.change_password'),
)
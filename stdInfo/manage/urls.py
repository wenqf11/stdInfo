#coding: utf-8
__author__ = 'Qingfu Wen'
from django.conf.urls import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'stdInfo.views.home', name='home'),
    url(r'^$', 'manage.views.index'),
    url(r'^basic_info$', 'manage.views.get_basic_info'),
    url(r'^degree_info$', 'manage.views.get_degree_info'),
    url(r'^award_info$', 'manage.views.get_award_info'),
    url(r'^work_info$', 'manage.views.get_work_info'),
    url(r'^graduation_info$', 'manage.views.get_graduation_info'),
    url(r'^detail', 'manage.views.get_detail'),
    url(r'^import_excel', 'manage.views.import_excel'),
    url(r'^export_excel', 'manage.views.export_excel'),
)
#coding: utf-8
__author__ = u"王彬彬"
__email__ = '18800160527@163.com'

from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.models import User
from student.models import *


def index(request):
    return get_basic_info(request)


def get_basic_info(request):
    username = request.session.get("username")
    user = User.objects.get(username=username)
    student = Student.objects.get(user=user)
    return render_to_response("student/student.html", {'student': student}, context_instance=RequestContext(request))
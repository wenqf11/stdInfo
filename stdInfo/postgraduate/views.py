#coding: utf-8

from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.models import User
from postgraduate.models import *


def index(request):
    return get_basic_info(request)


def get_basic_info(request):
    username = request.session.get("username")
    user = User.objects.get(username=username)
    student = Postgraduate.objects.get(user=user)
    return render_to_response("postgraduate/postgraduate.html", locals(), context_instance=RequestContext(request))


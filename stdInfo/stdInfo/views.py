#coding: utf-8
__author__ = 'vince'
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response


def index(request):
    if request.user.is_authenticated():
        if request.user.is_staff:
            return HttpResponseRedirect('/manage')
        else:
            return HttpResponseRedirect('/student')
    return render_to_response("index.html")

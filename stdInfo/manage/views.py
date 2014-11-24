#coding: utf-8
__author__ = 'vince'
from django.http import HttpResponse
from django.shortcuts import render_to_response


def index(request):
    return HttpResponse("hello world")
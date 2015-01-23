#coding: utf-8
__author__ = 'Qingfu Wen'
__contact__ = 'thssvince@163.com'
__date__ = '2014-12-04'
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response


def index(request):
    if request.user.is_authenticated():
            if request.user.is_staff:
                return HttpResponseRedirect('/manage')
            else:
                return HttpResponseRedirect('/student')

    if request.method == 'GET':
        return render_to_response("index.html", context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/manage')

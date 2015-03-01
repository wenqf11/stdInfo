#coding: utf-8
__author__ = 'Qingfu Wen'
__contact__ = 'thssvince@163.com'
__date__ = '2014-12-04'
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, render, redirect
from django.template.loader import get_template
from django.db import connection
from django.http import HttpResponse
from student.models import Student
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import Http404
import datetime
import xlwt



def log(request):
    return render_to_response('student.html')


def index(request):
    errors = []
    if request.method == 'GET':
        request.session.set_test_cookie()
        return render_to_response("index.html", context_instance=RequestContext(request))
    if not request.user.is_authenticated():
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
        else:
            errors.append('username or password is wrong!')
            return render_to_response("index.html", {'errors':errors}, context_instance=RequestContext(request))
    if request.user.is_authenticated():
        if request.user.is_staff:
            return HttpResponseRedirect('/manage')
        else:
            return HttpResponseRedirect('/student')


def logout(request):
    auth.logout(request)
    return render_to_response("index.html", context_instance=RequestContext(request))


def create_user(request, parm1, parm2):
    user = User(username=parm1,
                password=parm2)
    user.save()
    user = User.objects.get(username=parm1)
    user.set_password(parm2)
    user.save()
    return HttpResponse('create user successfully. username:%s, password:%s'%(user.username, user.password))

def save_xls(request):
    book = xlwt.Workbook(encoding='utf-8')
    sheet = book.add_sheet('untitled')
    sheet.write(0, 0, "姓名")
    sheet.write(0, 1, "密码")
    user = User.objects.all()
    data1 = []
    data = []
    for i in user.values():
        data1.append(i["username"])
        data1.append(i["password"])
        data.append(data1)
        data1 = []
    for k in range(len(data)):
        for j in range(len(data[k])):
            sheet.write(k+1,j,data[k][j])
    response = HttpResponse(mimetype='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=example.xls'
    book.save(response)
    return response


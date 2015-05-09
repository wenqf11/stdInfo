#coding: utf-8
__author__ = u"王彬彬"
__email__ = '18800160527@163.com'


from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from student.models import *


@login_required
def index(request):
    if request.method == 'GET':
        if not request.user.is_staff:
            student = Student.objects.get(user=request.user)
            return render_to_response("student/student.html", {'student': student}, context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect('/manage')
    else:
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')
        politics = request.POST.get('politics', '')
        postcode = request.POST.get('postcode', '')
        address = request.POST.get('address', '')
        family_phone = request.POST.get('address', '')
        graduation_email = request.POST.get('graduation_email', '')
        graduation_phone = request.POST.get('graduation_phone', '')
        destination = request.POST.get('destination', '')
        competition = request.POST.get('competition', '')
        social_work = request.POST.get('social_work', '')
        student = Student.objects.get(user=request.user)
        student.phone = phone
        student.email = email
        student.politics = politics
        student.family.address = address
        student.family.phone = family_phone
        student.graduation.email = graduation_email
        student.graduation.phone = graduation_phone
        student.graduation.destination = destination
        student.experience.competition = competition
        student.experience.social_work = social_work
        student.family.save()
        student.graduation.save()
        student.experience.save()
        student.save()
        return render_to_response("student/student.html", {'student': student}, context_instance=RequestContext(request))


@login_required
def change_password(request):
    old_password = request.POST.get("old_password", "")
    new_password = request.POST.get("new_password", "")
    confirm_password = request.POST.get("confirm_password", "")

    if new_password != confirm_password:
        return HttpResponse("修改失败，新密码不一致！")
    elif len(new_password) < 6:
        return HttpResponse("修改失败，密码太短！")

    user = auth.authenticate(username=request.user.username, password=old_password)
    if user is not None:
        user.set_password(new_password)
        user.save()
        return HttpResponse("密码修改成功！")
    else:
        return HttpResponse("修改失败，旧密码错误！")
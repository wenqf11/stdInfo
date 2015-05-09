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

    scholarships = Scholarship.objects.filter(student=student)
    grants = Grant.objects.filter(student=student)
    loans = Loan.objects.filter(student=student)
    award_scholarship = ''
    award_grant = ''
    award_loan = ''
    for scholarship in scholarships:
        award_scholarship += scholarship.code + ' ' + scholarship.year + ' ' + scholarship.name + ' ' + \
                             str(scholarship.amount) + '\r\n'
    for grant in grants:
        award_grant += grant.code + ' ' + grant.year + ' ' + grant.name + ' ' + str(grant.amount) + '\r\n'
    for loan in loans:
        award_loan += loan.info + '\r\n'

    competitions = Competition.objects.filter(student=student)
    social_works = SocialWork.objects.filter(student=student)
    work_competition = ''
    work_social_work = ''
    for competition in competitions:
        work_competition += competition.year + ' ' + competition.name + '\r\n'

    for social_work in social_works:
        work_social_work += social_work.year + ' ' + social_work.name + '\r\n'

    return render_to_response("postgraduate/postgraduate.html", locals(), context_instance=RequestContext(request))


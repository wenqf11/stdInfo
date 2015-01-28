#coding: utf-8
__author__ = 'vince'
from django.db import models
from django.contrib.auth.models import User

class Teacher(models.Model):
    user = models.OneToOneField(User, null=True)
    name = models.CharField(u'姓名', max_length=30)
    phone = models.CharField(u'电话', max_length=11)
    email = models.CharField(u'邮箱', max_length=50)
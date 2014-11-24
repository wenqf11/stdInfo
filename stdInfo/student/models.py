#coding: utf-8
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Student(models.Model):
    user = models.OneToOneField(User)
    number = models.IntegerField(u"学号")
    name = models.CharField(u"姓名", max_length=30)
    gender = models.BooleanField(u"性别", default=False)
    ID_number = models.CharField(u"身份证号", max_length=20)
    birthday = models.DateField(u"出生日期")
    nation = models.CharField(u"民族", max_length=20)
    nationality = models.CharField(u"国籍", max_length=20, default=u"中国")
    politics = models.CharField(u"政治面貌", max_length=20, default=u"共青团员")
    high_school = models.CharField(u"毕业中学", max_length=50)
    exam_province = models.CharField(u"考区", max_length=20)
    entrance_exam_score = models.CharField(u"高考总分", max_length=20)


class DegreeInfo(models.Model):
    department= models.CharField(u"系所名", max_length=30)
    major = models.CharField(u"专业名", max_length=30)
    class_num  = models.CharField(u"教学班", max_length=30)
    grade = models.CharField(u"所属年级", max_length=20)
    duration = models.IntegerField(u"学制")
    change =  models.TextField(u"是否异动",blank=True)
    degree_type = models.CharField(u'学位', max_length=20)
    is_candidate =  models.BooleanField(u"是否有学籍", default=True)
    student_type = models.CharField(u'学生类别', max_length=20,default=u"一般")
    expenditure_type = models.CharField(u'经费办法', max_length=20,default=u"软件")
    exchange_info = models.TextField(u"交换时间/学校",blank=True)

class SecondDegree(models.Model):
    major_type = models.CharField(u"二学位", max_length=30)
    major = models.CharField(u"二学位专业名", max_length=50)
    department_num = models.CharField(u"二学位单位内码", max_length=20)
    department_name = models.CharField(u"二学位单位简称", max_length=20)
    major_num = models.CharField(u"二学位专业号", max_length=20)
    class_num  = models.CharField(u"二学位班号", max_length=20)
    date = models.DateField(u'二学位毕业日期')
    scores_rank = models.CharField(u"大三学年成绩及排名", max_length=50)

class FamilyInfo(models.Model):
    address = models.CharField(u"家庭住址", max_length=200)
    hukou_type = models.CharField(u'户口类型', max_length=20)
    avg_income = models.FloatField(u'家庭人均月收入（元）')
    I_value = models.FloatField(u"I值")
    poverty_degree  = models.CharField(u'贫困等级', max_length=20)
    detail = models.TextField(u'经济情况说明',blank=True)

class Scholarship(models.Model):
    year = models.CharField(u"学年度", max_length=50)
    hukou_type = models.CharField(u'户口类型', max_length=20)
    name = models.CharField(u"学年度", max_length=50)
    amount = models.IntegerField(u"获奖金额")

class Loan(models.Model):
    info = models.CharField(u"贷款", max_length=200)

class Competition(models.Model):
    year = models.CharField(u"学年度", max_length=50)
    name = models.TextField(u"科技赛事名称",blank=True)

class SocialWork(models.Model):
    year = models.CharField(u"学年度", max_length=50)
    name = models.TextField(u"社会工作（学生干部情况）",blank=True)

class GraduationInfo(models.Model):
    date = models.DateField(u'毕业日期')
    type = models.CharField(u"毕业类别", max_length=20)
    phone = models.CharField(u"毕业手机", max_length=11)
    email = models.CharField(u"毕业邮箱", max_length=50)
    destination = models.CharField(u"毕业去向", max_length=50)
    direction =  models.CharField(u"分流方向", max_length=50)

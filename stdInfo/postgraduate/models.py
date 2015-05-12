#coding:utf-8
__author__ = 'wangbb'
__email__ = '18800160527@163.com'
from django.db import models
from django.contrib.auth.models import User


class PostgraduateDegree(models.Model):
    degree = models.CharField(u"学位", max_length=30, null=True)
    class_name = models.CharField(u"班号", max_length=30, null=True)
    grade = models.CharField(u'年级', max_length=20, null=True)
    first_test = models.CharField(u"初试成绩", max_length=30, null=True)
    opening_time = models.DateField(u"开题时间", null=True)
    exchange_info = models.CharField(u"交流学校/时间", max_length=100, null=True)
    admissions_way = models.CharField(u"招生途径", max_length=20, default=u"统考")
    rank_before_graduation = models.CharField(u"毕业前或推免前综合排名", max_length=30, null=True)
    admissions_rank = models.CharField(u"入学成绩/排名", max_length=50, null=True)
    regular_school = models.CharField(u"本科毕业学校", max_length=50, null=True)
    regular_major = models.CharField(u"本科专业", max_length=50, null=True)


class PostGraduationInfo(models.Model):
    date = models.DateField(u'毕业日期', null=True)
    destination = models.CharField(u"毕业去向", max_length=50, null=True)
    job = models.CharField(u"职务", max_length=50, null=True)
    salary = models.CharField(u"年薪", max_length=50, null=True)
    alumni_donation = models.CharField(u"校友捐款", max_length=50, null=True)
    phone = models.CharField(u"毕业手机", max_length=11, null=True)
    email = models.CharField(u"毕业邮箱", max_length=50, null=True)


class ScholarshipLoan(models.Model):
    scholarship = models.TextField(u'奖学金', null=True)
    grant = models.TextField(u'助学金', null=True)
    loan = models.TextField(u'贷款', null=True)


class Experience(models.Model):
    competition = models.TextField(u'科技赛事', null=True)
    social_work = models.TextField(u'社会工作', null=True)


class Postgraduate(models.Model):
    user = models.OneToOneField(User, null=True)
    degree = models.OneToOneField(PostgraduateDegree, null=True)
    graduation = models.OneToOneField(PostGraduationInfo, null=True)
    scholarship_loan = models.OneToOneField(ScholarshipLoan, null=True)
    experience = models.OneToOneField(Experience, null=True)
    number = models.CharField(u"学号", max_length=30)
    name = models.CharField(u"姓名", max_length=30, null=True)
    gender = models.CharField(u"性别", max_length=30, default=False)
    nation = models.CharField(u"民族", max_length=20, null=True)
    politics = models.CharField(u"政治面貌", max_length=20, default=u"共青团员")
    tutor = models.CharField(u"导师", max_length=30, null=True)
    phone = models.CharField(u"手机", max_length=11, null=True)
    email = models.CharField(u"邮箱", max_length=50, null=True)
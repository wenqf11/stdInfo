#coding: utf-8
__author__ = 'Qingfu Wen'
__email__ = 'thssvince@163.com'
from django.db import models
from django.contrib.auth.models import User


class DegreeInfo(models.Model):
    department = models.CharField(u"系所名", max_length=30, null=True)
    major = models.CharField(u"专业名", max_length=30, null=True)
    class_num = models.CharField(u"教学班", max_length=30, null=True)
    grade = models.CharField(u"所属年级", max_length=20, null=True)
    duration = models.IntegerField(u"学制", null=True)
    change = models.TextField(u"是否异动", null=True)
    degree_type = models.CharField(u'学位', max_length=20)
    is_foreign = models.BooleanField(u"是否留学生", default=True)
    is_candidate = models.BooleanField(u"是否有学籍", default=True)
    student_type = models.CharField(u'学生类别', max_length=20, default=u"一般")
    expenditure_type = models.CharField(u'经费办法', max_length=20, default=u"软件")
    exchange_info = models.TextField(u"交换时间/学校", null=True)
    scores_rank = models.CharField(u"大三年级学分绩及排名", max_length=50, null=True)


class SecondDegree(models.Model):
    major_type = models.CharField(u"二学位", max_length=30, null=True)
    major = models.CharField(u"二学位专业名", max_length=50, null=True)
    department_num = models.CharField(u"二学位单位内码", max_length=20, null=True)
    department_name = models.CharField(u"二学位单位简称", max_length=20, null=True)
    major_num = models.CharField(u"二学位专业号", max_length=20, null=True)
    class_num = models.CharField(u"二学位班号", max_length=20, null=True)
    date = models.DateField(u'二学位毕业日期', null=True)


class FamilyInfo(models.Model):
    address = models.CharField(u"家庭住址", max_length=200, null=True)
    hukou_type = models.CharField(u'户口类别', max_length=20, null=True)
    avg_income = models.FloatField(u'家庭人均月收入（元）', null=True)
    I_value = models.FloatField(u"I值", null=True)
    poverty_degree = models.CharField(u'贫困等级', max_length=20, null=True)
    detail = models.TextField(u'经济情况说明', null=True)


class GraduationInfo(models.Model):
    date = models.DateField(u'毕业日期', null=True)
    type = models.CharField(u"毕业类别", max_length=20, null=True)
    phone = models.CharField(u"毕业手机", max_length=11, null=True)
    email = models.CharField(u"毕业邮箱", max_length=50, null=True)
    destination = models.CharField(u"毕业去向", max_length=50, null=True)
    direction = models.CharField(u"分流方向", max_length=50, null=True)


class Student(models.Model):
    user = models.OneToOneField(User, null=True)
    degree = models.OneToOneField(DegreeInfo, null=True)
    second_degree = models.OneToOneField(SecondDegree, null=True)
    family = models.OneToOneField(FamilyInfo, null=True)
    graduation = models.OneToOneField(GraduationInfo, null=True)
    number = models.IntegerField(u"学号")
    name = models.CharField(u"姓名", max_length=30, null=True)
    gender = models.BooleanField(u"性别", default=False)   # 0 means girl, 1 means boy
    identity_number = models.CharField(u"身份证号", max_length=20, null=True)
    birthday = models.DateField(u"出生日期", null=True)
    nation = models.CharField(u"民族", max_length=20, null=True)
    nationality = models.CharField(u"国籍", max_length=20, default=u"中国")
    politics = models.CharField(u"政治面貌", max_length=20, default=u"共青团员")
    high_school = models.CharField(u"毕业中学", max_length=50, null=True)
    exam_province = models.CharField(u"考区", max_length=20, null=True)
    entrance_exam_score = models.CharField(u"高考总分", max_length=20, null=True)


class Scholarship(models.Model):
    student = models.ForeignKey(Student)
    year = models.CharField(u"奖学金学年度", null=True, max_length=50)
    honor_grade = models.CharField(u'荣誉等级', null=True, max_length=50)
    name = models.CharField(u"奖项简称", null=True, max_length=50)
    amount = models.IntegerField(u"获奖金额", null=True)


class Grant(models.Model):
    student = models.ForeignKey(Student)
    year = models.CharField(u"助学金学年度", null=True, max_length=50)
    name = models.CharField(u"助项简称", null=True, max_length=50)
    amount = models.IntegerField(u"获助金额", null=True)


class Loan(models.Model):
    student = models.ForeignKey(Student)
    info = models.CharField(u"贷款", null=True, max_length=200)


class Competition(models.Model):
    student = models.ForeignKey(Student)
    year = models.CharField(u"科技赛事学年度", null=True, max_length=50)
    name = models.TextField(u"科技赛事名称", null=True)


class SocialWork(models.Model):
    student = models.ForeignKey(Student)
    year = models.CharField(u"社工学年度", null=True, max_length=50)
    name = models.TextField(u"社会工作（学生干部情况）", null=True)

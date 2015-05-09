#coding: utf-8
__author__ = 'Qingfu Wen'
__email__ = 'thssvince@163.com'
from django.db import models
from django.contrib.auth.models import User


class DegreeInfo(models.Model):
    major = models.CharField(u"专业名", max_length=30, null=True)
    class_num = models.CharField(u"教学班", max_length=30, null=True)
    grade = models.CharField(u"所属年级", max_length=20, null=True)
    change = models.TextField(u"是否异动", null=True)
    degree_type = models.CharField(u'学位', max_length=20)
    is_foreign = models.CharField(u"是否留学生", max_length=10, default=True)
    exchange_info = models.TextField(u"交换时间/学校", null=True)
    english_level = models.TextField(u'英语水平', null=True)
    scores_rank = models.CharField(u"大三年级学分绩及排名", max_length=50, null=True)


class SecondDegree(models.Model):
    major = models.CharField(u"二学位专业名", max_length=50, null=True)
    department_name = models.CharField(u"二学位单位简称", max_length=20, null=True)
    class_num = models.CharField(u"二学位班号", max_length=20, null=True)
    date = models.DateField(u'二学位毕业日期', null=True)


class FamilyInfo(models.Model):
    address = models.CharField(u"家庭住址", max_length=200, null=True)
    phone = models.TextField(u'父母联系方式', null=True)
    postcode = models.TextField(u'邮编', null=True)
    hukou_type = models.CharField(u'户口类别', max_length=20, null=True)
    avg_income = models.FloatField(u'家庭人均月收入（元）', null=True)
    I_value = models.FloatField(u"I值", null=True)
    poverty_degree = models.CharField(u'贫困等级', max_length=20, null=True)
    detail = models.TextField(u'经济状况说明', null=True)


class GraduationInfo(models.Model):
    date = models.DateField(u'毕业日期', null=True)
    type = models.CharField(u"毕业类别", max_length=20, null=True)
    phone = models.CharField(u"毕业手机", max_length=11, null=True)
    email = models.CharField(u"毕业邮箱", max_length=50, null=True)
    destination = models.CharField(u"毕业去向", max_length=50, null=True)
    direction = models.CharField(u"分流方向", max_length=50, null=True)
    date_ad = models.CharField(u"补行毕业时间", max_length=50, null=True)
    type_ad = models.CharField(u"补行毕业类别", max_length=50, null=True)


class ScholarshipLoan(models.Model):
    scholarship= models.TextField(u'奖学金', null=True)
    grant = models.TextField(u'助学金', null=True)
    loan = models.TextField(u'贷款', null=True)
    temp_loan = models.TextField(u'临时借款', null=True)


class Experience(models.Model):
    competition  = models.TextField(u'科技赛事', null=True)
    social_work  = models.TextField(u'社会工作', null=True)


class Student(models.Model):
    user = models.OneToOneField(User, null=True)
    degree = models.OneToOneField(DegreeInfo, null=True)
    second_degree = models.OneToOneField(SecondDegree, null=True)
    family = models.OneToOneField(FamilyInfo, null=True)
    graduation = models.OneToOneField(GraduationInfo, null=True)
    scholarship_loan = models.OneToOneField(ScholarshipLoan, null=True)
    experience = models.OneToOneField(Experience, null=True)
    number = models.CharField(u"学号", max_length=30)
    name = models.CharField(u"姓名", max_length=30, null=True)
    gender = models.CharField(u"性别", max_length=10, default=False)
    identity_number = models.CharField(u"身份证号", max_length=20, null=True)
    birthday = models.DateField(u"出生日期", null=True)
    nation = models.CharField(u"民族", max_length=20, null=True)
    nationality = models.CharField(u"国籍", max_length=20, default=u"中国")
    politics = models.CharField(u"政治面貌", max_length=20, default=u"共青团员")
    high_school = models.CharField(u"毕业中学", max_length=50, null=True)
    exam_province = models.CharField(u"考区", max_length=20, null=True)
    entrance_exam_score = models.CharField(u"高考总分", max_length=20, null=True)
    email = models.CharField(u"邮箱", max_length=100, null=True)
    phone = models.CharField(u"手机号", max_length=50, null=True)
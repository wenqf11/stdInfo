#coding: utf-8
__author__ = 'Qingfu Wen'
__email__ = 'thssvince@163.com'
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from student.models import *
import datetime
import xlrd

basic_info_set = set([
    u'学号',
    u'姓名',
    u'系所名',
    u'专业名',
    u'教学班',
    u'所属年级',
    u'性别',
    u'身份证号',
    u'出生日期',
    u'民族',
    u'国籍',
    u'政治面貌',
    u'考区',
    u'毕业中学',
    u'高考总分',
    u"系所名",
    u"专业名",
    u"教学班",
    u"所属年级",
    u"学制",
    u"是否异动",
    u'学位',
    u'是否留学生',
    u"是否有学籍",
    u'学生类别',
    u'经费办法',
    u"交换时间/学校",
    u"大三年级学分绩及排名",
    u"二学位",
    u"二学位专业名",
    u"二学位单位内码",
    u"二学位单位简称",
    u"二学位专业号",
    u"二学位班号",
    u'二学位毕业日期',
    u"家庭住址",
    u'户口类型',
    u'家庭人均月收入（元）',
    u"I值",
    u'贫困等级',
    u'经济情况说明',
    u'毕业日期',
    u"毕业类别",
    u"毕业手机",
    u"毕业邮箱",
    u"毕业去向",
    u"分流方向",
])

def index(request):
    return render_to_response("manage/manage.html", {}, context_instance=RequestContext(request))


def get_basic_info(request):
    return render_to_response("manage/manage.html", {
        'page': 'basic_info',
    }, context_instance=RequestContext(request))


def get_degree_info(request):
    return render_to_response("manage/manage.html", {
        'page': 'degree_info',
    }, context_instance=RequestContext(request))


def get_award_info(request):
    return render_to_response("manage/manage.html", {
        'page': 'award_info',
    }, context_instance=RequestContext(request))


def get_work_info(request):
    return render_to_response("manage/manage.html", {
        'page': 'work_info',
    }, context_instance=RequestContext(request))


def get_graduation_info(request):
    return render_to_response("manage/manage.html", {
        'page': 'graduation_info',
    }, context_instance=RequestContext(request))


def get_detail(request):
    return render_to_response("manage/detail.html", {}, context_instance=RequestContext(request))


def export_excel(request):
    return render_to_response("manage/export_excel.html", {}, context_instance=RequestContext(request))


def import_excel(request):
    if request.method == 'POST':
        basic_info = request.FILES['basic_info']
        error_msg = ''
        if basic_info:
            data = xlrd.open_workbook(file_contents=basic_info.read())
            table = data.sheets()[0]
            nrows = table.nrows
            ncols = table.ncols
            for i in xrange(1, nrows):
                try:
                    std_num = int(table.cell(i, 1).value)
                    if len(str(std_num)) != 10:
                        raise ValueError('学号有误')
                    students = Student.objects.filter(number=std_num)
                    if len(students) == 0:
                        student = Student(number=std_num)
                        degree = DegreeInfo()
                        second_degree = SecondDegree()
                        graduation = GraduationInfo()
                    else:
                        student = students[0]
                        degree = student.degree
                        second_degree = student.second_degree
                        graduation = student.graduation

                    for j in xrange(2, ncols):
                        try:
                            if table.cell(0, j).value in basic_info_set:
                                value = table.cell(i, j).value
                                if table.cell(0, j).value == u'姓名':
                                    student.name = value
                                elif table.cell(0, j).value == u'性别':
                                    student.gender = True if value == u'男' else False
                                elif table.cell(0, j).value == u'身份证号':
                                    student.identity_number = value
                                elif table.cell(0, j).value == u'出生日期':
                                    student.birthday = datetime.datetime.strptime(str(int(value)), "%Y%m%d")
                                elif table.cell(0, j).value == u'民族':
                                    student.nation = value
                                elif table.cell(0, j).value == u'国籍':
                                    student.nationality = value
                                elif table.cell(0, j).value == u'政治面貌':
                                    student.politics = value
                                elif table.cell(0, j).value == u'毕业中学':
                                    student.high_school = value
                                elif table.cell(0, j).value == u'考区':
                                    student.exam_province = value
                                elif table.cell(0, j).value == u'高考总分':
                                    student.entrance_exam_score = value
                                elif table.cell(0, j).value == u'系所名':
                                    degree.department = value
                                elif table.cell(0, j).value == u'专业名':
                                    degree.major = value
                                elif table.cell(0, j).value == u'教学班':
                                    degree.class_num = value
                                elif table.cell(0, j).value == u'所属年级':
                                    degree.grade = value
                                elif table.cell(0, j).value == u'学制':
                                    degree.duration = value
                                elif table.cell(0, j).value == u'是否异动':
                                    degree.change = value
                                elif table.cell(0, j).value == u'学位':
                                    degree.degree_type = value
                                elif table.cell(0, j).value == u'是否留学生':
                                    degree.is_foreign = value
                                elif table.cell(0, j).value == u'是否有学籍':
                                    degree.is_candidate = value
                                elif table.cell(0, j).value == u'学生类别':
                                    degree.student_type = value
                                elif table.cell(0, j).value == u'经费办法':
                                    degree.expenditure_type = value
                                elif table.cell(0, j).value == u'交换时间/学校':
                                    degree.exchange_info = value
                                elif table.cell(0, j).value == u'大三年级学分绩及排名':
                                    degree.scores_rank = value
                                elif table.cell(0, j).value == u'二学位':
                                    second_degree.major_type = value
                                elif table.cell(0, j).value == u'二学位专业名':
                                    second_degree.major = value
                                elif table.cell(0, j).value == u'二学位单位内码':
                                    second_degree.department_num = value
                                elif table.cell(0, j).value == u'二学位单位简称':
                                    second_degree.department_name = value
                                elif table.cell(0, j).value == u'二学位专业号':
                                    second_degree.major_num = value
                                elif table.cell(0, j).value == u'二学位班号':
                                    second_degree.class_num = value
                                elif table.cell(0, j).value == u'二学位毕业日期':
                                    if value == '':
                                        second_degree.date = None
                                    else:
                                        second_degree.date = datetime.datetime.strptime(str(int(value)), "%Y%m%d")
                                elif table.cell(0, j).value == u'毕业日期':
                                    if value == '':
                                        graduation.date = None
                                    else:
                                        graduation.date = datetime.datetime.strptime(str(int(value)), "%Y%m%d")
                                elif table.cell(0, j).value == u'毕业类别':
                                    graduation.type = value
                                elif table.cell(0, j).value == u'毕业手机':
                                    graduation.phone = int(value)
                                elif table.cell(0, j).value == u'毕业邮箱':
                                    graduation.email = value
                                elif table.cell(0, j).value == u'毕业去向':
                                    graduation.destination = value
                                elif table.cell(0, j).value == u'分流方向':
                                    graduation.direction = value
                        except Exception, e:
                            error_msg = u'导入文件错误，错误位置(%d, %d)' %(i, j)
                            return render_to_response("manage/error.html", {
                                "error_msg": error_msg
                            }, context_instance=RequestContext(request))

                    if len(User.objects.filter(username=str(std_num))) == 0:
                        user = User.objects.create(username=str(std_num))
                        user.set_password(str(std_num))
                        student.user = user
                    graduation.save()
                    degree.save()
                    second_degree.save()
                    student.graduation = graduation
                    student.degree = degree
                    student.second_degree = second_degree
                    student.save()

                except ValueError:
                    error_msg = u'导入文件错误！'
                    return render_to_response("manage/error.html", {
                        "error_msg": error_msg
                    }, context_instance=RequestContext(request))
            return render_to_response("manage/import_excel.html", {}, context_instance=RequestContext(request))
        else:
            error_msg = '导入 Excel 文件格式错误！'
            return render_to_response("manage/error.html", {
                "error_msg": error_msg
            }, context_instance=RequestContext(request))
    else:
        return render_to_response("manage/import_excel.html", {}, context_instance=RequestContext(request))
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
import xlwt
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
    if request.method == 'POST':
        info = request.REQUEST.getlist('info')
        if info != []:
            font0 = xlwt.Font()
            font0.name = 'Bold Figure'
            font0.bold = True
            alignment0 = xlwt.Alignment()
            alignment0.horz = xlwt.Alignment.HORZ_CENTER
            alignment0.vert = xlwt.Alignment.VERT_CENTER
            style0 = xlwt.XFStyle()
            style0.font = font0
            style0.alignment = alignment0
            data1 = []
            data = []
            column = 0
            book = xlwt.Workbook(encoding='utf-8')
            sheet = book.add_sheet('untitled')
            student = Student.objects.all()
            degreeInfo = DegreeInfo.objects.all()
            graduation = GraduationInfo.objects.all()
            secondDegree = SecondDegree.objects.all()
            familyInfo = FamilyInfo.objects.all()
            scholarship = Scholarship.objects.all()
            loan = Loan.objects.all()
            competition = Competition.objects.all()
            socialWork = SocialWork.objects.all()
            for m in range(len(info)):
                if info[m] == u'基本信息':
                    sheet.write(0, column + 0, "学号", style0)
                    sheet.write(0, column + 1, "姓名", style0)
                    sheet.write(0, column + 2, "系所名", style0)
                    sheet.write(0, column + 3, "专业名", style0)
                    sheet.write(0, column + 4, "教学班", style0)
                    sheet.write(0, column + 5, "所属年级", style0)
                    sheet.write(0, column + 6, "性别", style0)
                    sheet.write(0, column + 7, "身份证号", style0)
                    sheet.write(0, column + 8, "出生日期", style0)
                    sheet.write(0, column + 9, "民族", style0)
                    sheet.write(0, column + 10, "国籍", style0)
                    sheet.write(0, column + 11, "政治面貌", style0)
                    sheet.write(0, column + 12, "考区", style0)
                    sheet.write(0, column + 13, "毕业中学", style0)
                    sheet.write(0, column + 14, "高考总分", style0)
                    column = column + 14
                    for i in student.values():
                        data1.append(i["number"])
                        data1.append(i["name"])
                        data.append(data1)
                        data1 = []
                    for i in degreeInfo.values():
                        data1.append(i["department"])
                        data1.append(i["major"])
                        data1.append(i["class_num"])
                        data1.append(i["grade"])
                        data.append(data1)
                        data1 = []
                    for i in student.values():
                        data1.append(i["gender"])
                        data1.append(i["identity_number"])
                        data1.append(i["birthday"])
                        data1.append(i["nation"])
                        data1.append(i["nationality"])
                        data1.append(i["politics"])
                        data1.append(i["exam_province"])
                        data1.append(i["high_school"])
                        data1.append(i["entrance_exam_score"])
                        data.append(data1)
                        data1 = []
                elif info[m] == u'学籍信息' :
                    if column == 0:
                        sheet.write(0, column, "学号", style0)
                        for i in student.values():
                            data1.append(i["number"])
                            data.append(data1)
                            data1 = []
                    sheet.write(0, column + 1, "入学年级", style0)
                    sheet.write(0, column + 2, "学制", style0)
                    sheet.write(0, column + 3, "是否异动", style0)
                    sheet.write(0, column + 4, "学位", style0)
                    sheet.write(0, column + 5, "是否留学生", style0)
                    sheet.write(0, column + 6, "是否参加过交换", style0)
                    sheet.write(0, column + 7, "交换时间/学校", style0)
                    sheet.write(0, column + 8, "毕业日期", style0)
                    sheet.write(0, column + 9, "毕业类别", style0)
                    sheet.write(0, column + 10, "分流方向", style0)
                    sheet.write(0, column + 11, "二学位", style0)
                    sheet.write(0, column + 12, "二学位单位内码", style0)
                    sheet.write(0, column + 13, "二学位专业号", style0)
                    sheet.write(0, column + 14, "二学位班号", style0)
                    sheet.write(0, column + 15, "二学位单位简称", style0)
                    sheet.write(0, column + 16, "二学位专业名", style0)
                    #sheet.write(0, column + 17, "补行毕业时间", style0)
                    #sheet.write(0, column + 18, "补行毕业类别", style0)
                    sheet.write(0, column + 17, "大三年级学分绩及排名", style0)
                    column += 17

                    for i in degreeInfo.values():
                        data1.append(i["grade"])
                        data1.append(i["duration"])
                        data1.append(i["change"])
                        data1.append(i["degree_type"])
                        data1.append(i["is_foreign"])
                        data1.append(i["is_candidate"])
                        data1.append(i["exchange_info"])
                        data.append(data1)
                        data1 = []
                    for i in graduation.values():
                        data1.append(i["date"])
                        data1.append(i["type"])
                        data1.append(i["direction"])
                        data.append(data1)
                        data1 = []
                    for i in secondDegree.values():
                        data1.append(i["major_type"])
                        data1.append(i["department_num"])
                        data1.append(i["major_num"])
                        data1.append(i["class_num"])
                        data1.append(i["department_name"])
                        data1.append(i["major"])
                        data.append(data1)
                        data1 = []
                    for i in degreeInfo.values():
                        data1.append(i["scores_rank"])
                        data.append(data1)
                        data1 = []
                elif info[m] == u'毕业信息':
                    if column == 0:
                        sheet.write(0, column, "学号", style0)
                        for i in student.values():
                            data1.append(i["number"])
                            data.append(data1)
                            data1 = []
                    sheet.write(0, column + 1, "毕业手机", style0)
                    sheet.write(0, column + 2, "毕业邮箱", style0)
                    sheet.write(0, column + 3, "毕业去向", style0)
                    column = column + 3
                    for i in graduation.values():
                        data1.append(i["phone"])
                        data1.append(i["email"])
                        data1.append(i["destination"])
                        data.append(data1)
                        data1 = []
                elif info[m] == u'家庭信息':
                    if column == 0:
                        sheet.write(0, column, "学号", style0)
                        for i in student.values():
                            data1.append(i["number"])
                            data.append(data1)
                            data1 = []
                    sheet.write(0, column + 1, "家庭住址", style0)
                    sheet.write(0, column + 2, "户口类别", style0)
                    sheet.write(0, column + 3, "家庭人月均收入", style0)
                    sheet.write(0, column + 4, "I值", style0)
                    sheet.write(0, column + 5, "贫困等级", style0)
                    sheet.write(0, column + 6, "经济情况说明", style0)
                    column = column + 6
                    for i in familyInfo.values():
                        data1.append(i["address"])
                        data1.append(i["hukou_type"])
                        data1.append(i["avg_income"])
                        data1.append(i["I_value"])
                        data1.append(i["poverty_degree"])
                        data1.append(i["detail"])
                        data.append(data1)
                        data1 = []
                elif info[m] == u'奖助贷信息':
                    if column == 0:
                        sheet.write(0, column, "学号", style0)
                        for i in student.values():
                            data1.append(i["number"])
                            data.append(data1)
                            data1 = []
                    sheet.write(0, column + 1, "奖学金学年度", style0)
                    sheet.write(0, column + 2, "奖项金额", style0)
                    sheet.write(0, column + 3, "贷款", style0)
                    column = column + 3
                    for i in scholarship.values():
                        data1.append(i["year"])
                        data1.append(i["amount"])
                        data.append(data1)
                        data1 = []
                    for i in loan.values():
                        data1.append(i["info"])
                        data.append(data1)
                        data1 = []
                elif info[m] == u'社工及科研信息':
                    if column == 0:
                        sheet.write(0, column, "学号", style0)
                        for i in student.values():
                            data1.append(i["number"])
                            data.append(data1)
                            data1 = []
                    sheet.write(0, column + 1, "科技赛事学年度", style0)
                    sheet.write(0, column + 2, "科技赛事名称", style0)
                    sheet.write(0, column + 3, "社工学年度", style0)
                    sheet.write(0, column + 4, "社会工作（学生干部情况）", style0)
                    column = column + 4
                    for i in competition.values():
                        data1.append(i["year"])
                        data1.append(i["name"])
                        data.append(data1)
                        data1 = []
                    for i in socialWork.values():
                        data1.append(i["year"])
                        data1.append(i["name"])
                        data.append(data1)
                        data1 = []
            for k in range(len(data)):
                for j in range(len(data[k])):
                    sheet.write(k+1,j,data[k][j])
            response = HttpResponse(mimetype='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename=学生信息表.xls'
            book.save(response)
            return response
        else :
            return render_to_response("manage/export_excel.html", {}, context_instance=RequestContext(request))
    else :
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
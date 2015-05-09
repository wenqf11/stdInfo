#coding: utf-8
__author__ = 'Qingfu Wen'
__email__ = 'thssvince@163.com'
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.db import transaction
from student.models import *
from manage.models import Staff
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
    u'户口类别',
    u'家庭人均月收入',
    u"I值",
    u'贫困等级',
    u'经济状况说明',
    u'毕业日期',
    u'毕业类别',
    u'毕业手机',
    u'毕业邮箱',
    u'毕业去向',
    u'分流方向',
    u'奖学金',
    u'助学金',
    u'贷款',
    u'临时借款',
    u'科技赛事',
    u'社会工作',
])


@login_required
def global_search(request):
    content = request.POST.get('search_content', '')
    students = Student.objects.filter(number=content)
    if len(students) == 0:
        students = Student.objects.filter(name__contains=content)
    return render_to_response("manage/degree.html", locals(), context_instance=RequestContext(request))


@login_required
def index(request):
    return search(request)


@login_required
def search(request):
    if request.method == 'GET':
        return render_to_response("manage/search.html", context_instance=RequestContext(request))
    else:
        students = Student.objects.all()
        if request.POST.get('number', ''):
            students = students.filter(number=request.POST.get('number', ''))
        if request.POST.get('name', ''):
            students = students.filter(name__contains=request.POST.get('name', ''))
        if request.POST.get('grade', ''):
            degreeinfos = DegreeInfo.objects.filter(grade=request.POST.get('grade', ''))
            students = students.filter(degree__in=degreeinfos)
        if request.POST.get('nation', ''):
            students = students.filter(nation=request.POST.get('nation', ''))
        if request.POST.get('politics', ''):
            students = students.filter(politics=request.POST.get('politics', ''))
        if request.POST.get('province', ''):
            students = students.filter(exam_province=request.POST.get('province', ''))
        if request.POST.get('is_foreign', ''):
            is_foreign = request.POST.get('is_foreign', '')
            degreeinfos = DegreeInfo.objects.filter(is_foreign=is_foreign)
            students = students.filter(degree__in=degreeinfos)
        if request.POST.get('hukou_type', ''):
            familyinfos = FamilyInfo.objects.filter(hukou_type=request.POST.get('hukou_type', ''))
            students = students.filter(family__in=familyinfos)
        if request.POST.get('poverty_degree', ''):
            familyinfos = FamilyInfo.objects.filter(poverty_degree=request.POST.get('poverty_degree', ''))
            students = students.filter(family__in=familyinfos)
        if request.POST.get('graduation_type', ''):
            graduationinfos = GraduationInfo.objects.filter(type=request.POST.get('graduation_type', ''))
            students = students.filter(graduation__in=graduationinfos)
        if request.POST.get('graduation_year', ''):
            graduationinfos = GraduationInfo.objects.filter(date__year=request.POST.get('graduation_year', ''))
            students = students.filter(graduation__in=graduationinfos)
        if request.POST.get('graduation_direction', ''):
            graduationinfos = GraduationInfo.objects.filter(direction=request.POST.get('graduation_direction', ''))
            students = students.filter(graduation__in=graduationinfos)


        basic_info = False
        degree_info = False
        award_info = False
        family_info = False
        experience_info = False
        graduation_info = False
        if request.POST.get('basic_info', ''):
            basic_info = True
        if request.POST.get('degree_info', ''):
            degree_info = True
        if request.POST.get('award_info', ''):
            award_info = True
        if request.POST.get('family_info', ''):
            family_info = True
        if request.POST.get('experience_info', ''):
            experience_info = True
        if request.POST.get('graduation_info', ''):
            graduation_info = True


        return render_to_response("manage/search.html", {
            'students': students,
            'basic_info': basic_info,
            'degree_info': degree_info,
            'award_info': award_info,
            'family_info': family_info,
            'experience_info': experience_info,
            'graduation_info': graduation_info
        }, context_instance=RequestContext(request))


@login_required
@csrf_exempt
def update_search_result(request):
    id = request.POST.get('id', '')
    birthday = request.POST.get('birthday', '')
    second_date = request.POST.get('second_date', '')
    date = request.POST.get('graduation_date', '')

    student = Student.objects.get(id=id)
    student.number = request.POST.get('number', '')
    student.name = request.POST.get('name', '')
    student.phone = request.POST.get('phone', '')
    student.email = request.POST.get('email', '')
    student.gender = request.POST.get('gender', '')
    student.identity_number = request.POST.get('identity_number', '')
    if len(birthday) == 8:
        student.birthday = datetime.datetime.strptime(birthday, "%Y%m%d")
    student.nation = request.POST.get('nation', '')
    student.nationality = request.POST.get('nationality', '')
    student.politics = request.POST.get('politics', '')
    student.high_school = request.POST.get('high_school', '')
    student.exam_province = request.POST.get('exam_province', '')
    student.entrance_exam_score = request.POST.get('entrance_exam_score', '')

    student.degree.major = request.POST.get('major', '')
    student.degree.class_num = request.POST.get('class_num', '')
    student.degree.grade = request.POST.get('grade', '')
    student.degree.change = request.POST.get('change', '')
    student.degree.degree_type = request.POST.get('degree_type', '')
    student.degree.is_foreign = request.POST.get('is_foreign', '')
    student.degree.exchange_info = request.POST.get('exchange_info', '')
    student.degree.scores_rank = request.POST.get('scores_rank', '')
    student.degree.english_level = request.POST.get('english_level', '')
    student.second_degree.major = request.POST.get('second_major', '')
    student.second_degree.department_name = request.POST.get('second_department', '')
    if len(second_date) == 8:
        student.second_degree.date = datetime.datetime.strptime(second_date, "%Y%m%d")
    student.degree.save()
    student.second_degree.save()

    student.scholarship_loan.scholarship = request.POST.get('scholarship', '')
    student.scholarship_loan.loan = request.POST.get('loan', '')
    student.scholarship_loan.grant = request.POST.get('grant', '')
    student.scholarship_loan.temp_loan = request.POST.get('temp_loan', '')
    student.scholarship_loan.save()

    student.family.address = request.POST.get('address', '')
    student.family.phone = request.POST.get('family_phone', '')
    student.family.hukou_type = request.POST.get('hukou_type', '')
    try:
        student.family.avg_income = float(request.POST.get('avg_income', ''))
        student.family.I_value = float( request.POST.get('I_value', ''))
    except:
        pass
    student.family.poverty_degree = request.POST.get('poverty_degree', '')
    student.family.detail = request.POST.get('detail', '')
    student.family.save()

    student.experience.competition = request.POST.get('competition', '')
    student.experience.social_work = request.POST.get('social_work', '')
    student.experience.save()

    if len(date) == 8:
        student.graduation.date = datetime.datetime.strptime(date, "%Y%m%d")
    student.graduation.type = request.POST.get('graduation_type', '')
    student.graduation.phone = request.POST.get('graduation_phone', '')
    student.graduation.email = request.POST.get('graduation_email', '')
    student.graduation.destination = request.POST.get('destination', '')
    student.graduation.direction = request.POST.get('direction', '')
    student.graduation.save()

    student.save()
    return HttpResponse('OK')


@login_required
def get_basic_info(request):
    today = datetime.date.today()
    if today.month > 7:
        start_year = today.year - 3
    else:
        start_year = today.year - 4
    degreeinfos = DegreeInfo.objects.filter(grade__gte=start_year)

    students = Student.objects.filter(degree__in=degreeinfos)
    return render_to_response("manage/basic_info.html", {'students': students}, context_instance=RequestContext(request))


@login_required
@csrf_exempt
def update_basic_info(request):
    id = request.POST.get('id', '')
    number = request.POST.get('number', '')
    name = request.POST.get('name', '')
    gender = request.POST.get('gender', '')
    phone = request.POST.get('phone', '')
    email = request.POST.get('email', '')
    identity_number = request.POST.get('identity_number', '')
    birthday = request.POST.get('birthday', '')
    nation = request.POST.get('nation', '')
    nationality = request.POST.get('nationality', '')
    politics = request.POST.get('politics', '')
    high_school = request.POST.get('high_school', '')
    exam_province = request.POST.get('exam_province', '')
    entrance_exam_score = request.POST.get('entrance_exam_score', '')
    student = Student.objects.get(id=id)
    student.number = number
    student.name = name
    student.phone = phone
    student.email = email
    student.gender = gender
    student.identity_number = identity_number
    if len(birthday) == 8:
        student.birthday = datetime.datetime.strptime(birthday, "%Y%m%d")
    student.nation = nation
    student.nationality = nationality
    student.politics = politics
    student.high_school = high_school
    student.exam_province = exam_province
    student.entrance_exam_score = entrance_exam_score
    student.save()
    return HttpResponse('OK')


@login_required
def get_degree_info(request):
    today = datetime.date.today()
    if today.month > 7:
        start_year = today.year - 3
    else:
        start_year = today.year - 4
    degreeinfos = DegreeInfo.objects.filter(grade__gte=start_year)

    students = Student.objects.filter(degree__in=degreeinfos)
    return render_to_response("manage/degree.html", {'students': students}, context_instance=RequestContext(request))


@login_required
@csrf_exempt
def update_degree_info(request):
    id = request.POST.get('id', '')
    number = request.POST.get('number', '')
    name = request.POST.get('name', '')
    major = request.POST.get('major', '')
    class_num = request.POST.get('class_num', '')
    grade = request.POST.get('grade', '')
    change = request.POST.get('change', '')
    degree_type = request.POST.get('degree_type', '')
    is_foreign = request.POST.get('is_foreign', '')
    exchange_info = request.POST.get('exchange_info', '')
    english_level = request.POST.get('english_level', '')
    scores_rank = request.POST.get('scores_rank', '')
    second_major = request.POST.get('second_major', '')
    second_department = request.POST.get('second_department', '')
    second_date = request.POST.get('second_date', '')
    student = Student.objects.get(id=id)
    student.number = number
    student.name = name
    student.degree.major = major
    student.degree.class_num = class_num
    student.degree.grade = grade
    student.degree.change = change
    student.degree.degree_type = degree_type
    student.degree.is_foreign = is_foreign
    student.degree.exchange_info = exchange_info
    student.degree.scores_rank = scores_rank
    student.degree.english_level = english_level
    student.second_degree.major = second_major
    student.second_degree.department_name = second_department
    if len(second_date) == 8:
        student.second_degree.date = datetime.datetime.strptime(second_date, "%Y%m%d")
    student.degree.save()
    student.second_degree.save()
    student.save()
    return HttpResponse('OK')


@login_required
def get_award_info(request):
    today = datetime.date.today()
    if today.month > 7:
        start_year = today.year - 3
    else:
        start_year = today.year - 4
    degreeinfos = DegreeInfo.objects.filter(grade__gte=start_year)

    students = Student.objects.filter(degree__in=degreeinfos)
    return render_to_response("manage/award.html", {'students': students}, context_instance=RequestContext(request))


@login_required
@csrf_exempt
def update_award_info(request):
    id = request.POST.get('id', '')
    number = request.POST.get('number', '')
    name = request.POST.get('name', '')
    scholarship = request.POST.get('scholarship', '')
    loan = request.POST.get('loan', '')
    temp_loan = request.POST.get('temp_loan', '')
    grant = request.POST.get('grant', '')

    student = Student.objects.get(id=id)
    student.number = number
    student.name = name
    student.scholarship_loan.scholarship = scholarship
    student.scholarship_loan.loan = loan
    student.scholarship_loan.grant = grant
    student.scholarship_loan.temp_loan = temp_loan
    student.scholarship_loan.save()
    student.save()
    return HttpResponse('OK')


@login_required
def get_family_info(request):
    today = datetime.date.today()
    if today.month > 7:
        start_year = today.year - 3
    else:
        start_year = today.year - 4
    degreeinfos = DegreeInfo.objects.filter(grade__gte=start_year)

    students = Student.objects.filter(degree__in=degreeinfos)
    return render_to_response("manage/family.html", {'students': students}, context_instance=RequestContext(request))


@login_required
@csrf_exempt
def update_family_info(request):
    id = request.POST.get('id', '')
    number = request.POST.get('number', '')
    name = request.POST.get('name', '')
    address = request.POST.get('address', '')
    phone = request.POST.get('phone', '')
    hukou_type = request.POST.get('hukou_type', '')
    avg_income = request.POST.get('avg_income', '')
    I_value = request.POST.get('I_value', '')
    poverty_degree = request.POST.get('poverty_degree', '')
    detail = request.POST.get('detail', '')
    student = Student.objects.get(id=id)
    student.number = number
    student.name = name
    student.family.address = address
    student.family.phone = phone
    student.family.hukou_type = hukou_type
    try:
        student.family.avg_income = float(avg_income)
        student.family.I_value = float(I_value)
    except:
        pass
    student.family.poverty_degree = poverty_degree
    student.family.detail = detail
    student.family.save()
    student.save()
    return HttpResponse('OK')


@login_required
def get_experience_info(request):
    today = datetime.date.today()
    if today.month > 7:
        start_year = today.year - 3
    else:
        start_year = today.year - 4
    degreeinfos = DegreeInfo.objects.filter(grade__gte=start_year)

    students = Student.objects.filter(degree__in=degreeinfos)
    return render_to_response("manage/experience.html", {'students': students}, context_instance=RequestContext(request))

@login_required
@csrf_exempt
def update_experience_info(request):
    id = request.POST.get('id', '')
    number = request.POST.get('number', '')
    name = request.POST.get('name', '')
    competition = request.POST.get('competition', '')
    social_work = request.POST.get('social_work', '')
    student = Student.objects.get(id=id)
    student.number = number
    student.name = name
    student.experience.competition = competition
    student.experience.social_work = social_work
    student.experience.save()
    student.save()
    return HttpResponse('OK')


@login_required
def get_graduation_info(request):
    today = datetime.date.today()
    if today.month > 7:
        start_year = today.year - 3
    else:
        start_year = today.year - 4
    degreeinfos = DegreeInfo.objects.filter(grade__lt=start_year).exclude(grade__lt=start_year-2)

    students = Student.objects.filter(degree__in=degreeinfos)
    return render_to_response("manage/graduation.html",  {'students': students}, context_instance=RequestContext(request))


@login_required
@csrf_exempt
def update_graduation_info(request):
    id = request.POST.get('id', '')
    number = request.POST.get('number', '')
    name = request.POST.get('name', '')
    date = request.POST.get('date', '')
    type = request.POST.get('type', '')
    phone = request.POST.get('phone', '')
    email = request.POST.get('email', '')
    destination = request.POST.get('destination', '')
    direction = request.POST.get('direction', '')
    student = Student.objects.get(id=id)
    student.number = number
    student.name = name
    if len(date) == 8:
        student.graduation.date = datetime.datetime.strptime(date, "%Y%m%d")
    student.graduation.type = type
    student.graduation.phone = phone
    student.graduation.email = email
    student.graduation.destination = destination
    student.graduation.direction = direction
    student.graduation.save()
    student.save()
    return HttpResponse('OK')


@login_required
def get_detail(request, id):
    students = Student.objects.filter(id=id)
    if len(students) == 0:
        student = None
    else:
        student = students[0]
    return render_to_response("manage/detail.html", {'student': student}, context_instance=RequestContext(request))


@login_required
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
            style1 = xlwt.XFStyle()
            styleDate = xlwt.XFStyle()

            styleDate.num_format_str = 'YYYY-MM-DD'
            styleDate.font.name = 'Times New Roman'
            styleDate.alignment = alignment0
            style0.font = font0
            style0.alignment = alignment0
            style1.alignment = alignment0
            data1 = []
            data = []
            column = 0
            book = xlwt.Workbook(encoding='utf-8')
            sheet = book.add_sheet('untitled', cell_overwrite_ok = True)
            sheet.col(0).width = 256*13

            student = Student.objects.all()
            degreeInfo = DegreeInfo.objects.all()
            graduation = GraduationInfo.objects.all()
            secondDegree = SecondDegree.objects.all()
            familyInfo = FamilyInfo.objects.all()

            for m in range(len(info)):
                if info[m] == u'基本信息':
                    sheetCol = column
                    sheet.write(0, column + 0, "学号", style0)
                    sheet.write(0, column + 1, "姓名", style0)
                    sheet.write(0, column + 2, "性别", style0)
                    sheet.write(0, column + 3, "身份证号", style0)
                    sheet.write(0, column + 4, "出生日期", style0)
                    sheet.write(0, column + 5, "民族", style0)
                    sheet.write(0, column + 6, "国籍", style0)
                    sheet.write(0, column + 7, "政治面貌", style0)
                    sheet.write(0, column + 8, "考区", style0)
                    sheet.write(0, column + 9, "毕业中学", style0)
                    sheet.write(0, column + 10, "高考总分", style0)

                    sheet.col(column + 3).width = 256*12
                    sheet.col(column + 7).width = 256*20
                    sheet.col(column + 8).width = 256*12
                    sheet.col(column + 13).width = 256*30

                    for i in student.values():
                        data1.append(i["number"])
                        data1.append(i["name"])
                        data.append(data1)
                        data1 = []
                    for k in range(len(data)):
                        for j in range(len(data[k])):
                            sheet.write(k+1,j + sheetCol,data[k][j])
                    sheetCol = column + 2
                    data = []

                    for k in range(len(data)):
                        for j in range(len(data[k])):
                            sheet.write(k+1,j + sheetCol,data[k][j], style1)

                    sheetCol += 1

                    for i in student.values():
                        sheet.write(i["id"], -1 + sheetCol,i["gender"], style1)
                        sheet.write(i["id"], 0 + sheetCol,i["identity_number"], style1)
                        sheet.write(i["id"], 1 + sheetCol,i["birthday"], styleDate)
                        sheet.write(i["id"], 2 + sheetCol,i["nation"], style1)
                        sheet.write(i["id"], 3 + sheetCol,i["nationality"], style1)
                        sheet.write(i["id"], 4 + sheetCol,i["politics"], style1)
                        sheet.write(i["id"], 5 + sheetCol,i["exam_province"], style1)
                        sheet.write(i["id"], 6 + sheetCol,i["high_school"], style1)
                        sheet.write(i["id"], 7 + sheetCol,i["entrance_exam_score"], style1)


                    data = []

                    column = 14


                elif info[m] == u'学籍信息' :
                    sheetCol = column + 1
                    if column == 0:
                        sheet.write(0, column, "学号", style0)
                        for i in student.values():
                            data1.append(i["number"])
                            data.append(data1)
                            data1 = []
                        for k in range(len(data)):
                            for j in range(len(data[k])):
                                sheet.write(k+1,j,data[k][j], style1)
                        sheetCol = column + 1
                        data = []


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

                    sheet.col(column + 3).width = 256*65
                    sheet.col(column + 5).width = 256*12
                    sheet.col(column + 6).width = 256*17
                    sheet.col(column + 7).width = 256*15
                    sheet.col(column + 12).width = 256*17
                    sheet.col(column + 13).width = 256*15
                    sheet.col(column + 14).width = 256*12
                    sheet.col(column + 15).width = 256*17
                    sheet.col(column + 16).width = 256*40
                    sheet.col(column + 17).width = 256*22



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
                    for k in range(len(data)):
                        for j in range(len(data[k])):
                            sheet.write(k+1,j + sheetCol,data[k][j], style1)
                    sheetCol = column + 8
                    data = []

                    for i in graduation.values():
                        sheet.write(i["id"],sheetCol,i["date"], styleDate)
                        sheet.write(i["id"],sheetCol + 1,i["type"], style1)
                        sheet.write(i["id"],sheetCol + 2,i["direction"], style1)
                        data1.append(i["type"])

                    sheetCol = column + 11
                    data = []

                    for i in secondDegree.values():
                        data1.append(i["major_type"])
                        data1.append(i["department_num"])
                        data1.append(i["major_num"])
                        data1.append(i["class_num"])
                        data1.append(i["department_name"])
                        data1.append(i["major"])
                        data.append(data1)
                        data1 = []
                    for k in range(len(data)):
                        for j in range(len(data[k])):
                            sheet.write(k+1,j + sheetCol,data[k][j])
                    sheetCol = column + 17
                    data = []

                    for i in degreeInfo.values():
                        data1.append(i["scores_rank"])
                        data.append(data1)
                        data1 = []
                    for k in range(len(data)):
                        for j in range(len(data[k])):
                            sheet.write(k+1,j + sheetCol,data[k][j])
                    data = []

                    column += 17


                elif info[m] == u'毕业信息':
                    sheetCol = column + 1
                    if column == 0:
                        sheet.write(0, column, "学号", style0)
                        for i in student.values():
                            data1.append(i["number"])
                            data.append(data1)
                            data1 = []
                        for k in range(len(data)):
                            for j in range(len(data[k])):
                                sheet.write(k+1,j,data[k][j])
                        sheetCol = column + 1
                        data = []

                    sheet.write(0, column + 1, "毕业手机", style0)
                    sheet.write(0, column + 2, "毕业邮箱", style0)
                    sheet.write(0, column + 3, "毕业去向", style0)

                    sheet.col(column + 1).width = 256*13
                    sheet.col(column + 2).width = 256*25
                    sheet.col(column + 3).width = 256*50


                    for i in graduation.values():
                        data1.append(i["phone"])
                        data1.append(i["email"])
                        data1.append(i["destination"])
                        data.append(data1)
                        data1 = []
                    for k in range(len(data)):
                        for j in range(len(data[k])):
                            sheet.write(k+1,j + sheetCol,data[k][j])
                    data = []

                    column += 3


                elif info[m] == u'家庭信息':
                    sheetCol = column + 1
                    if column == 0:
                        sheet.write(0, column, "学号", style0)
                        for i in student.values():
                            data1.append(i["number"])
                            data.append(data1)
                            data1 = []
                        for k in range(len(data)):
                            for j in range(len(data[k])):
                                sheet.write(k+1,j,data[k][j])
                        sheetCol = column + 1
                        data = []

                    sheet.write(0, column + 1, "家庭住址", style0)
                    sheet.write(0, column + 2, "户口类别", style0)
                    sheet.write(0, column + 3, "家庭人月均收入", style0)
                    sheet.write(0, column + 4, "I值", style0)
                    sheet.write(0, column + 5, "贫困等级", style0)
                    sheet.write(0, column + 6, "经济情况说明", style0)

                    sheet.col(column + 1).width = 256*55
                    sheet.col(column + 2).width = 256*13
                    sheet.col(column + 3).width = 256*17
                    sheet.col(column + 6).width = 256*250


                    for i in familyInfo.values():
                        data1.append(i["address"])
                        data1.append(i["hukou_type"])
                        data1.append(i["avg_income"])
                        data1.append(i["I_value"])
                        data1.append(i["poverty_degree"])
                        data1.append(i["detail"])
                        data.append(data1)
                        data1 = []
                    for k in range(len(data)):
                        for j in range(len(data[k])):
                            sheet.write(k+1,j + sheetCol,data[k][j])
                    data = []

                    column += 6

                elif info[m] == u'奖助贷信息':
                    sheetCol = column + 1
                    if column == 0:
                        sheet.write(0, column, "学号", style0)
                        for i in student.values():
                            data1.append(i["number"])
                            data.append(data1)
                            data1 = []
                        for k in range(len(data)):
                            for j in range(len(data[k])):
                                sheet.write(k+1,j,data[k][j])
                        sheetCol = column + 1
                        data = []

                    sheet.write(0, column + 1, "奖学金学年度", style0)
                    sheet.write(0, column + 2, "荣誉等级", style0)
                    sheet.write(0, column + 3, "奖项简称", style0)
                    sheet.write(0, column + 4, "奖项金额", style0)
                    sheet.write(0, column + 5, "助学金学年度", style0)
                    sheet.write(0, column + 6, "助项简称", style0)
                    sheet.write(0, column + 7, "获助简称", style0)
                    sheet.write(0, column + 8, "贷款", style0)

                    sheet.col(column + 1).width = 256*15
                    sheet.col(column + 2).width = 256*20
                    sheet.col(column + 3).width = 256*14
                    sheet.col(column + 5).width = 256*15

                    for i in scholarship.values():
                        sheet.write(i["student_id"],sheetCol,i["year"])
                        sheet.write(i["student_id"],sheetCol + 1,i["honor_grade"])
                        sheet.write(i["student_id"],sheetCol + 2,i["name"])
                        sheet.write(i["student_id"],sheetCol + 3,i["amount"])
                    sheetCol = column + 4

                    for i in grant.values():
                        sheet.write(i["student_id"],sheetCol,i["year"])
                        sheet.write(i["student_id"],sheetCol + 1,i["name"])
                        sheet.write(i["student_id"],sheetCol + 2,i["amount"])
                    sheetCol = column + 7

                    for i in loan.values():
                        sheet.write(i["student_id"],sheetCol,i["info"])

                    column += 8


                elif info[m] == u'社工及科研信息':
                    sheetCol = column + 1
                    if column == 0:
                        sheet.write(0, column, "学号", style0)
                        for i in student.values():
                            data1.append(i["number"])
                            data.append(data1)
                            data1 = []
                        for k in range(len(data)):
                            for j in range(len(data[k])):
                                sheet.write(k+1,j,data[k][j])
                        sheetCol = column + 1
                        data = []

                    sheet.write(0, column + 1, "科技赛事学年度", style0)
                    sheet.write(0, column + 2, "科技赛事名称", style0)
                    sheet.write(0, column + 3, "社工学年度", style0)
                    sheet.write(0, column + 4, "社会工作（学生干部情况）", style0)

                    sheet.col(column + 1).width = 256*16
                    sheet.col(column + 2).width = 256*15
                    sheet.col(column + 3).width = 256*13
                    sheet.col(column + 4).width = 256*25

                    for i in competition.values():
                        data1.append(i["year"])
                        data1.append(i["name"])
                        data.append(data1)
                        data1 = []
                    for k in range(len(data)):
                        for j in range(len(data[k])):
                            sheet.write(k+1,j + sheetCol,data[k][j])
                    sheetCol = column + 2
                    data = []

                    for i in socialWork.values():
                        data1.append(i["year"])
                        data1.append(i["name"])
                        data.append(data1)
                        data1 = []
                    for k in range(len(data)):
                        for j in range(len(data[k])):
                            sheet.write(k+1,j + sheetCol,data[k][j])



            response = HttpResponse(mimetype='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename=学生信息表.xls'
            book.save(response)
            return response
        else :
            return render_to_response("manage/export_excel.html", {}, context_instance=RequestContext(request))
    else :
        return render_to_response("manage/export_excel.html", {}, context_instance=RequestContext(request))


def parse_data(request, excel_data):
    data = xlrd.open_workbook(file_contents=excel_data.read())
    table = data.sheets()[0]
    nrows = table.nrows
    ncols = table.ncols
    for i in xrange(1, nrows):
        std_num = table.cell(i, 0).value
        if isinstance(std_num, float):
            std_num = int(std_num)
        students = Student.objects.filter(number=std_num)

        if len(students) == 0:
            student = Student(number=std_num)
            degree = DegreeInfo()
            second_degree = SecondDegree()
            graduation = GraduationInfo()
            family_info = FamilyInfo()
            scholarship_loan = ScholarshipLoan()
            experience = Experience()
        else:
            student = students[0]
            if student.degree:
                degree = student.degree
            else:
                degree = DegreeInfo()
            if student.second_degree:
                second_degree = student.second_degree
            else:
                second_degree = SecondDegree()
            if student.graduation:
                graduation = student.graduation
            else:
                graduation = GraduationInfo()

            if student.family:
                family_info = student.family
            else:
                family_info = FamilyInfo()

            if student.scholarship_loan:
                scholarship_loan = student.scholarship_loan
            else:
                scholarship_loan = ScholarshipLoan()

            if student.experience:
                experience = student.experience
            else:
                experience = Experience()

        for j in xrange(1, ncols):
            try:
                if table.cell(0, j).value in basic_info_set:
                    value = table.cell(i, j).value
                    if table.cell(0, j).value == u'姓名':
                        student.name = value
                    elif table.cell(0, j).value == u'性别':
                        student.gender = value
                    elif table.cell(0, j).value == u'身份证号':
                        student.identity_number = value
                    elif table.cell(0, j).value == u'出生日期':
                        if value == '':
                            student.birthday = None
                        else:
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
                    elif table.cell(0, j).value == u'邮箱':
                        student.email = value
                    elif table.cell(0, j).value == u'手机号':
                        student.phone = value
                    elif table.cell(0, j).value == u'专业名':
                        degree.major = value
                    elif table.cell(0, j).value == u'教学班':
                        degree.class_num = value
                    elif table.cell(0, j).value == u'所属年级':
                        degree.grade = value
                    elif table.cell(0, j).value == u'是否异动':
                        degree.change = value
                    elif table.cell(0, j).value == u'学位':
                        degree.degree_type = value
                    elif table.cell(0, j).value == u'是否留学生':
                        degree.is_foreign = value
                    elif table.cell(0, j).value == u'交换时间/学校':
                        degree.exchange_info = value
                    elif table.cell(0, j).value == u'英语水平':
                        degree.english_level = value
                    elif table.cell(0, j).value == u'大三年级学分绩及排名':
                        degree.scores_rank = value
                    elif table.cell(0, j).value == u'二学位专业名':
                        second_degree.major = value
                    elif table.cell(0, j).value == u'二学位单位简称':
                        second_degree.department_name = value
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
                    elif table.cell(0, j).value == u'家庭住址':
                        family_info.address = value
                    elif table.cell(0, j).value == u'户口类别':
                        family_info.hukou_type = value
                    elif table.cell(0, j).value == u'家庭人均月收入':
                        if value:
                            family_info.avg_income = float(value)
                        else:
                            family_info.avg_income = 0
                    elif table.cell(0, j).value == u'I值':
                        if value:
                            family_info.I_value = float(value)
                        else:
                            family_info.I_value = 0
                    elif table.cell(0, j).value == u'贫困等级':
                        family_info.poverty_degree = value
                    elif table.cell(0, j).value == u'家庭电话':
                        family_info.phone = value
                    elif table.cell(0, j).value == u'经济状况说明':
                        family_info.detail = value
                    elif table.cell(0, j).value == u'奖学金':
                        scholarship_loan.scholarship = value
                    elif table.cell(0, j).value == u'助学金':
                        scholarship_loan.grant = value
                    elif table.cell(0, j).value == u'贷款':
                        scholarship_loan.loan = value
                    elif table.cell(0, j).value == u'临时借款':
                        scholarship_loan.temp_loan = value
                    elif table.cell(0, j).value == u'科技赛事':
                        experience.competition = value
                    elif table.cell(0, j).value == u'社会工作':
                        experience.social_work = value
            except Exception as e:
                error_msg = u'导入文件错误，错误位置(%d, %d)' %(i, j)
                return render_to_response("manage/error.html", {
                    "error_msg": error_msg
                }, context_instance=RequestContext(request))

        if len(User.objects.filter(username=std_num)) == 0:
            user = User.objects.create(username=std_num)
            user.set_password(std_num)
            user.save()
            student.user = user

        graduation.save()
        degree.save()
        second_degree.save()
        family_info.save()
        scholarship_loan.save()
        experience.save()

        student.graduation = graduation
        student.degree = degree
        student.second_degree = second_degree
        student.family = family_info
        student.scholarship_loan = scholarship_loan
        student.experience = experience
        student.save()
    return render_to_response("manage/import_excel.html", {}, context_instance=RequestContext(request))


def parse_data_ad(request, excel_data_ad):
    data = xlrd.open_workbook(file_contents=excel_data_ad.read())
    table = data.sheets()[0]
    nrows = table.nrows
    ncols = table.ncols
    for i in xrange(1, nrows):
        std_num = table.cell(i, 0).value
        if isinstance(std_num, float):
            std_num = int(std_num)
        students = Student.objects.filter(number=std_num)

        if len(students) == 0:
            student = Student(number=std_num)
            degree = DegreeInfo()
            second_degree = SecondDegree()
            graduation = GraduationInfo()
            family_info = FamilyInfo()
            scholarship_loan = ScholarshipLoan()
            experience = Experience()
        else:
            student = students[0]
            if student.degree:
                degree = student.degree
            else:
                degree = DegreeInfo()
            if student.second_degree:
                second_degree = student.second_degree
            else:
                second_degree = SecondDegree()
            if student.graduation:
                graduation = student.graduation
            else:
                graduation = GraduationInfo()

            if student.family:
                family_info = student.family
            else:
                family_info = FamilyInfo()

            if student.scholarship_loan:
                scholarship_loan = student.scholarship_loan
            else:
                scholarship_loan = ScholarshipLoan()

            if student.experience:
                experience = student.experience
            else:
                experience = Experience()

        for j in xrange(1, ncols):
            try:
                if table.cell(0, j).value in basic_info_set:
                    value = table.cell(i, j).value
                    if table.cell(0, j).value == u'奖学金':
                        if scholarship_loan.scholarship:
                            scholarship_loan.scholarship += '\r\n' + value
                        else:
                            scholarship_loan.scholarship = value
                    elif table.cell(0, j).value == u'助学金':
                        if scholarship_loan.grant:
                            scholarship_loan.grant += '\r\n' + value
                        else:
                            scholarship_loan.grant = value
                    elif table.cell(0, j).value == u'贷款':
                        if scholarship_loan.loan:
                            scholarship_loan.loan += u'\r\n' + value
                        else:
                            scholarship_loan.loan = value
                    elif table.cell(0, j).value == u'临时借款':
                        if scholarship_loan.temp_loan:
                            scholarship_loan.temp_loan += '\r\n' + value
                        else:
                            scholarship_loan.temp_loan = value
                    elif table.cell(0, j).value == u'科技赛事':
                        if experience.competition:
                            experience.competition += '\r\n' + value
                        else:
                            experience.competition = value
                    elif table.cell(0, j).value == u'社会工作':
                        if experience.social_work:
                            experience.social_work +=  u'\r\n' + value
                        else:
                            experience.social_work = value
            except Exception as e:
                error_msg = u'导入文件错误，错误位置(%d, %d)' %(i, j)
                return render_to_response("manage/error.html", {
                    "error_msg": error_msg
                }, context_instance=RequestContext(request))

        if len(User.objects.filter(username=std_num)) == 0:
            user = User.objects.create(username=std_num)
            user.set_password(std_num)
            user.save()
            student.user = user

        graduation.save()
        degree.save()
        second_degree.save()
        family_info.save()
        scholarship_loan.save()
        experience.save()

        student.graduation = graduation
        student.degree = degree
        student.second_degree = second_degree
        student.family = family_info
        student.scholarship_loan = scholarship_loan
        student.experience = experience
        student.save()
    return render_to_response("manage/import_excel.html", {}, context_instance=RequestContext(request))


@login_required
def import_excel(request):
    if request.method == 'POST':
        try:
            excel_data = request.FILES.get("excel_data")
            excel_data_ad = request.FILES.get("excel_data_ad")
            if excel_data is not None:
                return parse_data(request, excel_data)
            elif excel_data_ad is not None:
                return parse_data_ad(request, excel_data_ad)
        except Exception as e:
            error_msg = u'导入文件错误！%s' % e
            return render_to_response("manage/error.html", {
                "error_msg": error_msg
            }, context_instance=RequestContext(request))
    else:
        return render_to_response("manage/import_excel.html", {}, context_instance=RequestContext(request))


@login_required
@csrf_exempt
def delete_students(request):
    ids = request.POST.getlist("ids")
    for id in ids:
        student = Student.objects.get(id=id)
        student.degree.delete()
        student.second_degree.delete()
        student.scholarship_loan.delete()
        student.family.delete()
        student.experience.delete()
        student.graduation.delete()
        student.user.delete()
        student.delete()
    return HttpResponse("OK")


@login_required
def manage_user(request):
    users = User.objects.filter(is_staff=1).filter(is_active=1)
    staffs = Staff.objects.filter(user__in=users)
    return render_to_response("manage/user.html", {'staffs': staffs}, context_instance=RequestContext(request))


@login_required
@csrf_exempt
def add_staff(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    confirm_password = request.POST.get('confirm_password', '')
    name = request.POST.get('name', '')
    phone = request.POST.get('phone', '')
    email = request.POST.get('email', '')
    if len(User.objects.filter(username=username)) > 0:
        return HttpResponse("添加失败，用户名已存在！")
    elif password != confirm_password:
        return HttpResponse("添加失败，新密码不一致！")
    elif len(password) < 6:
        return HttpResponse("添加失败，密码太短！")

    try:
        with transaction.atomic():
            user = User(
                username=username,
                is_staff=1
            )
            user.set_password(password)
            user.save()
            staff = Staff(
                user=user,
                name=name,
                phone=phone,
                email=email,
            )
            staff.save()
    except:
        return HttpResponse("添加失败，保存到数据库出错！")
    else:
        return HttpResponse("添加成功！")


@login_required
@csrf_exempt
def update_staff(request):
    username = request.POST.get('username', '')
    name = request.POST.get('name', '')
    phone = request.POST.get('phone', '')
    email = request.POST.get('email', '')
    user = User.objects.get(username=username)
    staff = Staff.objects.get(user=user)
    staff.name = name
    staff.phone = phone
    staff.email = email
    staff.save()
    return HttpResponse("OK")


@login_required
@csrf_exempt
def delete_staffs(request):
    usernames = request.POST.getlist("usernames")
    for username in usernames:
        user = User.objects.get(username=username)
        if user.is_superuser == 0:
            user.is_active = 0
        user.save()
    return HttpResponse("OK")


@login_required
def get_profile(request):
    staff = Staff.objects.get(user=request.user)
    return render_to_response("manage/profile.html", {'staff': staff}, context_instance=RequestContext(request))


@login_required
def update_profile(request):
    name = request.POST.get("name", "")
    phone = request.POST.get("phone", "")
    email = request.POST.get("email", "")
    staff = Staff.objects.get(user=request.user)
    staff.name = name
    staff.phone = phone
    staff.email = email
    staff.save()
    return render_to_response("manage/profile.html", {'staff': staff}, context_instance=RequestContext(request))


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


@login_required
def reset_staff_psd(request):
    username = request.POST.get("username", "")
    new_password = request.POST.get("new_password", "")
    confirm_password = request.POST.get("confirm_password", "")

    if new_password != confirm_password:
        return HttpResponse("修改失败，新密码不一致！")
    elif len(new_password) < 6:
        return HttpResponse("修改失败，密码太短！")

    user = User.objects.get(username=username)
    if user is not None:
        user.set_password(new_password)
        user.save()
        return HttpResponse("密码修改成功！")
    else:
        return HttpResponse("修改失败！")
#coding: utf-8
__author__ = 'Qingfu Wen'
__email__ = 'thssvince@163.com'
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
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
    u'户口类别',
    u'家庭人均月收入（元）',
    u"I值",
    u'贫困等级',
    u'经济情况说明',
    u'毕业日期',
    u'毕业类别',
    u'毕业手机',
    u'毕业邮箱',
    u'毕业去向',
    u'分流方向',
    u'奖学金学年度',
    u'荣誉等级',
    u'奖项简称',
    u'获奖金额',
    u'助学金学年度',
    u'助项简称',
    u'获助金额',
    u'贷款',
    u'科技赛事学年度',
    u'科技赛事名称',
    u'社工学年度',
    u'社会工作（学生干部情况）',
])


def global_search(request):
    content = request.POST.get('search_content', '')
    students = Student.objects.filter(number=int(content))
    if len(students) == 0:
        students = Student.objects.filter(name=content)
    return render_to_response("manage/degree.html", locals(), context_instance=RequestContext(request))


def index(request):
    return search(request)


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
            is_foreign = True if request.POST.get('is_foreign', '') ==  u'是' else False
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
        work_info = False
        graduation_info = False
        if request.POST.get('basic_info', ''):
            basic_info = True
        if request.POST.get('degree_info', ''):
            degree_info = True
        if request.POST.get('award_info', ''):
            award_info = True
        if request.POST.get('family_info', ''):
            family_info = True
        if request.POST.get('work_info', ''):
            work_info = True
        if request.POST.get('graduation_info', ''):
            graduation_info = True

        return render_to_response("manage/search.html", {
            'students': students,
            'basic_info': basic_info,
            'degree_info': degree_info,
            'award_info': award_info,
            'family_info': family_info,
            'work_info': work_info,
            'graduation_info': graduation_info,
        }, context_instance=RequestContext(request))


def get_basic_info(request):
    students = Student.objects.all()
    return render_to_response("manage/manage.html", locals(), context_instance=RequestContext(request))


@csrf_exempt
def update_basic_info(request):
    id = request.POST.get('id', '')
    number = request.POST.get('number', '')
    name = request.POST.get('name', '')
    gender = request.POST.get('gender', '')
    identity_number = request.POST.get('identity_number', '')
    birthday = request.POST.get('birthday', '')
    nation = request.POST.get('nation', '')
    nationality = request.POST.get('nationality', '')
    politics = request.POST.get('politics', '')
    high_school = request.POST.get('high_school', '')
    exam_province = request.POST.get('exam_province', '')
    entrance_exam_score = request.POST.get('entrance_exam_score', '')
    student = Student.objects.get(id=id)
    student.number = int(number)
    student.name = name
    student.gender = True if gender == u'男' else False
    student.identity_number = identity_number
    student.birthday = datetime.datetime.strptime(birthday, "%Y-%m-%d")
    student.nation = nation
    student.nationality = nationality
    student.politics = politics
    student.high_school = high_school
    student.exam_province = exam_province
    student.entrance_exam_score = entrance_exam_score
    student.save()
    return HttpResponse('OK')


def get_degree_info(request):
    students = Student.objects.all()
    return render_to_response("manage/degree.html", locals(), context_instance=RequestContext(request))


@csrf_exempt
def update_degree_info(request):
    id = request.POST.get('id', '')
    number = request.POST.get('number', '')
    name = request.POST.get('name', '')
    department = request.POST.get('department', '')
    major = request.POST.get('major', '')
    class_num = request.POST.get('class_num', '')
    grade = request.POST.get('grade', '')
    duration = request.POST.get('duration', '')
    change = request.POST.get('change', '')
    degree_type = request.POST.get('degree_type', '')
    is_foreign = request.POST.get('is_foreign', '')
    is_candidate = request.POST.get('is_candidate', '')
    student_type = request.POST.get('student_type', '')
    expenditure_type = request.POST.get('expenditure_type', '')
    exchange_info = request.POST.get('exchange_info', '')
    scores_rank = request.POST.get('scores_rank', '')
    student = Student.objects.get(id=id)
    student.number = int(number)
    student.name = name
    student.degree.department = department
    student.degree.major = major
    student.degree.class_num = class_num
    student.degree.grade = grade
    student.degree.duration = int(duration)
    student.degree.change = change
    student.degree.degree_type = degree_type
    student.degree.is_foreign = True if is_foreign == u'是' else False
    student.degree.is_candidate = True if is_candidate == u'是' else False
    student.degree.student_type = student_type
    student.degree.expenditure_type = expenditure_type
    student.degree.exchange_info = exchange_info
    student.degree.scores_rank = scores_rank
    student.degree.save()
    student.save()
    return HttpResponse('OK')


def get_award_info(request):
    students = Student.objects.all()
    awards = list()
    for student in students:
        scholarships = Scholarship.objects.filter(student=student)
        grants = Grant.objects.filter(student=student)
        loans = Loan.objects.filter(student=student)
        award_scholarship = ''
        award_grant = ''
        award_loan = ''
        for scholarship in scholarships:
            award_scholarship += scholarship.year + ' ' + scholarship.honor_grade + ' ' + scholarship.name + ' ' + \
                                 str(scholarship.amount) + '\r\n'
        for grant in grants:
            award_grant += grant.year + ' ' + grant.name + ' ' + str(grant.amount) + '\r\n'

        for loan in loans:
            award_loan += loan.info + '\r\n'

        awards.append({
            'id': student.id,
            'number': student.number,
            'name': student.name,
            'scholarship': award_scholarship,
            'grant': award_grant,
            'loan': award_loan
        })
    return render_to_response("manage/award.html", {
        'awards' : awards
    }, context_instance=RequestContext(request))


def update_award_info(request):
    id = request.POST.get('id', '')
    number = request.POST.get('number', '')
    name = request.POST.get('name', '')
    address = request.POST.get('address', '')
    hukou_type = request.POST.get('hukou_type', '')
    avg_income = request.POST.get('avg_income', '')
    I_value = request.POST.get('I_value', '')
    poverty_degree = request.POST.get('poverty_degree', '')
    detail = request.POST.get('detail', '')
    student = Student.objects.get(id=id)
    student.number = int(number)
    student.name = name
    student.family.address = address
    student.family.hukou_type = hukou_type
    student.family.avg_income = float(avg_income)
    student.family.I_value = float(I_value)
    student.family.poverty_degree = poverty_degree
    student.family.detail = detail
    student.family.save()
    student.save()
    return HttpResponse('OK')


def get_family_info(request):
    students = Student.objects.all()
    return render_to_response("manage/family.html", locals(), context_instance=RequestContext(request))


@csrf_exempt
def update_family_info(request):
    id = request.POST.get('id', '')
    number = request.POST.get('number', '')
    name = request.POST.get('name', '')
    address = request.POST.get('address', '')
    hukou_type = request.POST.get('hukou_type', '')
    avg_income = request.POST.get('avg_income', '')
    I_value = request.POST.get('I_value', '')
    poverty_degree = request.POST.get('poverty_degree', '')
    detail = request.POST.get('detail', '')
    student = Student.objects.get(id=id)
    student.number = int(number)
    student.name = name
    student.family.address = address
    student.family.hukou_type = hukou_type
    student.family.avg_income = float(avg_income)
    student.family.I_value = float(I_value)
    student.family.poverty_degree = poverty_degree
    student.family.detail = detail
    student.family.save()
    student.save()
    return HttpResponse('OK')

def get_work_info(request):
    students = Student.objects.all()
    works = list()
    for student in students:
        competitions = Competition.objects.filter(student=student)
        social_works = SocialWork.objects.filter(student=student)
        work_competition = ''
        work_social_work = ''
        for competition in competitions:
            work_competition += competition.year + ' ' + competition.name + '\r\n'

        for social_work in social_works:
            work_social_work += social_work.name + '\r\n'

        works.append({
            'id': student.id,
            'number': student.number,
            'name': student.name,
            'competition': work_competition,
            'social_work': work_social_work
        })
    return render_to_response("manage/work.html", {
        'works' : works
    }, context_instance=RequestContext(request))


def get_graduation_info(request):
    students = Student.objects.all()
    return render_to_response("manage/graduation.html", locals(), context_instance=RequestContext(request))


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
    student.number = int(number)
    student.name = name
    student.graduation.date = datetime.datetime.strptime(date, "%Y-%m-%d")
    student.graduation.type = type
    student.graduation.phone = phone
    student.graduation.email = email
    student.graduation.destination = destination
    student.graduation.direction = direction
    student.graduation.save()
    student.save()
    return HttpResponse('OK')


def get_detail(request):
    return render_to_response("manage/detail.html", {}, context_instance=RequestContext(request))


def export_excel(request):
    return render_to_response("manage/export_excel.html", {}, context_instance=RequestContext(request))


def import_excel(request):
    if request.method == 'POST':
        try:
            basic_info = request.FILES['basic_info']
            data = xlrd.open_workbook(file_contents=basic_info.read())
            table = data.sheets()[0]
            nrows = table.nrows
            ncols = table.ncols
            for i in xrange(1, nrows):
                std_num = int(table.cell(i, 1).value)
                if len(str(std_num)) != 10:
                    raise ValueError('学号有误')
                students = Student.objects.filter(number=std_num)
                if len(students) == 0:
                    student = Student(number=std_num)
                    degree = DegreeInfo()
                    second_degree = SecondDegree()
                    graduation = GraduationInfo()
                    family_info = FamilyInfo()
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
                                if value == u'是':
                                    degree.is_foreign = True
                                else:
                                    degree.is_foreign = False
                            elif table.cell(0, j).value == u'是否有学籍':
                                if value == u'是':
                                    degree.is_candidate = True
                                else:
                                    degree.is_candidate = False
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
                            elif table.cell(0, j).value == u'家庭住址':
                                family_info.address = value
                            elif table.cell(0, j).value == u'户口类别':
                                family_info.hukou_type = value
                            elif table.cell(0, j).value == u'家庭人均月收入（元）':
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
                            elif table.cell(0, j).value == u'经济情况说明':
                                family_info.detail = value
                            elif table.cell(0, j).value == u'奖学金学年度':
                                scholarship = Scholarship(student=student)
                                scholarship.year = value
                            elif table.cell(0, j).value == u'荣誉等级':
                                scholarship.honor_grade = value
                            elif table.cell(0, j).value == u'奖项简称':
                                scholarship.name = value
                            elif table.cell(0, j).value == u'获奖金额':
                                scholarship.amount = int(value)
                                scholarship.save()
                            elif table.cell(0, j).value == u'助学金学年度':
                                grant = Grant(student=student)
                                grant.year = value
                            elif table.cell(0, j).value == u'助项简称':
                                grant.name = value
                            elif table.cell(0, j).value == u'获助金额':
                                grant.amount = int(value)
                                grant.save()
                            elif table.cell(0, j).value == u'贷款':
                                loan = Loan(student=student)
                                loan.info = value
                                loan.save()
                            elif table.cell(0, j).value == u'科技赛事学年度':
                                competition = Competition(student=student)
                                competition.year = value
                            elif table.cell(0, j).value == u'科技赛事名称':
                                competition.name = value
                                competition.save()
                            elif table.cell(0, j).value == u'社工学年度':
                                social_work = SocialWork(student=student)
                                social_work.year = value
                            elif table.cell(0, j).value == u'社会工作（学生干部情况）':
                                social_work.name = value
                                social_work.save()
                    except Exception as e:
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
                family_info.save()
                student.graduation = graduation
                student.degree = degree
                student.second_degree = second_degree
                student.family = family_info
                student.save()
            return render_to_response("manage/import_excel.html", {}, context_instance=RequestContext(request))
        except Exception as e:
            error_msg = u'导入文件错误！%s' % e
            return render_to_response("manage/error.html", {
                "error_msg": error_msg
            }, context_instance=RequestContext(request))
    else:
        return render_to_response("manage/import_excel.html", {}, context_instance=RequestContext(request))
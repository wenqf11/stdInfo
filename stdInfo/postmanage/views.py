#coding: utf-8
__author__ = 'Zichen Zhu'
__email__ = 'thssvince@163.com'
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from postgraduate.models import *
import datetime
import xlrd
import xlwt
basic_info_set = set([
    u'学号'
    ,u'姓名'
    ,u'性别'
    ,u'民族'
    ,u'政治面貌'
    ,u'导师'
    ,u'手机'
    ,u'邮箱'
    ,u'学位'
    ,u'招生途径'
    ,u'毕业前或推免前综合排名'
    ,u'入学成绩/排名'
    ,u'初试成绩'
    ,u'开题时间'
    ,u'交流学校/时间'
    ,u'本科毕业学校'
    ,u'本科专业'
    ,u'班号'
    ,u'毕业日期'
    ,u'毕业去向'
    ,u'职务'
    ,u'年薪'
    ,u'校友捐款'
    ,u'毕业手机'
    ,u'毕业邮箱'
    ,u'奖项代码'
    ,u'奖学金学年度'
    ,u'奖项名称'
    ,u'获奖金额'
    ,u'助项代码'
    ,u'助学金学年度'
    ,u'助项简称'
    ,u'获助金额'
    ,u'贷款'
    ,u'科技赛事学年度'
    ,u'科技赛事名称'
    ,u'社工学年度'
    ,u'社会工作（学生干部情况）',

])

def global_search(request):
    content = request.POST.get('search_content', '')
    students = Postgraduate.objects.filter(number=int(content))
    if len(students) == 0:
        students = Postgraduate.objects.filter(name=content)
    return render_to_response("", locals(), context_instance=RequestContext(request))


def index(request):
    return search(request)

def search(request):
    if request.method == 'GET':
        return render_to_response("postmanage/search.html", context_instance=RequestContext(request))
    else:
        students = Postgraduate.objects.all()
        if request.POST.get('number', ''):
            students = students.filter(number=request.POST.get('number', ''))
        if request.POST.get('name', ''):
            students = students.filter(name__contains=request.POST.get('name', ''))
        if request.POST.get('nation', ''):
            students = students.filter(nation=request.POST.get('nation', ''))
        if request.POST.get('politics', ''):
            students = students.filter(politics=request.POST.get('politics', ''))
        if request.POST.get('tutor', ''):
            students = students.filter(tutor=request.POST.get('tutor', ''))
        if request.POST.get('graduation_year', ''):
            graduationinfos = PostGraduationInfo.objects.filter(date__year=request.POST.get('graduation_year', ''))
            students = students.filter(graduation__in=graduationinfos)
        if request.POST.get('graduation_direction', ''):
            graduationinfos = PostGraduationInfo.objects.filter(direction=request.POST.get('graduation_direction', ''))
            students = students.filter(graduation__in=graduationinfos)

        basic_info = False
        degree_info = False
        award_info = False
        work_info = False
        graduation_info = False
        if request.POST.get('basic_info', ''):
            basic_info = True
        if request.POST.get('degree_info', ''):
            degree_info = True
        if request.POST.get('award_info', ''):
            award_info = True
        if request.POST.get('work_info', ''):
            work_info = True
        if request.POST.get('graduation_info', ''):
            graduation_info = True

        return render_to_response("postmanage/search.html", {
            'students': students,
            'basic_info': basic_info,
            'degree_info': degree_info,
            'award_info': award_info,
            'work_info': work_info,
            'graduation_info': graduation_info,
            }, context_instance=RequestContext(request))

def get_basic_info(request):
        students = Postgraduate.objects.filter(number__gte=2014000000)
        return render_to_response("postmanage/basic_info.html", locals(), context_instance=RequestContext(request))

@csrf_exempt
def update_basic_info(request):
    id = request.POST.get('id', '')
    number = request.POST.get('number', '')
    name = request.POST.get('name', '')
    gender = request.POST.get('gender', '')
    nation = request.POST.get('nation', '')
    politics = request.POST.get('politics', '')
    tutor = request.POST.get('tutor', '')
    phone = request.POST.get('phone', '')
    email = request.POST.get('email', '')
    student = Postgraduate.objects.get(id=id)
    student.number = int(number)
    student.name = name
    student.gender = gender
    student.nation = nation
    student.politics = politics
    student.tutor = tutor
    student.phone = phone
    student.email = email
    student.save()
    return HttpResponse('OK')


def get_degree_info(request):
    students = Postgraduate.objects.filter(number__gte=2014000000)
    return render_to_response("postmanage/degree.html", locals(), context_instance=RequestContext(request))

@csrf_exempt
def update_degree_info(request):
    id = request.POST.get('id', '')
    number = request.POST.get('number', '')
    name = request.POST.get('name', '')
    degree = request.POST.get('degree','')
    admissions_way = request.POST.get('admissions_way','')
    rank_before_graduation = request.POST.get('rank_before_graduation','')
    admissions_rank = request.POST.get('admissions_rank','')
    first_test = request.POST.get('first_test','')
    opening_time = request.POST.get('opening_time','')
    exchange_info = request.POST.get('exchange_info','')
    regular_school = request.POST.get('regular_school','')
    regular_major = request.POST.get('regular_major','')
    class_name = request.POST.get('class_name','')
    student = Postgraduate.objects.get(id=id)
    student.number = int(number)
    student.name = name
    student.degree.degree = degree
    student.degree.admissions_way = admissions_way
    student.degree.rank_before_graduation = rank_before_graduation
    student.degree.admissions_rank = admissions_rank
    student.degree.first_test = first_test
    student.degree.opening_time = opening_time
    student.degree.exchange_info = exchange_info
    student.degree.regular_school  = regular_school
    student.degree.regular_major = regular_major
    student.degree.class_name = class_name
    student.degree.save()
    student.save()
    return HttpResponse('OK')

def get_award_info(request):
    students = Postgraduate.objects.filter(number__gte=2014000000)
    awards = list()
    for student in students:
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

        awards.append({
            'id': student.id,
            'number': student.number,
            'name': student.name,
            'scholarship': award_scholarship,
            'grant': award_grant,
            'loan': award_loan
        })
    return render_to_response("postmanage/award.html", {
        'awards' : awards
    }, context_instance=RequestContext(request))

@csrf_exempt
def update_award_info(request):
    id = request.POST.get('id', '')
    number = request.POST.get('number', '')
    name = request.POST.get('name', '')
    scholarship_code = request.POST.get('scholarship_code','')
    scholarship_year = request.POST.get('scholarship_year','')
    scholarship_name = request.POST.get('scholarship_name','')
    scholarship_amount = request.POST.get('scholarship_amount','')
    grant_code = request.POST.get('grant_code','')
    grant_year = request.POST.get('grant_year','')
    grant_name = request.POST.get('grant_name','')
    grant_amount = request.POST.get('grant_amount','')
    loan_info = request.POST.get('loan','')
    student = Postgraduate.objects.get(id=id)
    student.number = int(number)
    student.name = name
    scholarship = Scholarship.objects.get(id=id)
    grant = Grant.objects.get(id=id)
    loan = Loan.objects.get(id=id)
    scholarship.code = scholarship_code
    scholarship.year = scholarship_year
    scholarship.name = scholarship_name
    scholarship.amount = scholarship_amount
    grant.code = grant_code
    grant.year = grant_year
    grant.name = grant_name
    grant.amount = grant_amount
    loan.info = loan_info
    loan.save()
    grant.save()
    scholarship.save()
    student.save()
    return HttpResponse('OK')

def get_work_info(request):
    students = Postgraduate.objects.filter(number__gte=2014000000)
    works = list()
    for student in students:
        competitions = Competition.objects.filter(student=student)
        social_works = SocialWork.objects.filter(student=student)
        work_competition = ''
        work_social_work = ''
        for competition in competitions:
            work_competition += competition.year + ' ' + competition.name + '\r\n'

        for social_work in social_works:
            work_social_work += social_work.year + ' ' + social_work.name + '\r\n'

        works.append({
            'id': student.id,
            'number': student.number,
            'name': student.name,
            'competition': work_competition,
            'social_work': work_social_work
        })
    return render_to_response("postmanage/work.html", {
        'works' : works
    }, context_instance=RequestContext(request))

def update_work_info(request):
    id = request.POST.get('id', '')
    number = request.POST.get('number', '')
    name = request.POST.get('name', '')
    socialwork_year = request.POST.get('socialwork_year','')
    socialwork_name = request.POST.get('socialwork_name','')
    competition_year = request.POST.get('competition_year','')
    competition_name = request.POST.get('competition_name','')
    student = Postgraduate.objects.get(id=id)
    student.number = number
    student.name = name
    socialwork = SocialWork.objects.get(id=id)
    competition = Competition.objects.get(id=id)
    socialwork.year = socialwork_year
    socialwork.name = socialwork_name
    competition.year = competition_year
    competition.name = competition_name
    competition.save()
    socialwork.save()
    student.save()

def get_graduation_info(request):
    students = Postgraduate.objects.filter(number__gte=2014000000)
    return render_to_response("postmanage/graduation.html", locals(), context_instance=RequestContext(request))

@csrf_exempt
def update_graduation_info(request):
    id = request.POST.get('id', '')
    number = request.POST.get('number', '')
    name = request.POST.get('name', '')
    date = request.POST.get('date', '')
    destination = request.POST.get('destination', '')
    job = request.POST.get('job','')
    salary = request.POST.get('salary','')
    alumni_donation = request.POST.get('alumni_donation','')
    phone = request.POST.get('phone', '')
    email = request.POST.get('email', '')
    student = Postgraduate.objects.get(id=id)
    student.number = int(number)
    student.name = name
    student.graduation.date = datetime.datetime.strptime(date, "%Y-%m-%d")
    student.graduation.destination = destination
    student.graduation.job = job
    student.graduation.salary = salary
    student.graduation.alumni_donation = alumni_donation
    student.graduation.phone = phone
    student.graduation.email = email
    student.graduation.save()
    student.save()
    return HttpResponse('OK')

def get_detail(request, id):
    student = Postgraduate.objects.get(id=id)

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

    return render_to_response("postmanage/detail.html", locals(), context_instance=RequestContext(request))


def import_excel(request):
    if request.method == 'POST':
        try:
            basic_info = request.FILES['basic_info']
            data = xlrd.open_workbook(file_contents=basic_info.read())
            table = data.sheets()[0]
            nrows = table.nrows
            ncols = table.ncols
            for i in xrange(1, nrows):
                std_num = int(table.cell(i, 0).value)
                if len(str(std_num)) != 10:
                    raise ValueError('学号有误')
                students = Postgraduate.objects.filter(number=std_num)
                if len(students) == 0:
                    student = Postgraduate(number=std_num)
                    degree = PostgraduateDegree()
                    graduation = PostGraduationInfo()
                    scholarship = Scholarship(student=student)
                    loan = Loan(student=student)
                    grant = Grant(student=student)
                    competition = Competition(student=student)
                    social_work = SocialWork(student=student)
                else:
                    student = students[0]
                    if student.degree:
                        degree = student.degree
                    else:
                        degree = PostgraduateDegree()
                    if student.graduation:
                        graduation = student.graduation
                    else:
                        graduation = PostGraduationInfo()
                    scholarship = Scholarship(student=student)
                    loan = Loan(student=student)
                    grant = Grant(student=student)
                    competition = Competition(student=student)
                    social_work = SocialWork(student=student)

                for j in xrange(1, ncols):
                    try:
                        if table.cell(0, j).value in basic_info_set:
                            value = table.cell(i, j).value
                            if value == '':
                                continue
                            if table.cell(0, j).value == u'姓名':
                                student.name = value
                            elif table.cell(0, j).value == u'性别':
                                student.gender = value
                            elif table.cell(0, j).value == u'民族':
                                student.nation = value
                            elif table.cell(0, j).value == u'政治面貌':
                                student.politics = value
                            elif table.cell(0, j).value == u'导师':
                                student.tutor = value
                            elif table.cell(0, j).value == u'手机':
                                student.phone = str(value)
                            elif table.cell(0, j).value == u'邮箱':
                                student.email = value
                            elif table.cell(0, j).value == u'学位':
                                degree.degree = value
                            elif table.cell(0, j).value == u'招生途径':
                                degree.admissions_way = value
                            elif table.cell(0, j).value == u'毕业前或推免前综合排名':
                                degree.rank_before_graduation = value
                            elif table.cell(0, j).value == u'入学成绩/排名':
                                degree.admissions_rank = value
                            elif table.cell(0, j).value == u'初试成绩':
                                degree.first_test = value
                            elif table.cell(0, j).value == u'开题时间':
                                #if value != '':
                                #    degree.opening_time = value
                                continue
                            elif table.cell(0, j).value == u'交流学校/时间':
                                degree.exchange_info = value
                            elif table.cell(0, j).value == u'本科毕业学校':
                                degree.regular_school = value
                            elif table.cell(0, j).value == u'本科专业':
                                degree.regular_major = value
                            elif table.cell(0, j).value == u'班号':
                                degree.class_name = value
                            elif table.cell(0, j).value == u'毕业日期':
                                graduation.date = value
                            elif table.cell(0, j).value == u'毕业去向':
                                graduation.destination = value
                            elif table.cell(0, j).value == u'职务':
                                graduation.job = value
                            elif table.cell(0, j).value == u'年薪':
                                graduation.salary = value
                            elif table.cell(0, j).value == u'校友捐款':
                                graduation.alumni_donation = value
                            elif table.cell(0, j).value == u'毕业手机':
                                graduation.phone = value
                            elif table.cell(0, j).value == u'毕业邮箱':
                                graduation.email = value
                            elif table.cell(0, j).value == u'奖项代码':
                                scholarship.code = value
                            elif table.cell(0, j).value == u'奖学金学年度':
                                scholarship.year = value
                            elif table.cell(0, j).value == u'奖项名称':
                                scholarship.name = value
                            elif table.cell(0, j).value == u'获奖金额':
                                scholarship.amount = int(value)
                                scholarship.save()
                            elif table.cell(0, j).value == u'助项代码':
                                grant.code = value
                            elif table.cell(0, j).value == u'助学金学年度':
                                grant.year = value
                            elif table.cell(0, j).value == u'助项简称':
                                grant.name = value
                            elif table.cell(0, j).value == u'获助金额':
                                grant.amount = int(value)
                                grant.save()
                            elif table.cell(0, j).value == u'贷款':
                                loan.info = value
                                loan.save()
                            elif table.cell(0, j).value == u'科技赛事学年度':
                                competition.year = value
                            elif table.cell(0, j).value == u'科技赛事名称':
                                competition.name = value
                                competition.save()
                            elif table.cell(0, j).value == u'社工学年度':
                                social_work.year = value
                            elif table.cell(0, j).value == u'社会工作（学生干部情况）':
                                social_work.name = value
                                social_work.save()
                    except Exception as e:
                        error_msg = u'导入文件错误，错误位置(%d, %d)' %(i, j)
                        return render_to_response("postmanage/error.html", {
                            "error_msg": error_msg
                        }, context_instance=RequestContext(request))

                if len(User.objects.filter(username=str(std_num))) == 0:
                    user = User.objects.create(username=str(std_num))
                    user.set_password(str(std_num))
                    student.user = user
                graduation.save()
                degree.save()
                student.graduation = graduation
                student.degree = degree
                student.save()
            return render_to_response("postmanage/import_excel.html", {}, context_instance=RequestContext(request))
        except Exception as e:
            error_msg = u'导入文件错误！%s' % e
            return render_to_response("postmanage/error.html", {
                "error_msg": error_msg
            }, context_instance=RequestContext(request))
    else:
        return render_to_response("postmanage/import_excel.html", {}, context_instance=RequestContext(request))



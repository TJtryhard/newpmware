import datetime
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
import requests
import json
from .models import Users, Projects, Announcement, KickOff, Milestones, Closure
from django.contrib.sessions.models import Session
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

###################### Login Page 登录页面


def start_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        result = sign_in(username, request)


        if result:
            response = redirect('navigation_page')
            response.set_cookie('pm',result.pm,expires=datetime.datetime.now()+datetime.timedelta(days=1),path='/')
            return response # 跳转到导航页面
        else:
            message = "Invalid user!" # 如果用户名或密码错误，添加一个消息
    else:
        message = ""
    
    context = {
        "message": message
    }
    return render(request, 'login.html', context)




###################### Navigation Page 导航页面

def navigation_page(request):
    pm = request.COOKIES.get('pm')
    user_projects = get_user_projects(pm)
    print('suc')
    all_projects = Projects.objects.all()
    print(all_projects)
    print(user_projects)
    return render(request, 'navigation_page.html',{'projects':user_projects})


###################### Start New Project 用户创建新项目网页


def start_new_project(request):
    # 创建字段名称映射
    date_attributes_mapping = {
        "Kickoff Time": "timing_kickoff",
        "Closure Time": "timing_closure",
        "Milestone 1 Time": "timing_milestone1",
        "Milestone 2 Time": "timing_milestone2",
        "Milestone 3 Time": "timing_milestone3",
        "Milestone 4 Time": "timing_milestone4"
    }

    context = {
        "attributes_before_project_type": [
            "Project Name",
            "Project Manager", 
            "Estimated Budget",
            "IRR",
            "Project Status",
            "Main Target",
        ],

        "sponsors": ["Apple", "Banana", "Cherry", "Durian", "Elderberry", "Fig", "Grape"],
        "facilitators": ["Jing Yang", "Lisa Shi", "Runkun Wang"],
        "steering_committee": ["Jeff Wang", "Yuan Zhou", "Yi Sun", "Brian Yang", "Li Yan", "Tony Huang", "Sam Guo", "Rowena Tao","Covey Wang", "Hairui Liu", "Bingyan Wang", "Abhishek Kumar"],
        
        # 使用映射中的模型字段名称
        "date_attributes": list(date_attributes_mapping.values()),

        "attributes_after_project_type_and_dates": [

            "Boundary Conditions",
            "Out of Scope",
            "Sponsor",
            "Steering committee",
            "Facilitator",
            #"Sponsor",
            "Risk and Uncertainties"
        ],
        # 保留映射，以备在模板中显示友好的名称
        "date_attributes_mapping": date_attributes_mapping
    }

    return render(request, 'start_new_project.html', context)


def project_site(request, project_id):
    project = Projects.objects.get(pk=project_id)
    if request.POST.get('success') == 'true':
        success_message = 'Update successful'
    else:
        success_message = 'Update fail'

    try:
        Announcement.objects.get(projectid=project)
        context = {
            'project': project,
            'success_message': success_message,
            'project_id': project_id,
            'announcement': Announcement.objects.get(projectid=project),
        }
        try:
            KickOff.objects.get(projectid=project)
            context = {
                'project': project,
                'success_message': success_message,
                'project_id': project_id,
                'announcement': Announcement.objects.get(projectid=project),
                'kickoff': KickOff.objects.get(projectid=project),
            }
        except KickOff.DoesNotExist:
            context = {
                'project': project,
                'success_message': success_message,
                'project_id': project_id,
                'announcement': Announcement.objects.get(projectid=project),
            }
    except Announcement.DoesNotExist:
        context = {
            'project': project,
            'success_message': success_message,
            'project_id': project_id,
        }

    return render(request, 'project_site.html', context)


#from .models import Projects, Announcement

def preview_announcement(request, project_id):

    project = get_object_or_404(Projects, projectid=project_id)

    announcement = get_object_or_404(Announcement, projectid=project_id)

    context = {
        'title': 'Announcement Review',
        'project': project,
        'announcement': announcement,
        'project_id': project_id
    }

    return render(request, 'preview_announcement.html', context)



def kickoff_review(request, project_id):

    project = get_object_or_404(Projects, projectid=project_id)
    kickoff = get_object_or_404(KickOff, projectid=project_id)

    context = {
        'title': 'Kickoff Review',
        'project': project,
        'kickoff': kickoff,
        'project_id': project_id  # 与kickoff_review相关的数据
    }

    return render(request, 'preview_kickoff.html', context)  # 确保有一个相应的HTML模板

def preview_milestone(request, project_id):
    project = get_object_or_404(Projects, projectid=project_id)
    milestones = get_object_or_404(Milestones, projectid=project_id)

    context = {
        'title': 'Milestone Review',
        'project': project,
        'milestones': milestones,
        'project_id': project_id
    }

    return render(request, 'preview_milestone.html', context)


def preview_closure(request, project_id):
    project = get_object_or_404(Projects, projectid=project_id)
    closure = get_object_or_404(Closure, projectid=project_id)
    
    context = {
        'project_id': project_id,  # 添加其他所需的上下文数据
        'project': project,
        'title':'Closure Review',
        'closure':closure
    }
    return render(request, 'preview_closure.html', context)


'''
def sign_in(username):

    url = 'http://10.246.97.75:8011/sso/admin/getinfo'
    data = {
        'username': username
    }
    response = requests.post(url, data=data)
    data = response.json()

    code = data['code']
    if code == 200:
        try:
            instance = Users.objects.get(pm=username)
            response = HttpResponse()
            response.set_cookie('pm', username)
            return instance
        except Users.DoesNotExist:
            string = data['data']
            data = json.loads(string)
            attribute = data['attributes']
            name = attribute['displayName'][0]
            email = attribute['mail'][0]
            department = attribute['department'][0]
            info = {'pm': username, 'name': name, 'email': email, 'department': department}
            instance = add_user(info)
            #set_cookie_pm(username)
            return instance
    else:
        return False



'''
def sign_in(username, request):
    try:
        instance = Users.objects.get(pm=username)

        # 将用户信息存储到session中
        request.session['user_data'] = {
            'name': instance.name,
            'email': instance.eml,
            'department': instance.dept
        }
        return instance

    except Users.DoesNotExist:
        # 如果用户不存在，这里需要从其他数据源获取用户数据（这部分代码未给出）
        # 假设从其他数据源获取的数据放在了data字典中
        string = data.get('data', '{}')
        data = json.loads(string)
        attribute = data.get('attributes', {})
        name = attribute.get('displayName', [''])[0]
        email = attribute.get('mail', [''])[0]
        department = attribute.get('department', [''])[0]
        
        info = {'pm': username, 'name': name, 'email': email, 'department': department}
        instance = add_user(info)
        
        # 也将新用户信息存储到session中
        request.session['user_data'] = {
            'name': name,
            'email': email,
            'department': department
        }
        return instance



def set_cookie_pm(username):
    response = HttpResponse()
    response.set_cookie('pm', username)
    return response


def add_user(info):
    name = info['name']
    pm = info['pm']
    email = info['email']
    department = info['department']

    new_user = Users(name=name, pm=pm, eml=email, dept=department)
    new_user.save()

    return new_user


def get_user_projects(pm):
    pm = Users.objects.get(pm=pm)
    projects = Projects.objects.filter(pm=pm)
    project_list = projects.values('project_name','project_manager','pm','project_status')
    return projects



def get_project_all(projectid):
    project = Projects.objects.get(projectid=projectid)
    return project

def get_announcement(project):
    try:
        announcement = Announcement.objects.get(projectid=project)
        return announcement
    except Announcement.DoesNotExist:
        return False

def get_closure(project):
    try:
        closure = Closure.objects.get(projectid=project)
        return closure
    except Closure.DoesNotExist:
        return False





def submit_new_project(request):
    if request.method == 'POST':
        # 从POST请求中获取数据
        project_name = request.POST.get('project_name')
        projectid = request.POST.get('project_id')  # 调整了变量名以匹配模型
        estimated_budget = request.POST.get('estimated_budget')
        irr = request.POST.get('irr')
        project_manager = request.POST.get('project_manager')
        project_type = request.POST.get('project_type')
        facilitator = request.POST.get('facilitator')
        main_target = request.POST.get('main_target')
        sponsor = request.POST.get('sponsor')
        project_status = request.POST.get('project_status')


        pm = request.COOKIES.get('pm')
        pm = Users.objects.get(pm=pm)

        # 获取项目的开始和结束日期
        timing_kickoff = request.POST.get('timing_kickoff')
        timing_closure = request.POST.get('timing_closure')
        timing_milestone1 = request.POST.get('timing_milestone1')
        timing_milestone2 = request.POST.get('timing_milestone2')
        timing_milestone3 = request.POST.get('timing_milestone3')
        timing_milestone4 = request.POST.get('timing_milestone4')

        # 从动态添加的字段中提取数据\

        boundary_conditions = '~'.join([request.POST.get(f'boundary-conditions_input_{i}', '') for i in range(1, 5)])
        out_of_scope = '~'.join([request.POST.get(f'out-of-scope_input_{i}', '') for i in range(1, 5)])
        risk_uncertainties = '~'.join([request.POST.get(f'risk-and-uncertainties_input_{i}', '') for i in range(1, 5)])

        # 获取 Steering committee 的多选复选框的值并合并为一个字符串
        steering_committee = ','.join(request.POST.getlist('steering_committee'))




        # 保存项目数据到数据库
        project = Projects(
            project_name=project_name,
            pm=pm,
            projectid=projectid,
            estimated_budget=estimated_budget,
            irr=irr,
            project_manager=project_manager,
            project_type=project_type,
            project_status=project_status,
            facilitator=facilitator,
            sponsor=sponsor,
            steering_committee=steering_committee,
            timing_kickoff=timing_kickoff,
            timing_closure=timing_closure,
            main_target=main_target,
            boundary_conditions=boundary_conditions,
            out_of_scope=out_of_scope,
            risk_uncertainties=risk_uncertainties,
            timing_milestone1=timing_milestone1,
            timing_milestone2=timing_milestone2,
            timing_milestone3=timing_milestone3,
            timing_milestone4=timing_milestone4,

        )
        project.save()

        # 保存数据到session中，供check_submitted_data视图使用
        request.session['submitted_data'] = {
            'project_name': project_name,
            'projectid': projectid,
            'estimated_budget': estimated_budget,
            'irr': irr,
            'project_manager': project_manager,
            'project_type': project_type,
            'facilitator': facilitator,
            'sponsor': sponsor,
            'project_status': project_status,
            'steering_committee': steering_committee,
            'timing_kickoff': timing_kickoff,
            'timing_closure': timing_closure,
            'main_target': main_target,
            'boundary_conditions': boundary_conditions,
            'out_of_scope': out_of_scope,
            'risk_uncertainties': risk_uncertainties,
            'timing_milestone1': timing_milestone1,
            'timing_milestone2': timing_milestone2,
            'timing_milestone3': timing_milestone3,
            'timing_milestone4': timing_milestone4,
        }

        # 重定向到check_submitted_data视图
        return redirect('check_data')

    else:
        return redirect('start_new_project_page')



def check_submitted_data(request):
    if 'submitted_data' in request.session:
        # 从session中获取数据
        data = request.session['submitted_data']
        # 渲染数据到模板
        return render(request, 'check_data.html', {'data': data})
    else:
        # 如果session中没有数据，重定向到start_new_project页面
        return redirect('start_new_project_page')


def update_project(request, projectid):
    if request.method == 'POST':
        # 从POST请求中获取数据
        project_name = request.POST.get('project_name')
        estimated_budget = request.POST.get('estimated_budget')
        irr = request.POST.get('irr')
        project_manager = request.POST.get('project_manager')
        project_type = request.POST.get('project_type')
        facilitator = request.POST.get('facilitator')
        sponsor = request.POST.get('sponsor')
        project_status = request.POST.get('project_status')
        main_target = request.POST.get('main_target')

        # 获取项目的开始和结束日期
        timing_kickoff = request.POST.get('timing_kickoff')
        timing_closure = request.POST.get('timing_closure')
        timing_milestone1 = request.POST.get('timing_milestone1')
        timing_milestone2 = request.POST.get('timing_milestone2')
        timing_milestone3 = request.POST.get('timing_milestone3')
        timing_milestone4 = request.POST.get('timing_milestone4')

        # 从动态添加的字段中提取数据
        #main_target = '$$'.join([request.POST.get(f'main-target_input_{i}', '') for i in range(1, 5)])
        boundary_conditions = ' '.join([request.POST.get(f'boundary-conditions_input_{i}', '') for i in range(1, 5)])
        out_of_scope = ' '.join([request.POST.get(f'out-of-scope_input_{i}', '') for i in range(1, 5)])
        risk_uncertainties = ' '.join([request.POST.get(f'risk-and-uncertainties_input_{i}', '') for i in range(1, 5)])

        project = Projects.objects.get(projectid=projectid)
        project.project_name=project_name
        project.project_manager=project_manager
        project.project_type=project_type
        project.estimated_budget=estimated_budget
        project.irr=irr
        project.facilitator=facilitator
        project.sponsor=sponsor

        project.timing_closure=timing_closure
        project.timing_kickoff=timing_kickoff
        project.timing_milestone1=timing_milestone1
        project.timing_milestone2=timing_milestone2
        project.timing_milestone3=timing_milestone3
        project.timing_milestone4=timing_milestone4

        project.main_target=main_target
        project.boundary_conditions=boundary_conditions
        project.out_of_scope=out_of_scope
        project.risk_uncertainties=risk_uncertainties

        project.save()
        return render(request, 'project_site.html', {'project': project})


def edit_announcement(request):
    data = json.loads(request.body.decode('utf-8'))
    projectid = data.get('projectid')
    try:
        project = Projects.objects.get(projectid=projectid)
        announcement = Announcement.objects.get(projectid=project)
        announcement.init_situation1 = data.get('section-a-1-0')
        announcement.init_situation2 = data.get('section-a-1-1')
        announcement.init_situation3 = data.get('section-a-1-2')
        announcement.init_situation4 = data.get('section-a-1-3')
        announcement.gene_concept1 = data.get('section-a-3-0')
        announcement.gene_concept2 = data.get('section-a-3-1')
        announcement.gene_concept3 = data.get('section-a-3-2')
        announcement.gene_concept4 = data.get('section-a-3-3')
        announcement.save()
        return JsonResponse({'success': True})
    except Announcement.DoesNotExist:
        project = Projects.objects.get(projectid=projectid)
        Announcement.objects.create(
            projectid=project,
            init_situation1=data.get('section-a-1-0'),
            init_situation2=data.get('section-a-1-1'),
            init_situation3=data.get('section-a-1-2'),
            init_situation4=data.get('section-a-1-3'),
            gene_concept1=data.get('section-a-3-0'),
            gene_concept2=data.get('section-a-3-1'),
            gene_concept3=data.get('section-a-3-2'),
            gene_concept4=data.get('section-a-3-3')
        )
        return JsonResponse({'success': True})
    except ValidationError:
        return JsonResponse({'success': False})


def edit_kickoff(request):
    data = json.loads(request.body.decode('utf-8'))
    projectid = data.get('projectid')
    try:
        project = Projects.objects.get(projectid=projectid)
        kickoff = KickOff.objects.get(projectid=project)
        kickoff.sub_target1 = data.get('section-b-1-0')
        kickoff.sub_target2 = data.get('section-b-1-1')
        kickoff.sub_target3 = data.get('section-b-1-2')
        kickoff.sub_target4 = data.get('section-b-1-3')
        kickoff.success_criteria1 = data.get('section-b-3-0')
        kickoff.success_criteria2 = data.get('section-b-3-1')
        kickoff.success_criteria3 = data.get('section-b-3-2')
        kickoff.success_criteria4 = data.get('section-b-3-3')
        kickoff.save()
        return JsonResponse({'success': True})
    except KickOff.DoesNotExist:
        project = Projects.objects.get(projectid=projectid)
        KickOff.objects.create(
            projectid=project,
            sub_target1=data.get('section-b-1-0'),
            sub_target2=data.get('section-b-1-1'),
            sub_target3=data.get('section-b-1-2'),
            sub_target4=data.get('section-b-1-3'),
            success_criteria1=data.get('section-b-3-0'),
            success_criteria2=data.get('section-b-3-1'),
            success_criteria3=data.get('section-b-3-2'),
            success_criteria4=data.get('section-b-3-3')
        )
        return JsonResponse({'success': True})
    except ValidationError:
        return JsonResponse({'success': False})


def edit_project(request):
    data = json.loads(request.body.decode('utf-8'))
    try:
        projectid = data.get('projectid')
        project = Projects.objects.get(projectid=projectid)

        project.project_name = data.get('general-information-1-0')
        project.estimated_budget = data.get('general-information-1-1')
        project.irr = data.get('general-information-3-1')
        project.project_manager = data.get('general-information-3-0')
        project.project_type = data.get('general-information-1-2')
        project.facilitator = data.get('general-information-1-7')

        project.timing_kickoff = data.get('general-information-1-3')
        project.timing_closure = data.get('general-information-3-3')
        project.timing_milestone1 = data.get('general-information-1-4')
        project.timing_milestone2 = data.get('general-information-3-4')
        project.timing_milestone3 = data.get('general-information-1-5')
        project.timing_milestone4 = data.get('general-information-3-5')

        project.main_target = data.get('general-information-1-6')
        project.boundary_conditions = data.get('general-information-3-6')
        project.out_of_scope = data.get('general-information-1-8')
        project.risk_uncertainties = data.get('general-information-3-8')

        project.save()

        return JsonResponse({'success':True})
    except ValidationError:
        return JsonResponse({'success':False})

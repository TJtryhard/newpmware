from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
import requests
import json
from .models import Users, Projects, Announcement, KickOff, Milestones, Closure
###################### Login Page 登录页面


def start_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        #password = request.POST.get('password')
        result = sign_in(username)
        #print(result.pm)

        if result:
            return redirect('navigation_page') # 跳转到导航页面
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
    user_projects = get_user_projects('uig27066')
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
            "Project Status"
        ],
        "managers": ["Apple", "Banana", "Cherry", "Durian", "Elderberry", "Fig", "Grape"],
        "facilitators": ["Jing Yang", "Lisa Shi", "Runkun Wang"],
        "steering_committee": ["Jeff Wang", "Yuan Zhou", "Yi Sun", "Brian Yang", "Li Yan", "Tony Huang", "Sam Guo", "Rowena Tao","Covey Wang", "Hairui Liu", "Bingyan Wang", "Abhishek Kumar"],
        
        # 使用映射中的模型字段名称
        "date_attributes": list(date_attributes_mapping.values()),

        "attributes_after_project_type_and_dates": [
            "Main Target",
            "Boundary Conditions",
            "Out of Scope",
            "Steering committee",
            "Facilitator",
            "Risk and Uncertainties"
        ],
        # 保留映射，以备在模板中显示友好的名称
        "date_attributes_mapping": date_attributes_mapping
    }

    return render(request, 'start_new_project.html', context)




def project_site(request):#########################See Existing Project Page用户阅读旧项目网页
    return render(request, 'project_site.html')

def preview_announcement(request):######################### Announcement Review Page
    return render(request, 'preview_announcement.html', {'title': 'Announcement Review'})

def kickoff_review(request):######################### Kick off Review Page
    return render(request, 'preview_kickoff.html')

def preview_milestone(request):######################### Milestone Review Page
    return render(request, 'preview_milestone.html')

def preview_closure(request):######################### Closure Review Page
    return render(request, 'preview_closure.html')


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
            return instance
    else:
        return False


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

        # 获取项目的开始和结束日期
        timing_kickoff = request.POST.get('timing_kickoff')
        timing_closure = request.POST.get('timing_closure')
        timing_milestone1 = request.POST.get('timing_milestone1')
        timing_milestone2 = request.POST.get('timing_milestone2')
        timing_milestone3 = request.POST.get('timing_milestone3')
        timing_milestone4 = request.POST.get('timing_milestone4')


        # 从动态添加的字段中提取数据
        main_target = ' '.join([request.POST.get(f'main-target_input_{i}', '') for i in range(1, 5)])
        boundary_conditions = ' '.join([request.POST.get(f'boundary-conditions_input_{i}', '') for i in range(1, 5)])
        out_of_scope = ' '.join([request.POST.get(f'out-of-scope_input_{i}', '') for i in range(1, 5)])
        risk_uncertainties = ' '.join([request.POST.get(f'risk-and-uncertainties_input_{i}', '') for i in range(1, 5)])



        # 保存项目数据到数据库
        project = Projects(
            project_name=project_name,
            projectid=projectid,
            estimated_budget=estimated_budget,
            irr=irr,
            project_manager=project_manager,
            project_type=project_type,
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

from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
import requests
import json
from .models import Users, Projects, Announcement, KickOff, Milestones, Closure

###################### Login Page 登录页面
from django.shortcuts import render, redirect
from .models import Users

def start_page(request):
    message = ""
    if request.method == "POST":
        username = request.POST.get('username')

        result = sign_in(username, request)  # 传递request到sign_in函数中

        if result:
            # 检查session中的数据
            user_data = request.session.get('user_data')
            if user_data:
                message = "数据已保存到session中: " + str(user_data)
            else:
                message = "数据未保存到session中!"

            return redirect('navigation_page')  # 跳转到导航页面
        else:
            message = "无效的用户!"  # 如果用户名或密码错误，添加一个消息

    context = {
        "message": message
    }
    return render(request, 'login.html', context)


###################### Navigation Page 导航页面

def navigation_page(request):
    # 从session中获取用户数据
    user_data = request.session.get('user_data', {})

    # 如果在session中有用户数据且包含'pm'键，则使用该用户的pm来获取他们的项目，否则使用默认值'uig27066'
    user_pm = user_data.get('pm', 'uig27066')

    user_projects = get_user_projects(user_pm)
    all_projects = Projects.objects.all()

    context = {
        'projects': user_projects,
        'all_projects': all_projects,
        'user_data': user_data  # 将user_data加入到context中，使其在模板中可用
    }

    return render(request, 'navigation_page.html', context)

def get_user_projects(pm_value):
    # 根据pm_value从数据库中筛选项目
    return Projects.objects.filter(project_manager=pm_value)



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

    # 从 session 中检查用户信息
    user_data = request.session.get('user_data', None)

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
        "date_attributes": list(date_attributes_mapping.values()),
        "attributes_after_project_type_and_dates": [
            "Main Target",
            "Boundary Conditions",
            "Out of Scope",
            "Steering committee",
            "Facilitator",
            "Risk and Uncertainties"
        ],
        "date_attributes_mapping": date_attributes_mapping,
        "user_data": user_data  # 将 user_data 添加到 context 中
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


from django.shortcuts import render, redirect
from .models import Users
import json

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
        # 从POST请求中获取数据，但不获取project_manager字段，因为我们将从session中获取PM数据。
        data = {
            'project_name': request.POST.get('project_name'),
            'estimated_budget': request.POST.get('estimated_budget'),
            'irr': request.POST.get('irr'),
            'project_type': request.POST.get('project_type'),
            'timing_kickoff': request.POST.get('timing_kickoff'),
            'timing_closure': request.POST.get('timing_closure'),
            'timing_milestone1': request.POST.get('timing_milestone1'),
            'timing_milestone2': request.POST.get('timing_milestone2'),
            'timing_milestone3': request.POST.get('timing_milestone3'),
            'timing_milestone4': request.POST.get('timing_milestone4'),
            'main_target': ' '.join([request.POST.get(f'main-target_input_{i}', '') for i in range(1, 5)]),
            'boundary_conditions': ' '.join([request.POST.get(f'boundary-conditions_input_{i}', '') for i in range(1, 5)]),
            'out_of_scope': ' '.join([request.POST.get(f'out-of-scope_input_{i}', '') for i in range(1, 5)]),
            'risk_uncertainties': ' '.join([request.POST.get(f'risk-and-uncertainties_input_{i}', '') for i in range(1, 5)])
        }

        # 从session中获取PM数据
        pm_data = request.session.get('user_data')
        if not pm_data:
            # 如果session中没有PM数据，可能是因为用户没有登录或者其他原因。这时应该处理这种情况。
            # 例如，重定向到登录页面或显示错误消息。
            return redirect('login_page')  # 假设有一个名为login_page的视图。

        pm_username = pm_data.get('name')  # 根据您的数据结构从session中获取PM的用户名。
        try:
            pm_instance = Users.objects.get(name=pm_username)  # 根据用户名获取Users对象
        except Users.DoesNotExist:
            # 如果找不到对应的用户，也应该处理这种情况。
            return redirect('error_page')  # 假设有一个名为error_page的视图。

        # 将项目与当前登录的PM关联
        data['pm'] = pm_instance

        # 保存项目数据到数据库
        project = Projects(**data)
        project.save()

        # 重定向到navigation_page视图
        return redirect('navigation_page')

    else:
        return redirect('start_new_project_page')




def check_submitted_data(request):
    # 检查是否在session中有提交的数据
    if 'submitted_data' in request.session:
        # 从session中获取数据，并明确命名为session_data
        session_data = request.session['submitted_data']
        # 渲染数据到模板
        return render(request, 'check_data.html', {'data': session_data})
    else:
        # 如果session中没有数据，重定向到start_new_project页面
        return redirect('navigation_page')

from django.http import JsonResponse



def check_session_data(request):
    user_data = request.session.get('user_data', None)
    if user_data:
        return JsonResponse(user_data)
    else:
        return JsonResponse({"message": "没有在session中找到用户数据"})

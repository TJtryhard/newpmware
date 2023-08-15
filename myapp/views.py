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
        password = request.POST.get('password')

        result = sign_in(username)
        #print(result.pm)

        if result:
            return redirect('navigation_page') # 跳转到导航页面
        #session here

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
    return render(request, 'navigation_page.html',{'projects':user_projects})


###################### Start New Project 用户创建新项目网页

from django.http import HttpResponse

from django.shortcuts import render
def start_new_project(request):
    context = {
        "attributes_before_project_type": [
            "Project ID",
            "Project Name",
            "Project Manager", 
            "Estimated Budget",
            "IRR",
            "Project Status"
        ],
        "managers": ["Apple", "Banana", "Cherry", "Durian", "Elderberry", "Fig", "Grape"],
        "facilitators": ["Jing Yang", "Lisa Shi", "Runkun Wang"],
        "steering_committee": ["Jeff Wang", "Yuan Zhou", "Yi Sun", "Brian Yang", "Li Yan", "Tony Huang", "Sam Guo", "Rowena Tao","Covey Wang", "Hairui Liu", "Bingyan Wang", "Abhishek Kumar"],
        
        "date_attributes": [
            "Kickoff Time",
            "Closure Time",
            "Milestone 1 Time",
            "Milestone 2 Time",
            "Milestone 3 Time",
            "Milestone 4 Time"
        ],
        "attributes_after_project_type_and_dates": [
            "Main Target",
            "Boundary Conditions",
            "Out of Scope",
            "Steering committee",
            "Facilitator",
            "Risk and Uncertainties"
        ]
    }
    
    return render(request, 'start_new_project.html', context)



#########################See Existing Project Page用户阅读旧项目网页


def project_site(request):
    return render(request, 'project_site.html')

######################### Announcement Review Page 

def preview_announcement(request):
    return render(request, 'preview_announcement.html', {'title': 'Announcement Review'})

######################### Kick off Review Page 

def kickoff_review(request):
    return render(request, 'preview_kickoff.html')

######################### Milestone Review Page 

def preview_milestone(request):
    return render(request, 'preview_milestone.html')

######################### Closure Review Page 

def preview_closure(request):
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


def new_project(request):
    try:
        if request.method == 'POST':
            project_name = request.POST.get('project_name')
            pm = request.POST.get('pm')
            estimated_budget = request.POST.get('estimated_budget')
            irr = request.POST.get('IRR')
            project_status = request.POST.get('project_status')
            project_type = request.POST.get('project_type')
            project_manager = request.POST.get('project_manager')
            project_team = request.POST.get('project_team')

            timing_kickoff = request.POST.get('timing_kickoff')
            timing_closure = request.POST.get('timing_closure')
            timing_milestone1 = request.POST.get('timing_milestone1')
            timing_milestone2 = request.POST.get('timing_milestone2')
            timing_milestone3 = request.POST.get('timing_milestone3')
            timing_milestone4 = request.POST.get('timing_milestone4')
            main_target = request.POST.get('main_target')
            boundary_conditions = request.POST.get('boundary_conditions')
            out_of_scope = request.POST.get('out_of_scope')
            steering_committee = request.POST.get('steering_committee')
            facilitator = request.POST.get('facilitator')
            risk_uncertainties = request.POST.get('risk_uncertainties')

            Projects.objects.create(
                Project_name=project_name,
                pm=pm,
                estimated_budget=estimated_budget,
                irr=irr,
                project_status=project_status,
                project_type=project_type,
                project_manager=project_manager,
                project_team=project_team,
                timing_kickoff=timing_kickoff,
                timing_closure=timing_closure,
                timing_milestone1=timing_milestone1,
                timing_milestone2=timing_milestone2,
                timing_milestone3=timing_milestone3,
                timing_milestone4=timing_milestone4,
                main_target=main_target,
                boundary_conditions=boundary_conditions,
                out_of_scope=out_of_scope,
                steering_committee=steering_committee,
                facilitator=facilitator,
                risk_uncertainties=risk_uncertainties
            )



    except Exception as e:
        pass

    #user_projects = {'project1':'project info', 'project2':'project info'}
    #return user_projects

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








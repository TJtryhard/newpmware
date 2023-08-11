from django.http import HttpResponse
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

    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Navigation Page</title>
        <link rel="stylesheet" href="/static/css/navigation_page_style.css"> <!-- Linking the external CSS file -->
    </head>
    <body>
        <h1>Navigation Page</h1>
        <a href="http://127.0.0.1:8000/start_new_project/"><button class="start-new-project-button">Start New Project</button></a>
        <a href="http://127.0.0.1:8000/project_site/"><button>Project Site</button></a>
        <h2>See Existing Project</h2>
        <table>
            <tr>
                <th>No.</th>
                <th>Project Name</th>
                <th>Project Manager</th>
                <th>Project ID</th>
                <th>Status</th>
            </tr>
            <tr><td></td><td></td><td></td><td></td><td></td></tr>
            <tr><td></td><td></td><td></td><td></td><td></td></tr>
            <tr><td></td><td></td><td></td><td></td><td></td></tr>
            <tr><td></td><td></td><td></td><td></td><td></td></tr>
        </table>
        <h3>Status Description:</h3>
        <p><span class="status-color" style="background-color:orange;"></span> Project Completed.</p>
        <p><span class="status-color" style="background-color:green;"></span> Progressing Satisfactorily.</p>
        <p><span class="status-color" style="background-color:#FFFF66;"></span> Project Marginally at Risk.</p>
        <p><span class="status-color" style="background-color:red;"></span> Project Significantly at Risk.</p>
        <p><span class="status-color" style="background-color:black;"></span> Project Cancelled.</p>
    </body>
    </html>
    """
    return HttpResponse(html)


###################### Start New Project 用户创建新项目网页

from django.http import HttpResponse

from django.shortcuts import render

def start_new_project(request):
    context = {
        "attributes_before_project_type": [
            "Project ID",
            "Project Name",
            "Project Manager",  # 添加 "Project Manager" 回到这里
            "Estimated Budget",
            "IRR",
            "Project Status"
        ],
        "managers": ["Apple", "Banana", "Cherry", "Durian", "Elderberry", "Fig", "Grape"],
        "facilitators": ["Jing", "Lisa", "Runkun Wang"],
        "steering_committee": ["Jeff", "Yuan", "Yi", "Brian"],
        
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
    user_projects = {'project1':'project info', 'project2':'project info'}
    return user_projects


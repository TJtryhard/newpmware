from django.urls import path
from .views import (start_page, navigation_page, start_new_project, project_site, 
                    preview_announcement, kickoff_review, preview_milestone, preview_closure, 
                    submit_new_project, check_submitted_data)  # Ensure submit_new_project is imported

urlpatterns = [
    path('login/', start_page, name='login_page'),
    path('navigation/', navigation_page, name='navigation_page'),
    path('start_new_project/', start_new_project, name='start_new_project_page'),
    path('submit_new_project/', submit_new_project, name='submit_new_project'),  # Directly use submit_new_project here
    path('project_site/<int:project_id>/', project_site, name='project_site'),
    path('previewannouncement/', preview_announcement, name='preview_announcement'),
    path('kickoff_review/', kickoff_review, name='kickoff_review'),
    path('preview_milestone/', preview_milestone, name='preview_milestone'),
    path('preview_closure/', preview_closure, name='preview_closure'),
    path('check_data/', check_submitted_data, name='check_data'),
]

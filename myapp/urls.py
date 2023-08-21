from django.urls import path
from .views import (start_page, navigation_page, start_new_project, project_site, 
                    preview_announcement, kickoff_review, preview_milestone, preview_closure, 
                    submit_new_project, check_submitted_data, edit_project)  # Ensure submit_new_project is imported

urlpatterns = [
    path('login/', start_page, name='login_page'),
    path('navigation/', navigation_page, name='navigation_page'),
    path('start_new_project/', start_new_project, name='start_new_project_page'),
    path('submit_new_project/', submit_new_project, name='submit_new_project'),  # Directly use submit_new_project here
    path('project_site/<int:project_id>/', project_site, name='project_site'),

    path('previewannouncement/<int:project_id>/', preview_announcement, name='preview_announcement'),
    path('kickoff_review/<int:project_id>/', kickoff_review, name='kickoff_review_with_id'),
    path('preview_milestone/<int:project_id>/', preview_milestone, name='preview_milestone_with_id'),
    path('preview_closure/<int:project_id>/', preview_closure, name='preview_closure_with_id'),


    path('check_data/', check_submitted_data, name='check_data'),
    path('edit_project/', edit_project, name='edit_project')
]


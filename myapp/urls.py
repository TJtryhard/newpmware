from django.urls import path
from .views import start_page, navigation_page, start_new_project, project_site, preview_announcement, kickoff_review, preview_milestone, preview_closure  # Import the new views

urlpatterns = [
    path('login/', start_page, name='login_page'),
    path('navigation/', navigation_page, name='navigation_page'),
    path('start_new_project/', start_new_project, name='start_new_project_page'),
    path('project_site/', project_site, name='project_site'),
    path('previewannouncement/', preview_announcement, name='preview_announcement'),
    path('kickoff_review/', kickoff_review, name='kickoff_review'),
    path('preview_milestone/', preview_milestone, name='preview_milestone'),  # New URL pattern for Preview Milestone
    path('preview_closure/', preview_closure, name='preview_closure'),  # New URL pattern for Preview Closure
]

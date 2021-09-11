from django.urls import path
from . import views

urlpatterns = [
    path('tasks_listing/', views.TaskListing.as_view(), name='tasks_listing'),
    path('own_tasks_listing/', views.EigeneTaskListing.as_view(),
         name='own_tasks_listing'),
    path('faculties_listing/', views.FacultyListing.as_view(), name='faculties_listing'),
    path('topics_listing/', views.TopicListing.as_view(), name='topics_listing'),
    path('grades_listing/', views.GradeListing.as_view(), name='grades_listing'),
]

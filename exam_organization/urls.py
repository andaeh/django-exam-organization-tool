from django.urls import path

from . import views
from .forms import UserLoginForm

app_name = 'exam_organization'
urlpatterns = [
    path('', views.task_overview, name="task_overview"),
    path('My/', views.own_task_overview_view,
         name="own_task_overview"),
    path('Exam/', views.prepare_create_exam,
         name='prepare_create_exam'),
    path('Exam/Tasks/', views.prepare_create_exam_tasks,
         name='prepare_create_exam_tasks'),
    path('Exam/output/', views.create_exam,
         name='create_exam'),
    #     path('Tag/<slug:slug>', views.tagged_view, name='tagged'),
    path('media/pdf/<str:pk>', views.create_pdf_preview, name='create_pdf_preview'),
    path('Task/Bearbeiten/<str:pk>',
         views.task_update_view, name='task_update'),
    path('Task/Löschen/<str:pk>',
         views.task_delete_view, name='task_delete'),
    #     path('Task/pdf/<str:pk>', views.task_pdf_preview, name='task_pdf'),
    path('Task/<str:pk>', views.task_detail_view,
         name='task_detail'),
    path('Neu/', views.task_create_view, name='task_create'),

]

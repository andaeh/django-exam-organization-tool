from django.urls import include, path
from rest_framework import routers
from exam_organization import views

router = routers.DefaultRouter()
router.register(r'tasks', views.TaskViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
]

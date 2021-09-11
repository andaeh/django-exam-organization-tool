import os

from django.apps import apps
from django.conf import settings

from .models import *


def get_model_names(request):
    models = apps.get_app_config('exam_organization').get_models()
    return {'models': models}


def get_current_model(request):
    try:
        current_model = apps.get_model(
            'exam_organization', request.path.split('/')[1])
    except:
        current_model = ''
    return {'current_model': current_model}

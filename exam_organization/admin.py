from django.contrib import admin

from . import models
# Register your models here.
admin.site.register(models.Faculty)
admin.site.register(models.Grade)
admin.site.register(models.Task)
admin.site.register(models.Topic)
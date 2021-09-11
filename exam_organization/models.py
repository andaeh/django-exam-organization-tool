import os

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save
from django.conf import settings
from django.core.validators import int_list_validator

from taggit.managers import TaggableManager
# Create your models here.


class Faculty(models.Model):
    short_name = models.CharField(max_length=10)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Ausbildungsrichtung"
        verbose_name_plural = "Ausbildungsrichtungen"

    def get_absolute_url(self):
        return reverse('exam_organization:overview', kwargs={'model': self._meta.verbose_name_raw})

    def __str__(self):
        return self.name


class Grade(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Jahrgangsstufe"
        verbose_name_plural = "Jahrgangsstufen"

    def get_absolute_url(self):
        return reverse('exam_organization:overview', kwargs={'model': self._meta.verbose_name_raw})

    def __str__(self):
        return self.name


class Topic(models.Model):
    short_name = models.CharField(max_length=10)
    grade = models.ForeignKey(
        Grade, on_delete=models.SET_NULL, null=True)
    faculty = models.ForeignKey(
        Faculty, on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Lernbereich"
        verbose_name_plural = "Lernbereiche"

    def __str__(self):
        return self.faculty.short_name + self.grade.name + ": " + self.description


class Task(models.Model):
    headline = models.CharField(max_length=100, verbose_name="Überschrift")
    topic = models.ManyToManyField(Topic, verbose_name="Lernbereiche")
    description = models.CharField(max_length=500, verbose_name="Beschreibung")
    total_BE = models.CharField(
        max_length=50, blank=True, validators=[int_list_validator], help_text="Pro Teilaufgabe, getrennt durch Kommata", verbose_name="Bewertungseinheiten")
    task_text = models.TextField(null=True, blank=True, verbose_name="Aufgabentext")
    slug = models.SlugField(unique=True, max_length=100, editable=True)
    tags = TaggableManager()
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="created_by", editable=False)
    edited_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="edited_by", editable=False)

    class Meta:
        verbose_name = "Aufgabe"
        verbose_name_plural = "Aufgaben"

    def get_absolute_url(self):
        return reverse('exam_organization:overview', kwargs={'model': self._meta.verbose_name_raw})

    def __str__(self):
        return self.headline


@receiver(post_save, sender=Task)
def delete_pdf(sender, instance, *args, **kwargs):
    try:
        file = os.path.join(settings.MEDIA_ROOT, 'pdf',
                            str(instance.id) + '.pdf')
        os.remove(file)
    except:
        pass


@receiver(post_delete, sender=Task)
def delete_pdf(sender, instance, *args, **kwargs):
    try:
        file = os.path.join(settings.MEDIA_ROOT, 'pdf',
                            str(instance.id) + '.pdf')
        os.remove(file)
    except:
        pass
    try:
        images = os.listdir(os.path.join(settings.MEDIA_ROOT, 'latex'))
        task_images = [f for f in images if f.startswith(str(instance.id))]
        for image in task_images:
            os.remove(os.path.join(settings.MEDIA_ROOT, 'latex', image))

    except:
        pass

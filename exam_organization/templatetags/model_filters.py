from django import template
from django.db.models import Q

from exam_organization.models import Task

register = template.Library()


@register.filter
def verbose_name(obj):
    return obj._meta.verbose_name


@register.filter
def verbose_name_plural(obj):
    return obj._meta.verbose_name_plural


@register.filter
def keyword_filter(obj, keywords):
    queryset = obj.none()
    keywords = keywords.split(" ")
    for keyword in keywords:
        queryset |= obj.filter(
            Q(headline__contains=keyword)
            | Q(description__contains=keyword)
            | Q(tags__name__contains=keyword)
        ).distinct()
    return queryset


@register.filter
def get_headline_from_id(obj):
    task = Task.objects.get(id=int(obj))
    return task.headline

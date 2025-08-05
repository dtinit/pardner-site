from django.contrib import admin
from django.contrib.admin.decorators import register
from .models import ServiceAccount, Study


@register(Study)
class StudyAdmin(admin.ModelAdmin):
    list_display = ['name', 'authors']
    verbose_name_plural = 'studies'

@register(ServiceAccount)
class ServiceAccount(admin.ModelAdmin):
    list_display = ['id', 'name', 'study']

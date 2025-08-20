from django.contrib import admin
from django.contrib.admin.decorators import register
from .models import Service, ServiceAccount, Study, Vertical

@register(Vertical)
class VerticalAdmin(admin.ModelAdmin):
    pass

@register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@register(Study)
class StudyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'authors']
    verbose_name_plural = 'studies'

@register(ServiceAccount)
class ServiceAccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'study', 'completed_donation_at']

from django.contrib import admin
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.shortcuts import resolve_url
from django.utils.html import format_html

from core.models import Service, ServiceAccount, Study, Vertical


def generate_model_link(model_class, model_obj_field, action='change'):
    url = resolve_url(admin_urlname(model_class._meta, action), model_obj_field.id)
    return format_html(f'<a href="{url}">{model_obj_field}</a>')


@admin.register(Vertical)
class VerticalAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'verticals_display']

    @admin.display(description='Vertical(s)')
    def verticals_display(self, obj):
        return ', '.join([vertical.name for vertical in obj.verticals.all()])


@admin.register(Study)
class StudyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'authors', 'service_display']
    verbose_name_plural = 'studies'

    @admin.display(description='Service(s)')
    def service_display(self, obj):
        return '; '.join(str(service) for service in obj.services.all())


@admin.register(ServiceAccount)
class ServiceAccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'link_to_study', 'link_to_service', 'completed_donation_at']

    def link_to_study(self, obj):
        return generate_model_link(Study, obj.study)

    def link_to_service(self, obj):
        return generate_model_link(Service, obj.service)

    actions = ['set_to_not_completed']

    @admin.action(description='Set to not completed')
    def set_to_not_completed(self, request, queryset):
        queryset.update(completed_donation_at=None)

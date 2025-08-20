from django.contrib import admin

from core.models import Service, ServiceAccount, Study, Vertical


def _verticals_display(verticals):
    return ', '.join([vertical.name for vertical in verticals])


@admin.register(Vertical)
class VerticalAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'verticals_display']

    @admin.display(description='Vertical(s)')
    def verticals_display(self, obj):
        return _verticals_display(obj.verticals.all())


@admin.register(Study)
class StudyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'authors', 'service_display']
    verbose_name_plural = 'studies'

    @admin.display(description='Service(s)')
    def service_display(self, obj):
        services = []
        for service in obj.services.all():
            verticals = _verticals_display(service.verticals.all())
            services.append(f'{service.name} ({service.id}) - {verticals}')
        return '; '.join(services)


@admin.register(ServiceAccount)
class ServiceAccountAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'study_display',
        'service_display',
        'verticals_display',
        'completed_donation_at',
    ]

    @admin.display(description='Study')
    def study_display(self, obj):
        return f'{obj.study.name} ({obj.study.id})'

    @admin.display(description='Service')
    def service_display(self, obj):
        return f'{obj.service.name} ({obj.service.id})'

    @admin.display(description='Vertical(s)')
    def verticals_display(self, obj):
        return ', '.join([vertical.name for vertical in obj.service.verticals.all()])

    actions = ['set_to_not_completed']

    @admin.action(description='Set to not completed')
    def set_to_not_completed(self, request, queryset):
        queryset.update(completed_donation_at=None)

from django import template

from core.models import ServiceAccount

register = template.Library()


@register.inclusion_tag('core/fragments/study_service.html', takes_context=True)
def render_study_service(context):
    service_account = ServiceAccount.objects.get_or_create_from_session(
        study_id=context['study'].id,
        session_id=context['request'].session.session_key,
        service_id=context['service'].id,
    )

    if service_account:
        return {**context.flatten(), 'service_account': service_account}

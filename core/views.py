from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import get_object_or_404, redirect, render

from core.internal import get_transfer_service
from core.internal.utils import fetch_and_store_token, get_current_host
from core.models import Service, ServiceAccount, Study


def index(request):
    studies = Study.objects.all()
    return render(request, "core/index.html", {
        'studies': studies
    })


def study_detail(request, study_id):
    study = get_object_or_404(Study, pk=study_id)
    return render(
        request,
        'core/study/detail.html',
        {
            'study': study,
            'should_show_completion_modal': request.session.pop(
                'has_finished_service_donation', False
            ),
        },
    )


def study_donation_modal(request, study_id, service_id):
    study = get_object_or_404(Study, pk=study_id)
    service = get_object_or_404(Service, pk=service_id)
    return render(request, "core/study/donation_modal.html", {
        'study': study,
        'service': service
    })


def study_donation_complete_modal(request, study_id):
    study = get_object_or_404(Study, pk=study_id)
    return render(
        request,
        'core/study/donation_complete_modal.html',
        {
            'study': study,
            'num_services_remaining': study.get_num_services_remaining(
                request.session.session_key
            ),
            'service_name': request.session.pop('service_donated_name', ''),
        },
    )


def study_connect(request, study_id, service_id):
    """
    Redirects to the authorization URL for the service of `transfer_service_name`
    and creates a `ServiceAccount` table entry.
    """
    service = get_object_or_404(Service, pk=service_id)
    transfer_service_manager = get_transfer_service(
        service.name, get_current_host(request)
    )
    if not transfer_service_manager:
        return HttpResponseNotFound('Service is not a part of the study.')

    auth_url, state = transfer_service_manager.authorization_url()

    service_account = ServiceAccount.objects.get_or_create_from_session(
        study_id, request.session.session_key, service_id
    )
    service_account.state = state
    service_account.save()

    return redirect(auth_url)


def callback(request, transfer_service_name):
    """
    Endpoint that gets called when the user's browser is redirected by the
    authorization server after accepting or rejecting the OAuth request.
    """
    transfer_service_manager = get_transfer_service(
        transfer_service_name, get_current_host(request)
    )
    if not transfer_service_manager:
        return HttpResponseNotFound('Service is not a part of the study.')

    state = request.GET.get('state')
    if not state:
        return HttpResponseNotFound(
            "Can't find authorization session with for participant of service."
        )

    service_account = get_object_or_404(ServiceAccount, state=state)

    try:
        fetch_and_store_token(request, transfer_service_manager, service_account)
        request.session['has_finished_service_donation'] = True
        request.session['service_donated_name'] = transfer_service_name
    except ValueError:
        return HttpResponseServerError('Error fetching token')

    return redirect('study_detail', study_id=service_account.study.id)

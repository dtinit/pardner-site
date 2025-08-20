from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.utils import timezone

from core.internal import build_full_url, get_current_host, get_transfer_service
from core.models import Service, Study, ServiceAccount


def index(request):
    studies = Study.objects.all()
    return render(request, "core/index.html", {
        'studies': studies
    })


def study_detail(request, study_id):
    study = get_object_or_404(Study, pk=study_id)
    return render(request, "core/study/detail.html", {
        'study': study,
        'has_finished_oauth': request.GET.get('has_finished_oauth', False)
    })


def study_donation_modal(request, study_id, service_id):
    study = get_object_or_404(Study, pk=study_id)
    service = get_object_or_404(Service, pk=service_id)
    return render(request, "core/study/donation_modal.html", {
        'study': study,
        'service': service
    })


def study_donation_complete_modal(request, study_id):
    study = get_object_or_404(Study, pk=study_id)
    return render(request, "core/study/donation_complete_modal.html", {
        'study': study
    })


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
        token = transfer_service_manager.fetch_token(
            authorization_response=build_full_url(request), code=request.GET.get('code')
        )
        service_account.access_token = token['access_token']
        service_account.completed_donation_at = timezone.now()
        service_account.save()
    except ValueError:
        return HttpResponseServerError('Error fetching token')

    return redirect(
        reverse(
            'study_detail', args=[service_account.study.id], query={'has_finished_oauth': True}
        ),
        study_id=service_account.study.id,
        permanent=True,
    )


from urllib.parse import urljoin

from django.utils import timezone
from pardner.services import StravaTransferService, TumblrTransferService
from pardner.verticals import Vertical

from core.models import Service
from pardnersite.settings import (
    STRAVA_CLIENT_ID,
    STRAVA_CLIENT_SECRET,
    TUMBLR_CLIENT_ID,
    TUMBLR_CLIENT_SECRET,
)


def _get_redirect_url(service_account_name, host):
    return urljoin(host, f'/callback/{service_account_name.lower()}')


def get_current_host(request):
    return f'{request.scheme}://{request.get_host()}'


def build_full_url(request):
    return urljoin(get_current_host(request), request.path_info)


def get_transfer_service(service_account_name, host):
    match service_account_name.lower():
        case Service.ServiceName.TUMBLR:
            return TumblrTransferService(
                client_id=TUMBLR_CLIENT_ID,
                client_secret=TUMBLR_CLIENT_SECRET,
                redirect_uri=_get_redirect_url(service_account_name, host),
                verticals={Vertical.FeedPost},
            )
        case Service.ServiceName.STRAVA:
            return StravaTransferService(
                client_id=STRAVA_CLIENT_ID,
                client_secret=STRAVA_CLIENT_SECRET,
                redirect_uri=_get_redirect_url(service_account_name, host),
                verticals={Vertical.FeedPost},
            )
        case _:
            return None

def fetch_and_store_token(request, transfer_service_manager, service_account):
    token = transfer_service_manager.fetch_token(
        authorization_response=build_full_url(request), code=request.GET.get('code')
    )
    service_account.access_token = token['access_token']
    service_account.completed_donation_at = timezone.now()
    service_account.save()
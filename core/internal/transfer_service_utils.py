from core.models import ServiceAccount
from pardnersite.settings import TUMBLR_CLIENT_ID, TUMBLR_CLIENT_SECRET
from pardner.services import TumblrTransferService
from pardner.verticals import Vertical


def get_transfer_service(service_account_name):
    match service_account_name.lower():
        case ServiceAccount.ServiceName.TUMBLR:
            return TumblrTransferService(
                client_id=TUMBLR_CLIENT_ID,
                client_secret=TUMBLR_CLIENT_SECRET,
                redirect_uri=ServiceAccount.redirect_url(service_account_name),
                verticals={Vertical.FeedPost},
            )
        case _:
            return None

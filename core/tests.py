import pytest
from unittest.mock import MagicMock

from pardner.exceptions import TumblrAPIError

from core.internal.utils import fetch_and_store_data
from core.models import DonatedPost, Service, ServiceAccount, Study


@pytest.fixture
def tumblr_service_account():
    """Creates a minimal Study + Service + ServiceAccount for Tumblr tests."""
    service = Service.objects.create(name=Service.ServiceName.TUMBLR)
    study = Study.objects.create(name='Test Study', authors='Tester')
    study.services.add(service)
    service_account = ServiceAccount.objects.create(
        study=study,
        service=service,
        state='test-state',
    )
    return study, service_account



def test_fetch_and_store_data_tumblr_success(tumblr_service_account):
    """
    When fetch_social_posting_vertical returns a valid tuple, DonatedPost
    records are created from the raw_posts list (the second element).
    """
    _, service_account = tumblr_service_account
    raw_post = {'id': 42, 'summary': 'hello'}

    mock_service = MagicMock()
    mock_service.fetch_social_posting_vertical.return_value = ([], [raw_post])

    fetch_and_store_data(mock_service, service_account, 'tumblr')

    posts = DonatedPost.objects.filter(service_account=service_account)
    assert posts.count() == 1
    assert posts.first().service_post_id == '42'
    assert posts.first().raw_data == raw_post


def test_fetch_and_store_data_tumblr_api_error_does_not_propagate(
    tumblr_service_account,
):
    """
    When fetch_social_posting_vertical raises TumblrAPIError, the exception is
    caught inside fetch_and_store_data and no DonatedPost records are created.
    The donation flow is unaffected (best-effort semantics).
    """
    _, service_account = tumblr_service_account

    mock_service = MagicMock()
    mock_service.fetch_social_posting_vertical.side_effect = TumblrAPIError(
        'Tumblr is down'
    )

    fetch_and_store_data(mock_service, service_account, 'tumblr')  # should not raise

    assert DonatedPost.objects.filter(service_account=service_account).count() == 0


def test_callback_stores_token_and_redirects(client, mocker, tumblr_service_account):
    """
    A successful callback stores the access token on the ServiceAccount and
    redirects to the study detail page.
    """
    study, service_account = tumblr_service_account

    mock_manager = MagicMock()
    mock_manager.fetch_token.return_value = {'access_token': 'test-token-123'}
    mocker.patch('core.views.get_transfer_service', return_value=mock_manager)
    mocker.patch('core.views.fetch_and_store_data')

    response = client.get(
        '/callback/tumblr',
        {'state': 'test-state', 'code': 'auth-code'},
    )

    service_account.refresh_from_db()
    assert service_account.access_token == 'test-token-123'
    assert response.status_code == 302
    assert response['Location'] == f'/study/{study.id}/'


def test_callback_data_fetch_failure_still_completes_donation(
    client, mocker, tumblr_service_account
):
    """
    When Tumblr's API raises TumblrAPIError, fetch_and_store_data catches it
    internally and does not propagate. The token is already stored before the
    data fetch, so the callback still redirects and the donation is complete.
    """
    study, service_account = tumblr_service_account

    mock_manager = MagicMock()
    mock_manager.fetch_token.return_value = {'access_token': 'test-token-456'}
    mock_manager.fetch_social_posting_vertical.side_effect = TumblrAPIError(
        'Tumblr is down'
    )
    mocker.patch('core.views.get_transfer_service', return_value=mock_manager)

    response = client.get(
        '/callback/tumblr',
        {'state': 'test-state', 'code': 'auth-code'},
    )

    service_account.refresh_from_db()
    assert service_account.access_token == 'test-token-456'
    assert response.status_code == 302
    assert response['Location'] == f'/study/{study.id}/'

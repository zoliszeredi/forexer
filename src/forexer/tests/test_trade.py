import json

import pytest
from django.urls import reverse

from forexer.trade.models import Trade


def test_tradepk():
    id_ = Trade._meta.fields[0].default()
    assert id_.startswith('TR') and len(id_[2:])


@pytest.mark.django_db
@pytest.mark.xfail
def test_rest_list(admin_client, live_server):
    instance = Trade.objects.create()
    assert reverse('trade-list') == '/api/trades/'
    response = admin_client.get(reverse('trade-list'))
    data = json.loads(response.data)
    assert data == [{}]

from django.urls import reverse


def test_unpopular(client):
    response = client.get(reverse("profile", kwargs=dict(username="georgewhewell")))
    assert response.status_code == 200


def test_popular(client):
    response = client.get(reverse("profile", kwargs=dict(username="barackobama")))
    assert response.status_code == 200

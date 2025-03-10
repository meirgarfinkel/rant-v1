import pytest


@pytest.fixture
def test_user(django_user_model):
    return django_user_model.objects.create_user(email='user@test.com', password='testpass123')

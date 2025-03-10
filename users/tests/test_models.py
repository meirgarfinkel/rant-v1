import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_user_creation():
    user = User.objects.create_user(
        email="test1@example.com",
        password="testpass123"
    )
    assert User.objects.count() == 1

@pytest.mark.django_db
def test_superuser_creation():
    superuser = User.objects.create_superuser(
        email="test2@example.com",
        password="testpass123"
    )
    assert User.objects.count() == 1

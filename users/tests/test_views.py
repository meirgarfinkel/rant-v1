import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_user_signup(client):
    url = reverse('users:signup')
    data = {
        'email': 'user@test.com',
        'password1': 'testpass123',
        'password2': 'testpass123'
    }
    response = client.post(url, data)
    # After signup, redirect should occur
    assert response.status_code == 302
    user = User.objects.get(email='user@test.com')
    assert user.email == 'user@test.com'

@pytest.mark.django_db
def test_user_login(client, test_user):
    url = reverse('users:login')
    data = {
        'username': 'user@test.com',
        'password': 'testpass123'
    }
    response = client.post(url, data)
    # Successful login should redirect
    assert response.status_code == 302

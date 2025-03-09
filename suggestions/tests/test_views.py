import pytest
from django.urls import reverse
from suggestions.models import Suggestion
from suggestions.managers import generate_anonymous_token


@pytest.mark.django_db
def test_create_suggestion(client, test_user):
    client.login(username='user@test.com', password='testpass123')

    url = reverse('suggestions:suggestion_create')
    data = {
        'title': 'Test Suggestion',
        'content': 'This is a test suggestion.'
    }
    response = client.post(url, data)
    assert response.status_code == 302

    # Ensure suggestion is created with the correct anonymous token
    sugg = Suggestion.objects.first()
    expected_token = generate_anonymous_token(test_user.id)
    assert sugg.anon_token == expected_token
    assert sugg.title == 'Test Suggestion'

@pytest.mark.django_db
def test_list_suggestions(client, test_user):
    token = generate_anonymous_token(test_user.id)
    # Create two suggestions for this user
    Suggestion.objects.create(title='Suggestion 1', content='Content 1', anon_token=token)
    Suggestion.objects.create(title='Suggestion 2', content='Content 2', anon_token=token)

    client.login(username='user@test.com', password='testpass123')
    url = reverse('suggestions:suggestion_list')
    response = client.get(url)
    assert response.status_code == 200
    # Ensure both suggestions are in the response context
    suggestions = response.context['suggestions']
    assert suggestions.count() == 2

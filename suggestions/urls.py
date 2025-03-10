from django.urls import path
from .views import SuggestionCreateView, SuggestionListView

app_name = 'suggestions'

urlpatterns = [
    path('create/', SuggestionCreateView.as_view(), name='suggestion_create'),
    path('list/', SuggestionListView.as_view(), name='suggestion_list'),
]

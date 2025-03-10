from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView
from .forms import SuggestionForm
from .models import Suggestion

class SuggestionCreateView(LoginRequiredMixin, CreateView):
    model = Suggestion
    form_class = SuggestionForm
    template_name = 'suggestions/suggestion_form.html'
    success_url = reverse_lazy('suggestions:suggestion_list')

    def form_valid(self, form):
        # Pass the logged-in user to the model’s save method
        self.object = form.save(user=self.request.user)
        return super().form_valid(form)

class SuggestionListView(LoginRequiredMixin, ListView):
    model = Suggestion
    template_name = 'suggestions/suggestion_list.html'
    context_object_name = 'suggestions'

    def get_queryset(self):
        # Employees see only their own suggestions
        return Suggestion.objects.for_user(self.request.user)

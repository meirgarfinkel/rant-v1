from django import forms
from .models import Suggestion
from suggestions.managers import generate_anonymous_token

class SuggestionForm(forms.ModelForm):
    class Meta:
        model = Suggestion
        fields = ['title', 'content']
    
    def save(self, commit=True, user=None):
        instance = super().save(commit=False)
        if user and not instance.anon_token:
            instance.anon_token = generate_anonymous_token(user.id)
        if commit:
            instance.save()
        return instance

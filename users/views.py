from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView as DjangoLoginView

from .forms import SignupForm, LoginForm


class SignupView(CreateView):
    form_class = SignupForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('app:home')

class LoginView(DjangoLoginView):
    authentication_form = LoginForm
    template_name = 'users/login.html'


# class LogoutView(View):
#     def get(self, request):
#         logout(request)
#         request.session.flush()
#         return redirect('login')

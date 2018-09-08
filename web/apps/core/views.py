from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from apps.core.forms.auth import LoginForm


class HomeView(TemplateView):
    template_name = 'core/home.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return redirect('sales:subscription-list')


class LoginView(TemplateView):
    template_name = 'core/login.html'

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['login_form'] = self.get_form()
        return context

    def get_form(self, *args, **kwargs):
        return LoginForm(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        form_data = request.POST.copy()
        login_form = self.get_form(form_data)

        if login_form.is_valid():
            user = authenticate(username=form_data.get('email'), password=form_data.get('password'))
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return redirect('login')


def logout_view(request):
    logout(request)
    return redirect('home')

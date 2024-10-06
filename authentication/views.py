from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .forms import SignupForm, SigninForm

class SignUpView    (FormView):
    template_name = 'authentication/signUpPage.html'
    form_class = SignupForm
    success_url = reverse_lazy('signInPage')  

    def form_valid(self, form):
        user = form.save()
        group_name = 'users'
        group, created = Group.objects.get_or_create(name=group_name)
        user.groups.add(group) 
        return super().form_valid(form)

class SignInView(FormView):
    template_name = 'authentication/signInPage.html'
    form_class = SigninForm
    success_url = reverse_lazy('homePage')  

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

class LogoutView(DjangoLogoutView):
    next_page = reverse_lazy('homePage')

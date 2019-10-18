# from django.shortcuts import render
from .forms import SignupForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy


class RegisterView(CreateView):
    template_name = 'signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('index')

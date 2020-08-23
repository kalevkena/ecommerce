from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.http import  HttpResponseRedirect
from accounts.models import Customer
from .forms import SignUpForm

# Create your views here.

class UserRegisterView(generic.CreateView):
    form_class = SignUpForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        context = {'form': self.form_class()}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user.save()
            new_custumer = Customer.objects.create(user=new_user)
            new_custumer.save()

            return HttpResponseRedirect(self.success_url)

        context = {'form': form}
        return render(request, self.template_name, context)

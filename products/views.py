from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView, FormView, CreateView, ListView
from products.models import Product, Category
from products.forms import ContactForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.core.mail import send_mail
import random



class HomeView(TemplateView):
    template_name = "home.html"

    """ def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        lucky_number = random.randint(1, 100)

        context = {'messages': {'m1': 'Hello SDA!', 'm2': 'Im alive!'},
               'lucky_number': lucky_number}

        return context """

class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('home')

def contact(request):
    if request.method == 'POST':
        message = request.POST['message']
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']

        # sending an email
        send_mail(
            name,
            message,
            email,
            ['kalevkena@gmail.com'],
        )

        return render(request, 'contact.html', {'name': name})
    else:
        return render(request, 'contact.html', {})

class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'


class CreateProductView(LoginRequiredMixin, CreateView):
    model = Product
    template_name = 'create.html'
    fields = '__all__'                   # instead of inserting all fields, like name, price et, can use __all__
    success_url = reverse_lazy('product_list')

def checkout(request):
    context = {}
    return render(request, 'checkout.html', context)

def cart(request):
    context= {}
    return render(request, 'cart.html', context)
    
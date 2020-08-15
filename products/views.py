from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, FormView, CreateView, ListView, DeleteView, UpdateView, DetailView
from products.models import Product, Category, Cart
from accounts.models import Customer
from products.forms import ContactForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.core.mail import send_mail
import random


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, *args, **kwargs):
        category_menu = Category.objects.all()
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context['category_menu'] = category_menu
        return context
        

class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('home')

def contact(request):
    if request.method == 'POST':
        message = request.POST['message']
        name = request.POST['name']
        email = request.POST['email']
        

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
    template_name = 'list.html'
    context_object_name = 'products'

    def get_queryset(self):
        filter_val = self.request.GET.get('filter', None)
        order = self.request.GET.get('orderby', 'id')
        
        new_queryset = Product.objects.order_by(order)

        
        if filter_val:
            new_queryset = new_queryset.filter(name__icontains=filter_val)
        
        return new_queryset


    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        
        context['orderby'] = self.request.GET.get(
            'orderby', 'id')
        
        context['filter'] = self.request.GET.get(
            'filter', None) 

        return context


class CreateProductView(LoginRequiredMixin, CreateView):
    model = Product
    template_name = 'create.html'
    fields = '__all__'                   # instead of inserting all fields, like name, price et, can use __all__
    success_url = reverse_lazy('list')

class DetailProductView(DetailView):
    model = Product
    template_name = 'detail.html'
    context_object_name = 'product'

class DeleteProductView(PermissionRequiredMixin, DeleteView):
    permission_required = ['products.delete_product', ]
    model = Product
    template_name = 'delete.html'
    context_object_name = 'product'
    success_url = reverse_lazy('list')

class UpdateProductView(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'update.html'
    context_object_name = 'product'
    fields = '__all__'
    success_url = reverse_lazy('list')

class CartView(ListView):
    model = Product
    template_name = 'cart.html'
    context_object_name = 'products'

    def get_queryset(self):
        logged_user = self.request.user
        customer = Customer.objects.filter(user=logged_user).first()

        cart = Cart.objects.filter(user=customer).filter(active=True).first()
        
        if cart == None:
            self.products = []
        else:
            self.products = cart.products.all()
        return self.products

    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        
        total = 0

        for p in self.products:
            total += p.price
    
        context['total'] = total 

        return context

def checkout(request):
    context = {}
    return render(request, 'checkout.html', context)

def CategoryView(request, categories):
    category_products = Product.objects.filter(category=categories)
    return render(request, 'categories.html', {'categories':categories, 'category_products':category_products})

def add_to_cart(request, product_id):
    logged_user = request.user
    customer = Customer.objects.filter(user=logged_user).first()

    carts = Cart.objects.filter(user=customer).filter(active=True)
    user_cart = None
    
    if carts.count() == 0:
        new_cart = Cart.objects.create(user=customer)
        new_cart.save()
        user_cart = new_cart
    else:
        user_cart = carts.first()

    product = Product.objects.filter(id=product_id).first()
    user_cart.products.add(product)
    return HttpResponseRedirect(reverse_lazy('list'))

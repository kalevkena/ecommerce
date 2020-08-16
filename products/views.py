from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, FormView, CreateView, ListView, DeleteView, UpdateView, DetailView
from products.models import Product, Category, Cart, OrderItem
from accounts.models import Customer
from products.forms import ContactForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.core.mail import send_mail
import random



def get_categories_context():
    categories = Category.objects.all()
    return categories

class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, *args, **kwargs):
        context = {}
        context['category_menu'] = get_categories_context()
        return context
        

class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('home')

    def get_context_data(self, *args, **kwargs):
        context = {}
        context['category_menu'] = get_categories_context()
        return context

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
        category = self.request.GET.get('category', None)
        
        new_queryset = Product.objects.order_by(order)

        
        if filter_val:
            new_queryset = new_queryset.filter(name__icontains=filter_val)
        
        if category:
            new_queryset = new_queryset.filter(category=category)

        
        return new_queryset


    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        
        context['orderby'] = self.request.GET.get(
            'orderby', 'id')
        
        context['filter'] = self.request.GET.get(
            'filter', None) 
        
        context['category_menu'] = get_categories_context()

        return context



class CreateProductView(LoginRequiredMixin, CreateView):
    model = Product
    template_name = 'create.html'
    fields = '__all__'                   # instead of inserting all fields, like name, price et, can use __all__
    success_url = reverse_lazy('list')

    def get_context_data(self, *args, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        context['category_menu'] = get_categories_context()
        return context

class DetailProductView(DetailView):
    model = Product
    template_name = 'detail.html'
    context_object_name = 'product'

    def get_context_data(self, *args, **kwargs):
        context = super(DetailProductView, self).get_context_data(**kwargs)
        context['category_menu'] = get_categories_context()
        return context

class DeleteProductView(PermissionRequiredMixin, DeleteView):
    permission_required = ['products.delete_product', ]
    model = Product
    template_name = 'delete.html'
    context_object_name = 'product'
    success_url = reverse_lazy('list')

    def get_context_data(self, *args, **kwargs):
        context = super(DeleteProductView, self).get_context_data(**kwargs)
        context['category_menu'] = get_categories_context()
        return context

class UpdateProductView(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'update.html'
    context_object_name = 'product'
    fields = '__all__'
    success_url = reverse_lazy('list')

    def get_context_data(self, *args, **kwargs):
        context = super(UpdateProductView, self).get_context_data(**kwargs)
        context['category_menu'] = get_categories_context()
        return context

class CartView(ListView):
    model = Product
    template_name = 'cart.html'
    context_object_name = 'order_items'

    def get_queryset(self):
        logged_user = self.request.user
        customer = Customer.objects.filter(user=logged_user).first()

        cart = Cart.objects.filter(user=customer).filter(active=True).first()
        
        if cart == None:
            self.order_items = []
        else:
            self.order_items = cart.order_items.all()

        return self.order_items

    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        
        total = 0

        for oi in self.order_items:
            total += oi.get_total

        context['total'] = total 
        context['category_menu'] = get_categories_context()

        return context


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

    order_item = user_cart.order_items.filter(product=product)

    if order_item.count() == 0:
        new_orderitem = OrderItem.objects.create(product=product)
        new_orderitem.save()
        user_cart.order_items.add(new_orderitem)
    else:
        orderitem = order_item.first()
        orderitem.quantity = orderitem.quantity + 1
        orderitem.save()

    return HttpResponseRedirect(reverse_lazy('list'))


def checkout(request):
    logged_user = request.user
    customer = Customer.objects.filter(user=logged_user).first()

    user_cart = Cart.objects.filter(user=customer).filter(active=True).first()

    order_items = user_cart.order_items.all()

    for order_item in order_items:
        order_item.product.quantity = order_item.product.quantity - 1
        order_item.product.save()
    
    user_cart.active = False
    user_cart.save()

    context = {'order_items' : order_items}

    sub_total = 0

    for oi in order_items:
        sub_total += oi.get_total
    
    context['sub_total'] = sub_total 
    context['shipping'] = 5
    context['total'] = sub_total + context['shipping'] 
    context['category_menu'] = get_categories_context()


    return render(request, 'checkout.html', context)

class PurchaseSuccessView(TemplateView, LoginRequiredMixin):
    template_name = "purchase_success.html"

    def get_context_data(self, *args, **kwargs):
        context = super(PurchaseSuccessView, self).get_context_data(**kwargs)
        context['category_menu'] = get_categories_context()
        return context

    


    
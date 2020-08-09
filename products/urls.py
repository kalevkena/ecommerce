from django.urls import path, include
from products.views import HomeView, ContactView, ProductListView, CreateProductView, DetailProductView, UpdateProductView, DeleteProductView, CartView, checkout
from . import views

urlpatterns = [
path('', HomeView.as_view(), name='home'),
path('contact/', ContactView.as_view(), name='contact'),
# path('accounts/register/', RegisterView.as_view(), name='register'),
path('checkout/', views.checkout, name='checkout'), 
path('list/', ProductListView.as_view(), name='list'),
path('create/', CreateProductView.as_view(), name='create'),
path('cart/', CartView.as_view(), name='cart'),
path('detail/<int:pk>', DetailProductView.as_view(), name='detail'),
path('update/<int:pk>', UpdateProductView.as_view(), name='update'),
path('delete/<int:pk>', DeleteProductView.as_view(), name='delete'),

]
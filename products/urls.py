from django.urls import path, include
from products.views import HomeView, ContactView, ProductListView, CreateProductView


urlpatterns = [
path('', HomeView.as_view(), name='home'),
path('contact/', ContactView.as_view(), name='contact'),
# path('accounts/register/', RegisterView.as_view(), name='register'),
# path('checkout/'), CheckoutView.as_view(), name='checkout'), 
path('product_list/', ProductListView.as_view(), name='product_list'),
path('create/', CreateProductView.as_view(), name='create'),
# path('cart/', CartView.as_view(), name='cart')

]
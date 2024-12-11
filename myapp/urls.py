
from django.urls import path
from .import views



urlpatterns=[
    path('', views.home ,name='home'),
    path('placeOrder/<str:i>/',views.placeOrder,name='placeOrder'),
    path('login/', views.loginPage,name='login'),
    path('logout/', views.logoutPage,name='logout'),
    path('register/',views. registerPage,name='register'),
    path('addProduct/',views. addProduct,name='addProduct'),
    path('add-to-cart/<int:p_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/',views.cart_view,name='cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
  
  
    path('buy-now/<int:product_id>/',views.buy_now, name='buy_now'),
    path('order-confirmation/<int:order_id>/',views.order_confirmation, name='order_confirmation'),
   
   
   
    path('pay/', views.initiate_payment, name='initiate_payment'),
    path('payment/callback/', views.payment_callback, name='payment_callback'),


    

]
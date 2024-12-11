from django.shortcuts import  redirect,render
from django.contrib.auth import login,logout,authenticate
from .forms import *
from .models import*
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .services.razorpay_services import create_order, verify_payment

from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from django.conf import settings
 
# Create your views here.
 
def home(request):                                       
    products = Product.objects.all()
    context = {
        'product':products
    }
    return render(request,'index.html',context)
 
def placeOrder(request,i):
    customer= Customer.objects.get(id=i)
    form=createorderform(instance=customer)
    if(request.method=='POST'):
        form=createorderform(request.POST,instance=customer)
        if(form.is_valid()):
            form.save()
            return render(request,'base.html',{'form':form})
    context={'form':form}
    return render(request,'placeOrder.html',context)
 
def addProduct(request):
    form=createproductform()
    if(request.method=='POST'):
        form=createproductform(request.POST,request.FILES)
        if(form.is_valid()):
            form.save()
            return redirect('/')
    context={'form':form}
    return render(request,'addProduct.html',context)
 
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home') 
    else: 
        form=createuserform()
        customerform=createcustomerform()
        if request.method=='POST':
            form=createuserform(request.POST)
            customerform=createcustomerform(request.POST)
            if form.is_valid() and customerform.is_valid():
                user=form.save()
                customer=customerform.save(commit=False)
                customer.user=user 
                customer.save()
                return redirect('login')
            context={
                'form':form,
                'customerform':customerform,
            }
        return render(request,'register.html',context)
 
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
       if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('/')
       context={}
       return render(request,'login.html',context)
 
def logoutPage(request):
    logout(request)
    return redirect('/')

def add_to_cart(request,p_id):
    product = Product.objects.get(id=p_id)
    cart_item, created = Cart.objects.get_or_create(product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('/')
    
def cart_view(request):
    cart_items = Cart.objects.all()
    total = sum(item.total_price() for item in cart_items)
    return render (request, 'cart.html', {'cart_items': cart_items, 'total': total})



def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        order = Order.objects.create(product=product)
        amount = int(product.price)  # Get amount from form or request
        order = create_order(amount)
        context = {
            'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            'order_id': order['id'],
            'amount': amount * 100,  # Amount in paise for Razorpay
            'currency': order['currency'],
        }
        return render(request, 'checkout.html', context)
        # Add logic for payment processing here

    return render(request, 'buy_now.html', {'product': product})


def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_confirmation.html', {'order': order})
    



def remove_from_cart(request, product_id):
    cart_item = Cart.objects.get(product_id=product_id)
    cart_item.delete()
    return redirect('cart')

def initiate_payment(request):
    if request.method == "POST":
        amount = int(request.POST['amount'])  # Get amount from form or request
        order = create_order(amount)
        context = {
            'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            'order_id': order['id'],
            'amount': amount * 100,  # Amount in paise for Razorpay
            'currency': order['currency'],
        }
        return render(request, 'payments/checkout.html', context)
    return render(request, 'payments/pay.html')

@csrf_exempt
def payment_callback(request):
    if request.method == "POST":
        payment_id = request.POST.get('razorpay_payment_id')
        order_id = request.POST.get('razorpay_order_id')
        signature = request.POST.get('razorpay_signature')

        # Verify the payment
        if verify_payment(payment_id, order_id, signature):
            # save to database
            Payment.objects.create(
                payment_id=payment_id,
                order_id=order_id,
                amount=1000,  # You can store actual amount from order
                status='Success'
            )
            return render(request, 'payments/success.html')
        else:
            # Payment failed
            Payment.objects.create(
                payment_id=payment_id,
                order_id=order_id,
                amount=1000,
                status='Failed'
            )
            return render(request, 'payments/failure.html')
    return redirect('initiate_payment')






    # product = get_object_or_404(Product, id=product_id)
    # if request.method == 'POST':
    #     order = Order.objects.create(product=product)
    #     # Add logic for payment processing here
    #     return redirect('order_confirmation', Order_id=order.product_id)

    # return render(request, 'buy_now.html', {'product': product})









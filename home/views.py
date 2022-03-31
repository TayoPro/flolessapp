from django.shortcuts import render,redirect
from django.http import HttpResponse 
from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .forms import RegisterForm, ProfileUpdateForm, TrainingForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash

from .models import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
import requests
import json
import random
import string
import uuid


# Create your views here.
def index(request):
    setting= Setting.objects.get(pk=1)
    brand = Brand.objects.all()[:3]
    banner = Banner.objects.all()[:1]
    sample = Sample.objects.all()[:3]
    training = Training.objects.all().order_by('-id')[:1]
    category = Category.objects.all()
    glow = Product.objects.filter(glow= True).order_by('-id')[:4]
    whitening = Product.objects.filter(whitening= True).order_by('-id')[:4]
    lightening = Product.objects.filter(lightening= True).order_by('-id')[:4]
    
    
    context={
        'setting':setting,
        'brand': brand,
        'banner':banner,
        'sample':sample,
        'glow': glow,
        'training':training,
        'category':category,
        'whitening': whitening,
        'lightening': lightening,
    }
    return render(request, 'index.html', context)
    

def about(request):
    setting = Setting.objects.get(pk=1)
    products = Product.objects.all()
    training = Training.objects.all()
    category = Category.objects.all()

    context = { 
        'setting': setting,
        'products': products,
        'training':training,
        'category':category,
    }            

    return render(request, 'about.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Your message has been sent! Our Customer Service Team will reach you soon.")
            return redirect('contact')


    setting = Setting.objects.get(pk=1)
    form = ContactForm()
    products = Product.objects.all()
    sample = Sample.objects.all()[:3]
    category = Category.objects.all()
       
    context= { 
        'setting': setting,
        'form': form,
        'products': products,   
        'sample':sample,
        'category':category,             
    }

    return render(request, 'contact.html', context)

def products(request):
    setting= Setting.objects.get(pk=1)
    sample = Sample.objects.all()[:3]
    category = Category.objects.all()
    products = Product.objects.order_by('-created').filter(available='In Stock')
    paginator = Paginator(products,4)
    page= request.GET.get('page')
    paginate = paginator.get_page(page)
    
    context= {
        'setting': setting,
        'sample': sample,
        'products': paginate,
        'category':category,
    }

    return render(request, 'products.html', context)

def product(request,id,slug):
    setting= Setting.objects.get(pk=1)
    category = Category.objects.all()
    sample = Sample.objects.all()[:3]
    catdata= Category.objects.get(pk=id)
    product = Product.objects.filter(category_id=id).order_by('-id')
    paginator = Paginator(product,4)
    page= request.GET.get('page')
    paged_product = paginator.get_page(page)
    

    context= {
        'setting': setting,
        'category': category,
        'catdata': catdata,
        'product': paged_product,
        'sample':sample,
        'category':category,
    }

    return render(request, 'product.html', context)
#     # return HttpResponse(products)



def detail(request,id,slug):
    setting= Setting.objects.get(pk=1)
    category = Category.objects.all()
    product = Product.objects.order_by('-id')[:4]
    detail = Product.objects.get(pk=id)
    
    
    context= {
        'setting': setting,
        'category': category,
        'product': product,
        'detail': detail,
    }

    return render(request, 'details.html', context)
    

def accountform(request):
    setting= Setting.objects.get(pk=1)
    sample = Sample.objects.all()[:3]

    context = {
        'setting': setting,
        'sample':sample,
    }
    return render(request, 'account.html', context)

def loginform(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user:
            login(request,user)
            return redirect('index')
        else:
            messages.info(request,'Invalid username/password')
    
    setting= Setting.objects.get(pk=1)
    sample = Sample.objects.all()[:3]
    

    context = {
        'setting': setting,
        'sample':sample,
    }
    return render(request,'account.html', context)


def logoutfunc(request):
  logout(request)
  return redirect('loginform')


def registerform(request):
    form = RegisterForm()
    if request.method == 'POST':
        pro_img = request.POST['pro_img']
        form = RegisterForm(request.POST)
        if form.is_valid():
            myuser = form.save()
            p = UserProfile(user=myuser)
            p.first_name = myuser.first_name
            p.last_name = myuser.last_name
            p.image = pro_img
            p.save()
            login(request,myuser)
            return redirect('index')
        else:
            messages.warning(request,form.errors)
        return redirect('registerform')
    
    setting= Setting.objects.get(pk=1)
    sample = Sample.objects.all()[:3]

    context = {
        'form':form,
        'setting': setting,
        'sample':sample,
    }
    
    return render(request,'account.html',context)
  


def training(request):
    fee = Training.objects.all().order_by('-id')[:1]
    form = RegisterForm()
    if request.method == 'POST':
        phone = request.POST['phone']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        country = request.POST['country']
        form = RegisterForm(request.POST)
        if form.is_valid():
            newuser = form.save()
            p = UserProfile(user=newuser)
            p.first_name = newuser.first_name
            p.last_name = newuser.last_name
            p.phone = phone
            p.address = address
            p.city = city
            p.state = state
            p.country = country
            p.save()
            login(request,newuser)
            return redirect('confirm')
        else:
            messages.warning(request,form.errors)
        return redirect('training')
    
    setting= Setting.objects.get(pk=1)
    sample = Sample.objects.all()[:3]

    context = {
        'form':form,
        'setting': setting,
        'sample':sample,
        'fee':fee
    }
    
    return render(request,'trainreg.html',context)
  

@login_required(login_url='/login')
def confirm(request):
    fee = Training.objects.all().order_by('-id')[:1]
    setting= Setting.objects.get(pk=1)
    profile= UserProfile.objects.get(user__username = request.user.username)
    sample = Sample.objects.all()[:3]

    context = {
        'setting': setting,
        'profile': profile,
        'sample':sample,
        'fee':fee
    }

    return render(request, 'confirm.html', context)


@login_required(login_url='/login')
def userprofile(request):
    setting= Setting.objects.get(pk=1)
    profile= UserProfile.objects.get(user__username = request.user.username)
    sample = Sample.objects.all()[:3]
    category = Category.objects.all()
    

    context = {
        'setting': setting,
        'profile': profile,
        'sample':sample,
        'category':category
    }
    return render(request, 'profile.html', context)



@login_required(login_url='/login')
def userupdate(request):
    if request.method == 'POST':
        profileform = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if profileform.is_valid:
            profileform.save()
            messages.success(request, 'Your Account has been updated!')
            return redirect('userprofile')
    else:
        profileform = ProfileUpdateForm(instance=request.user.userprofile)
        setting= Setting.objects.get(pk=1)
        category = Category.objects.all()
        profile = UserProfile.objects.get(user__username = request.user.username)
        sample = Sample.objects.all()[:3]
        category = Category.objects.all()

        context = {
            'profileform': profileform,
            'setting': setting,
            'category': category,
            'profile': profile,
            'sample':sample,
            'category':category
    }
    return render(request, 'profileupdate.html', context)



@login_required(login_url='/login')
def userpassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('index')
        else:
            messages.error(request, 'Please correct the error below.<br>' + str(form.errors))
            return redirect('userpassword')
    else:
        form = PasswordChangeForm(request.user)
        setting= Setting.objects.get(pk=1)
        category = Category.objects.all()
        profile = UserProfile.objects.get(user__username = request.user.username)
        sample = Sample.objects.all()[:3]
        category = Category.objects.all()


        context = {
            'form': form,
            'setting': setting,
            'category': category,
            'profile': profile,
            'sample':sample,
            'category':category
        }
    return render(request, 'password.html', context) 





@require_POST
@login_required(login_url='/login')
def addtoshopcart(request):
    profile= UserProfile.objects.get(user__username = request.user.username)
    cart_code = profile.id
    url = request.META.get('HTTP_REFERER')
    thequantity = int(request.POST['quantity'])
    theprodid = request.POST['prodid']
    aprod = Product.objects.get(pk=theprodid)

    cart = ShopCart.objects.filter(order_placed=False)
    if cart: 
        prodchecker = ShopCart.objects.filter(product_id = aprod.id, quantity=thequantity,order_code=cart_code, user__username=request.user.username).first()
        if prodchecker: 
            prodchecker.quantity += thequantity
            prodchecker.save()
            messages.success(request, "Product added to Shopcart!  Click on basket to view order.")
            return redirect(url)

        else: #product is not in the cart, add it
            anitem = ShopCart()
            anitem.product=aprod
            anitem.user=request.user
            anitem.order_code= cart_code
            anitem.quantity=thequantity
            anitem.order_placed=False
            anitem.save()                
                 
        
    else: #create a new cart, generate  order code
        ordercode = str(uuid.uuid4())
        newcart = ShopCart()
        newcart.product=aprod
        newcart.user=request.user
        newcart.order_code=cart_code
        newcart.quantity=thequantity
        newcart.order_placed=False
        newcart.save()

    messages.success(request, "Product added to Shopcart!")
    return redirect(url)
    


@login_required(login_url='/login')
def shopcart(request):  
    category = Category.objects.all() 
    setting= Setting.objects.get(pk=1)
    profile= UserProfile.objects.get(user__username = request.user.username)
    cart_code = profile.id
    shopcart = ShopCart.objects.filter(order_placed=False,user__username = request.user.username)
    # shopcart = ShopCart.objects.filter(order_placed=False).filter(user__username=request.user.username)
    
    subtotal=0
    shippingfee = 0
    vat =0
    total = 0
    
    for item in shopcart:
        if item.product.discount:
            subtotal += item.product.discount * item.quantity
        else:
            subtotal += item.product.price * item.quantity

    # Shipping rules: 8% fees to all orders above 150. 0 fees to orders lower
    if subtotal > 5000:
        shippingfee = 0.08 * subtotal
    else:
        shippingfee = 0

    vat = 0.075 * subtotal

    total = subtotal + shippingfee + vat
   
    
    context = { 
        'setting': setting,
        'category': category,
        'shopcart': shopcart,
        'subtotal': subtotal,
        'shipping': shippingfee,
        'vat': vat,
        'total':total,
        'cartcode':cart_code
    }

    return render(request, 'cart.html', context)


@require_POST
@login_required(login_url='/login')
def updatequantity(request):
    url = request.META.get('HTTP_REFERER')
    newquantity = request.POST['itemquantity']
    theitem = ShopCart.objects.get(id=request.POST['itemid'])
    theitem.quantity = newquantity
    theitem.save()

    messages.success(request, "Product Quantity successfully updated")
    return redirect(url)



@login_required(login_url='/login')
def deletefromcart(request,id):
    url = request.META.get('HTTP_REFERER')
    ShopCart.objects.filter(id=id).delete()
    cart =ShopCart.objects.filter(id=id)
    messages.success(request, 'Item deleted from Shopcart.')
    return redirect(url)
    


@login_required(login_url='/login')
def checkout(request):
    category = Category.objects.all()  
    setting= Setting.objects.get(pk=1)
    # shopcart = ShopCart.objects.filter(user__username = request.user.username).filter(order_placed=False)
    orderno = request.POST['get_cart']
    profil= UserProfile.objects.get(user__username = request.user.username)
    cart_code = profil.id
    shopcart = ShopCart.objects.filter(order_placed=False, user__username = request.user.username)
    profile= User.objects.get(username = request.user.username)

    subtotal=0
    shippingfee = 0
    vat = 0
    total = 0

    for item in shopcart:
        if item.product.discount:
            subtotal += item.product.discount* item.quantity
        else:
            subtotal += item.product.price * item.quantity 

    # Shipping rules: 8% fees to all orders above 150. 0 fees to orders lower
    if subtotal > 5000:
        shippingfee = 0.08 * subtotal
    else:
        shippingfee = 0

    # vat is at 7.50% of the total purchase to  be made 
    vat = 0.075 * subtotal

    total = subtotal + shippingfee + vat    

    context = { 
        'setting': setting,                
        'shopcart': shopcart,
        'order_code':orderno,
        'profile': profile,
        'category': category,               
        'subtotal': subtotal,
        'shipping': shippingfee,
        'vat': vat,
        'total':total
        }
    return render(request, 'checkout.html', context)
    

@require_POST
@login_required(login_url='/login')
def placeorder(request):
    api_key = 'sk_test_0c3bb25f14513ee95dcbe057e8b007f8b8480aa1'
    url = 'https://api.paystack.co/transaction/initialize'
    callback_url = 'http://18.208.137.83/ordercompleted/'
    # callback_url = 'http://localhost:8000/ordercompleted/'
    ordercode =  request.POST['order_number']
    autogen_ref = ''.join(random.choices(string.digits + string.ascii_letters, k=8))
    user = User.objects.get(username = request.user.username)
    total = float(request.POST['amount']) * 100    
    

    headers = {'Authorization': f'Bearer {api_key}'}
    data = {'reference': autogen_ref, 'amount':int(total), "currency": "NGN", 'order_number':ordercode, 'email':user.email, 'callback_url':callback_url }

    
    # making a request to PAYSTACK 
    try:
        r = requests.post(url, headers=headers, json=data)
    except Exception:
        messages.error(request, 'Network busy. Please try again in few minutes. Thank You!')
    else:
        # create an order 
        transback = json.loads(r.text)
        
        rd_url = transback['data']['authorization_url']
        theuser= UserProfile.objects.get(user=request.user)
        order = Checkout()
        order.first_name=theuser.user.first_name
        order.last_name=theuser.user.last_name
        order.phone=theuser.phone
        order.city=theuser.city
        order.order_code= ordercode
        order.payment_code = autogen_ref
        order.total=total
        order.order_placed = True
        order.save()

        shopcart = ShopCart.objects.filter(order_placed=False)
        for item in shopcart:
            item.order_placed = True
            item.save()
        
        
            aproduct = Product.objects.get(id=item.product.id)
            aproduct.maxquantity -= item.quantity
            aproduct.save() 
        return redirect(rd_url)
    return redirect('order:checkout')


@require_POST
@login_required(login_url='/login')
def payfee(request):
    api_key = 'sk_test_0c3bb25f14513ee95dcbe057e8b007f8b8480aa1'
    url = 'https://api.paystack.co/transaction/initialize'
    callback_url = 'http://18.208.137.83/profile/'
    autogen_ref = ''.join(random.choices(string.digits + string.ascii_letters, k=8))
    user = User.objects.get(username = request.user.username)
    total = float(request.POST['amount']) * 100 
     

    headers = {'Authorization': f'Bearer {api_key}'}
    data = {'reference': autogen_ref, 'amount':int(total), "currency": "NGN",'order_number':user.id,  'email':user.email, 'callback_url':callback_url }

    
    # making a request to PAYSTACK 
    try:
        r = requests.post(url, headers=headers, json=data)
    except Exception:
        messages.error(request, 'Network busy. Please try again in few minutes. Thank You!')
    else:
        # create an order 
        transback = json.loads(r.text)
        
        rd_url = transback['data']['authorization_url']
        user= User.objects.get(username=request.user.username)
        order = TrainingReg()
        order.user= user.userprofile.user
        order.first_name= user.userprofile.first_name
        order.last_name= user.userprofile.last_name
        # order.email= user.userprofile.email
        order.phone= user.userprofile.phone
        order.payment_code = autogen_ref
        order.fee=total
        order.paid=True
        order.save()

        return redirect(rd_url)
    return redirect('confirm')



@login_required(login_url='/login')
def ordercompleted(request):
    category = Category.objects.all()  
    sample = Sample.objects.all()[:3]
    setting= Setting.objects.get(pk=1)
    profile= User.objects.get(username = request.user.username)
    shopcart = ShopCart.objects.filter(order_placed=False).filter(user__username = request.user.username)
    
    context = {
        'setting': setting,
        'category': category,
        'sample':sample,
        'shopcart': shopcart,
        'profile': profile,
    }
    
    return render(request, 'ordercompleted.html', context)

from django.shortcuts import render,redirect
from shop.models import Category,Products
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    return render(request,'home.html')
@login_required
def category(request):
    return render(request,'category.html')

@login_required
def allcategory(request):
    items=Category.objects.all()
    return render(request,'category.html',{'items':items})

@login_required
def products(request,i):
    product=Category.objects.get(id=i)
    prds=Products.objects.filter(category=product)

    #or
    #prds=Products.objects.filter(category=i)
    #prds=Products.objects.filter(category__id=i)
    return render(request,'product.html',{'product':product,'prds':prds})

@login_required
def product_details(request,i):
    pro_detail=Products.objects.get(id=i)
    return render(request,'product_detail.html',{'pro_detail':pro_detail})

def register(request):
    if(request.method=="POST"):
        u=request.POST['u']
        p = request.POST['pw']
        cp = request.POST['pw1']
        fn = request.POST['fn']
        ln = request.POST['ln']
        e = request.POST['e']
        if(cp==p):
            user=User.objects.create_user(username=u,password=p,first_name=fn,last_name=ln,email=e)
            user.save()
            return redirect('shop:home')
    return render(request,'register.html')


def user_login(request):
    if(request.method=="POST"):
        u=request.POST['u']
        p=request.POST['pw']
        user=authenticate(username=u,password=p)
        if user:
            login(request,user)
            return redirect('shop:allcategory')
        else:
            messages.error(request,'Invalid credentials')
    return render(request,'login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect('shop:login')



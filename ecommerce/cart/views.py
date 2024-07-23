from django.shortcuts import render,HttpResponse,redirect
from shop.models import Products
from cart.models import Cart,Payment,Order_table
from django.contrib.auth.decorators import login_required
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import login


# Create your views here.

@login_required
def addtocart(request,pk):
    p=Products.objects.get(id=pk)
    u=request.user
    try:
        cart=Cart.objects.get(user=u,product=p)
        if(p.stock>0):
            cart.quantity += 1
            cart.save()
            p.stock -= 1
            p.save()

    except:
        if(p.stock):
            cart=Cart.objects.create(product=p,user=u,quantity=1)
            cart.save()
            p.stock -= 1
            p.save()

    return redirect('cart:cartview')

@login_required
def cartview(request):
    u=request.user
    cart=Cart.objects.filter(user=u)
    total=0
    for i in cart:
        total=total+i.quantity*i.product.price

    return render(request,'cartview.html',{'cart':cart,'total':total})

@login_required
def cart_decrement(request,pk):
    p=Products.objects.get(id=pk)
    u=request.user
    try:
        cart = Cart.objects.get(user=u, product=p)
        if(cart.quantity > 1):

            cart.quantity -= 1
            cart.save()
            p.stock += 1
            p.save()
        else:
            cart.delete()
            p.stock +=1
            p.save()
    except:
        pass

    return redirect('cart:cartview')

@login_required
def cart_remove(request,pk):
    p = Products.objects.get(id=pk)
    u = request.user
    try:
        cart = Cart.objects.get(user=u, product=p)
        cart.delete()
        p.stock += cart.quantity
        p.save()
    except:
        pass

    return redirect('cart:cartview')

@login_required

def orderform(request):
    if (request.method=='POST'):
        ph=request.POST['cn']
        a=request.POST['a']
        pin=request.POST['pin']
        u = request.user
        c=Cart.objects.filter(user=u)
        total=0
        for i in c:
            total=(total+(i.quantity*i.product.price))
        total=int(total*100) #convert the total rupees into paisa
        # print(total)
        # print(type(total))
        # create razorpay client
        client=razorpay.Client(auth=('rzp_test_1zd209HZvyBUMA','XNSuoLScrpoWw3daQ2fdaBTt'))
        # #create order
        response_payment=client.order.create(dict(amount=total,currency='INR'))
        print(response_payment)
        order_id=response_payment['id']
        order_status=response_payment['status']
        if order_status=='created':
            p=Payment.objects.create(name=u.username,amount=total,order_id=order_id)
            p.save()
            for i in c:
                o=Order_table.objects.create(user=u,product=i.product,address=a,phone=ph,pin=pin,no_of_items=i.quantity,order_id=order_id)
                o.save()

        response_payment['name']=u.username
        return render(request, 'payment.html',{'payment':response_payment})
    return render(request,'placeorder.html')

@csrf_exempt
def payment_status(request,u):
    print(request.user.is_authenticated)
    if not  request.user.is_authenticated:
        user= User.objects.get(username=u)
        login(request,user)
        print(request.user.is_authenticated)


    if(request.method=="POST"):
        response=request.POST
        # print(response)
        # print(u)
        param_dict={
        'razorpay_order_id':response['razorpay_order_id'],
        'razorpay_payment_id':response['razorpay_payment_id'],
        'razorpay_signature':response['razorpay_signature']

        }
        client = razorpay.Client(auth=('rzp_test_1zd209HZvyBUMA', 'XNSuoLScrpoWw3daQ2fdaBTt'))
        try:
            status=client.utility.verify_payment_signature(param_dict) #to check the authenticity of razorpay signature
            # print(status)
            #After successful payment

            #retrive paymnent record with a particular order_id
            ord = Payment.objects.get(order_id=response['razorpay_order_id'])
            ord.razorpay_payment_id=response['razorpay_payment_id']
            ord.paid=True
            ord.save()

            u=User.objects.get(username=u)
            c=Cart.objects.filter(user=u)

            #filter the order_table details with particular user with order_id
            o=Order_table.objects.filter(user=u,order_id=response['razorpay_order_id'])
            for i in o:
                i.payment_status="paid"
                i.save()
            c.delete() #delete the cart items for particular user
            return render(request, 'payment_status.html',{'status':True})

        except:
            return render(request, 'payment_status.html',{'status':False})



    return render(request,'payment_status.html')

@login_required
def orderview(request):
    u=request.user
    orders=Order_table.objects.filter(user=u,payment_status='paid')

    return render(request,'orderview.html',{'orders':orders,'u':u.username})



from django.shortcuts import render
from shop.models import Products
from django.db.models import Q
# Create your views here.

def search_products(request):
    p=None
    query=""
    if (request.method=="POST"):
        query=request.POST['q']
        if query:
            p=Products.objects.filter(Q(name__icontains=query) | Q(price__icontains=query))

    return render(request,'search_product.html',{'p':p,'query':query})


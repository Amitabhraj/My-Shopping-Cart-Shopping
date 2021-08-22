from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import Product,Contact,Order
from math import ceil
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout

# Create your views here.

def index(request):
    products= Product.objects.all()
    allprods=[]
    catprods= Product.objects.values('category', 'id')
    cats= {item["category"] for item in catprods}
    for cat in cats:
        prod=Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allprods.append([prod, range(1, nSlides), nSlides])
    params={'allprods':allprods}
    return render(request, 'shop/index.html', params)






def about(requests):
    return render(requests,"shop/about.html")






def contact(request):
    if request.method=="POST":
        name=request.POST.get('name', '')
        email=request.POST.get('email', '')
        phone=request.POST.get('phone', '')
        des=request.POST.get('des', '')
        contact = Contact(name=name, email=email, phone=phone, des=des)
        contact.save()
        return redirect("success1")
    return render(request, "shop/contact.html")





def search(requests):
   return render(requests,'shop/search.html')






def prodview(requests, myid):
    product = Product.objects.filter(id=myid)
    return render(requests,'shop/prodview.html', {'product':product[0]})





def order(request, myid):
    if request.method=="POST":
        name=request.POST.get('name', '')
        email=request.POST.get('email', '')
        address1=request.POST.get('address1', '')
        address2=request.POST.get('address2', '')
        city=request.POST.get('city','')
        state=request.POST.get('state','')
        zip=request.POST.get('zip','')
        phone=request.POST.get('phone','')
        order_method=request.POST.get('order_method','')
        order_d=request.POST.get('order','')
        
        order = Order(name=name, email=email,  address1=address1, address2=address2, city=city, state=state, zip=zip, phone=phone,order_method=order_method,order=order_d)
        order.save()
        return redirect("success")
    product = Product.objects.filter(id=myid)
    return render(request,'shop/order.html', {'product':product[0]})






 
def sellproduct(request):
    if request.method == 'POST':
        form = MyfileUploadForm(request.POST, request.FILES)
        
        if form.is_valid():
            name = form.cleaned_data['file_name']
            category = form.cleaned_data['file_category']
            subcategory = form.cleaned_data['file_subcategory']
            price = form.cleaned_data['file_price']
            des = form.cleaned_data['file_des']
            the_files = form.cleaned_data['files_data']

            Product(product_name=name, category=category, subcategory=subcategory, price=price ,des=des, image=the_files).save()
            return redirect("success2")
        
        else:
            return HttpResponse('<h1>Error</h1>')
    else:
        context = {
            'form':MyfileUploadForm()
        }
        return render(request, 'shop/sellproduct.html', context)
        





def show_file(request):
    all_data = Product.objects.all()
    context = {
        'data':all_data 
        }

    return render(request, 'shop/view.html', context)




def profile(request):
    return render(request, 'shop/profile.html')





def delete(request, myid):
    data=Product.objects.filter(id=myid)
    data.delete()
    return redirect('/shop/view')







def success(request):
    return render(request,'shop/success.html')


def success1(request):
    return render(request,'shop/success1.html')


def success2(request):
    return render(request,'shop/success2.html')
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import Product
from .models import Contact
from .models import Order
from django.db.models import Count
from math import ceil
from .forms import *
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.models import *
from django.contrib.auth import authenticate, logout
# Create your views here.



def index(request):
    allprods=[]
    catprods= Product.objects.values('category', 'id')
    cats= {item["category"] for item in catprods}
    for cat in cats:
        prod=Product.objects.filter(category=cat)[::-1][:3]
        allprods.append(prod)
    if request.method == "POST":
        cart_id=request.POST.get('cart_id','')
        image_p=request.POST.get('image_p','')
        name_p=request.POST.get('name_p','')
        price_p=request.POST.get('price_p','')
        product_id=request.POST.get('product_id','')
        quantity=request.POST.get('quantity','')
        cart=Cart(cart_id=cart_id,image_p=image_p,name_p=name_p,price_p=price_p,product_id=product_id,quantity=quantity)
        cart.save()
        return redirect('cart')
    return render(request, 'shop/index.html',{'allprods':allprods})






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







def prodview(request, myid):
    if request.method == "POST":
        cart_id=request.POST.get('cart_id','')
        image_p=request.POST.get('image_p','')
        name_p=request.POST.get('name_p','')
        price_p=request.POST.get('price_p','')
        product_id=request.POST.get('product_id','')
        quantity=request.POST.get('quantity','')
        cart=Cart(cart_id=cart_id,image_p=image_p,name_p=name_p,price_p=price_p,product_id=product_id,quantity=quantity)
        cart.save()
        return redirect('cart')
    product = Product.objects.filter(id=myid)
    prod=Product.objects.all()
    return render(request,'shop/prodview.html', {'product':product[0],'prod':prod})



# order_id=[]
# for order in Order.objects.all():
#     order_id.append(order.id)
# last_order_id=order_id[len(order_id)-1]
# print(last_order_id)
# last_order_id_plus=last_order_id+1

from django.views.decorators.csrf import csrf_exempt
from shop.paytm import Checksum
MERCHANT_KEY = 'bKMfNxPPf_QdZppa'

def order(request, myid):
    if request.method=="POST":
        product_image=request.POST.get('product_image', '')
        product_name=request.POST.get('product_name', '')
        product_price=request.POST.get('product_price', '')
        name=request.POST.get('name', '')
        email=request.POST.get('email', '')
        address1=request.POST.get('address1', '')
        address2=request.POST.get('address2', '')
        city=request.POST.get('city','')
        state=request.POST.get('state','')
        zip=request.POST.get('zip','')
        phone=request.POST.get('phone','')
        order_method=request.POST.get('order_method','')
        product_id=request.POST.get('product_id','')
        admin_id=request.POST.get('admin_id','')
        user_uid=request.POST.get('user_uid','')
        order_status=request.POST.get('order_status','')
        
        order = Order(product_image=product_image,
        product_price=product_price,
        product_name=product_name,
        name=name,
        email=email,  
        address1=address1, 
        address2=address2, 
        city=city, state=state, 
        zip=zip, 
        phone=phone,
        order_method=order_method,
        product_id=product_id,
        admin_id=admin_id,
        user_uid=user_uid,
        order_status=order_status)
        order.save()

        if order.order_method == "CARD METHOD":
            string_amount=order.product_price
            spliting_amount=string_amount.split('₹')
            real_amount=spliting_amount[1]

            param_dict = {
                    'ORDER_ID': 'OREDR_ID-'+ str(order.id),
                    'MID':'DIY12386817555501617',
                    'TXN_AMOUNT': real_amount,
                    'CUST_ID': email,
                    'INDUSTRY_TYPE_ID': 'Retail',
                    'WEBSITE': 'WEBSTAGING',
                    'CHANNEL_ID': 'WEB',
                    # 'CALLBACK_URL':'http://localhost:4000/shop/handlerequest/',
                    'CALLBACK_URL':'https://MyAwesomeCartShopping.pythonanywhere.com/shop/handlerequest/',
            }
            param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
            return render(request, 'shop/paytm.html', {'param_dict': param_dict})
        else:
            return redirect('/shop/success')

    product = Product.objects.filter(id=myid)
    return render(request,'shop/order.html', {'product':product[0]})


@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because ' + response_dict['RESPMSG'])
    return render(request, 'shop/paymentstatus.html', {'response': response_dict})





 
def sellproduct(request):
    if request.method == 'POST':
        form = MyfileUploadForm(request.POST, request.FILES)
        
        if form.is_valid():
            name = form.cleaned_data['file_name']
            category = form.cleaned_data['file_category']
            subcategory = form.cleaned_data['file_subcategory']
            price = form.cleaned_data['file_price']
            des = request.POST.get('des','')
            admin_id=form.cleaned_data['file_id']
            the_files = form.cleaned_data['files_data']

            Product(product_name=name, category=category, subcategory=subcategory, price=price ,des=des,admin_id=admin_id, image=the_files).save()
            return redirect("success2")
        
        else:
            return HttpResponse('<h1>Error</h1>')
    else:
        context = {
            'form':MyfileUploadForm()
        }
        return render(request, 'shop/sellproduct.html', context)
        





def show_file(request):
    product = Product.objects.all()
    paginator=Paginator(product,12)
    page_number = request.GET.get('page', 1)
    try:
        page = paginator.page(page_number)
    except EmptyPage:
        page = paginator.page(1)
    context = {'data':page }
    return render(request, 'shop/view.html', context)




def profile(request):
    return render(request, 'shop/profile.html')




def vieworder(requests):
    order= Order.objects.all()
    context={'order':order}
    return render(requests, 'shop/vieworder.html',context)




def orderrequest(requests):
    order= Order.objects.all()
    context={'order':order}
    return render(requests, 'shop/orderrequest.html',context)





def destroy(request,myid):  
    order = Order.objects.get(id=myid)  
    order.delete()  
    return redirect("/shop/vieworder") 


def moredetail(requests,myid):
    order= Order.objects.filter(id=myid)
    context={'order':order[0]}
    return render(requests, 'shop/moredetail.html',context)


def delete(request,myid):  
    product = Product.objects.get(id=myid)  
    product.delete()  
    return redirect("/shop/yourproduct")  





def search(request):
    if request.method == "POST":
        cart_id=request.POST.get('cart_id','')
        image_p=request.POST.get('image_p','')
        name_p=request.POST.get('name_p','')
        price_p=request.POST.get('price_p','')
        product_id=request.POST.get('product_id','')
        quantity=request.POST.get('quantity','')
        cart=Cart(cart_id=cart_id,image_p=image_p,name_p=name_p,price_p=price_p,product_id=product_id,quantity=quantity)
        cart.save()
        return redirect('cart')
    search=request.GET['search']
    product= Product.objects.filter(product_name__icontains=search)
    paginator=Paginator(product,12)
    page_number = request.GET.get('page', 1)
    try:
        page = paginator.page(page_number)
    except EmptyPage:
        page = paginator.page(1)
    params={'product': page,'search':search}
    return render(request, 'shop/search.html', params)




def yourproduct(requests):
    product = Product.objects.all()
    context={'product':product}
    return render(requests, 'shop/yourproduct.html',context)




def edit(request,myid):  
    product = Product.objects.get(id=myid)  
    return render(request,'shop/edit.html', {'product':product}) 



def update(request,myid):
    product = Product.objects.get(id=myid)
    product.product_name = request.POST['product_name']
    product.category = request.POST['category']
    product.subcategory = request.POST['subcategory']
    product.price = request.POST['price']
    product.des = request.POST['des']
    product.save()
    return redirect('/shop/yourproduct')



def update2(request,myid):
    order = Order.objects.get(id=myid)
    order.order_status = request.POST['order_status']
    order.save()
    return redirect('/shop/orderrequest')





def cart(request):
    cart=Cart.objects.all()
    context={'cart':cart}
    return render(request,'shop/cart.html',context) 


def cart_delete(request,myid):
    cart_delete = Cart.objects.get(id=myid)  
    cart_delete.delete() 
    return redirect('cart') 
    return render(request,'shop/cart.html')




def success(request):
    return render(request,'shop/success.html')


def success1(request):
    return render(request,'shop/success1.html')


def success2(request):
    return render(request,'shop/success2.html')

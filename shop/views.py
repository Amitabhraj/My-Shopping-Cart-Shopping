from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import numpy as np
from matplotlib import pyplot as plt
from email.mime.image import MIMEImage
import smtplib
import os
from django.core import mail
from .models import *
import random
from django.core.files.base import ContentFile
from django.core.mail import send_mail,EmailMessage,EmailMultiAlternatives
import math
import razorpay
from django.db.models import Count
from django.core.files.storage import default_storage
from math import ceil
from django.views.decorators.csrf import csrf_exempt
from .forms import *
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.models import *
from django.db.models import Count
from django.contrib.auth import login, authenticate, logout
from django.template import RequestContext
from django.contrib import messages
from googlevoice import Voice
from googlevoice.util import input
from mac.settings import EMAIL_HOST_USER,EMAIL_HOST_PASSWORD,BASE_DIR
from random import randint
from sms import send_sms

# Create your views here.


def generateOTP_forget_password() :
     digits = "0123456789"
     OTP = ""
     for i in range(5) :
         OTP += digits[math.floor(random.random() * 10)]
     return OTP


def generateOTP() :
     digits = "0123456789"
     OTP = ""
     for i in range(5) :
         OTP += digits[math.floor(random.random() * 10)]
     return OTP




def login_page(request):
    if request.user.is_authenticated:
        return redirect('/shop')
    if request.method=="POST":
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        if User.objects.filter(username=username):
            u_d=User.objects.get(username=username)
            user_password = u_d.check_password(password)
        else:
            user_password=False

        if User.objects.filter(username=username) and user_password==True:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/shop/starter")
            else:
                messages.error(request,"Invalid username or password.")
                return redirect(request.path)
        else:
            messages.error(request,"Invalid username or password.")
            return redirect(request.path)
    
    return render(request, 'accounts/login.html')




def register(request):
    if request.user.is_authenticated:
        return redirect('/shop')
    else:
        if request.method=="POST":
            username=request.POST.get('username', '')
            password=request.POST.get('password','')
            re_password=request.POST.get('re-password','')
            email=request.POST.get('email','')
            phone_number=request.POST.get('phone_number','')

            username_match=User.objects.filter(username=username)
            email_match=User.objects.filter(email=email)

            if username_match:
                messages.error(request,"Username Already Taken")
                return redirect(request.path)

            elif email_match:
                messages.error(request,"Email Already Taken")
                return redirect(request.path)

            elif password!=re_password:
                messages.error(request,"Password Do not Match!")
                return redirect(request.path)

            elif len(str(phone_number))<=9 or len(str(phone_number))>=11:
                messages.error(request,"Phone Number Should be 10 Digits")
                return redirect(request.path)
        

            elif not username_match and not email_match and password==re_password:
                random_str=generateOTP()
                send_mail(
                    'Thank You For Register in MyAwesomeCart, Find OTP',
                    f"This is the OTP for Getting Register in MyAwesomeCart:- {random_str}, Please Don't Share With Anyone",
                    'abhiraj1709w@gmail.com',
                    [f'{email}'],
                    fail_silently=False,
                )
                # print(random_str)
                if Register_Attempt.objects.filter(username=username, email=email):
                    reg_at=Register_Attempt.objects.get(username=username, email=email)
                    reg_at.password=password
                    reg_at.phone_number=phone_number
                    reg_at.otp=random_str
                    reg_at.save()
                    # print(reg_at.otp)
                else:
                    register_attempt=Register_Attempt(username=username,
                                                      email=email,
                                                      password=password,
                                                      phone_number=phone_number,
                                                      otp=random_str)
                    register_attempt.save()
                    # print(Register_Attempt.objects.get(username=username).otp)
                print('Successfully Mailed & saved Otp in database')
                status=True
                context={'status':status,'email':email,'username':username,'password':password}
                return render(request,'accounts/register.html',context)
            else:
                return HttpResponse('</h1>Error</h1>')
    return render(request, 'accounts/register.html')



@csrf_exempt
def verify_otp(request):
    response=request.POST
    otp=Register_Attempt.objects.get(username=response['username']).otp
    register_user=Register_Attempt.objects.get(username=response['username'])
    if request.method=="POST":
        if response['otp']==str(otp):
            user_detail=User.objects.create_user(username=response['username'],
                             password=response['password'],email=response['email'])
            user_detail.save()
            register_user.successfully_register=True
            register_user.save()
            messages.info(request,'You are Successfully Register, Please Login')
            return redirect('/shop/login')
        else:
            messages.info(request,'Incorrect OTP, Try Registration Again!')
            return redirect('/shop/register')
    return render(request, 'shop/verify_otp.html')




def forget_password(request):
    global otp_num
    global username
    global password
    if request.method=="POST":
        if not request.POST.get('otp', ''):
            otp_num= str(generateOTP_forget_password())
            print("otp_Num = "+otp_num)
            username=request.POST.get('username', '')
            password=request.POST.get('password', '')
            re_password=request.POST.get('re-password', '')

            if not User.objects.filter(username=username):
                messages.error(request,'you have Entered Wrong Username')
                return redirect('/shop/forget_password')
            elif password != re_password:
                messages.error(request,'Password Do Not Match')
                return redirect('/shop/forget_password')
            else:
                email_id=User.objects.get(username__exact=username).email
                subject = 'You are requested for set new password, here is your OTP:-'
                plain_message = f'this is your otp:- {otp_num}'
                from_email = 'abhiraj1709w@gmail.com'
                to = f'{email_id}'
                mail.send_mail(subject, plain_message, from_email, [to])
                
                status=200
                context={'status':status}
                return render(request, 'accounts/forget_password.html',context)
        else:
            otp = str(request.POST.get('otp', ''))
            if otp == otp_num:
                print("you have entered right otp")
                user_name=User.objects.get(username__exact=username)
                user_name.set_password(password)
                user_name.save()
                messages.success(request, 'You have Successfully Reset Your password')
                return redirect('/shop/login')
                
            else:
                print("you have not entered right otp")
                messages.error(request, 'You have not Entered Right OTP')
                return redirect('/shop/forget_password')
    else:
        status = 100
        context={'status':status}
        return render(request, 'accounts/forget_password.html',context)
    return render(request, 'accounts/forget_password.html')






#buyer
def starter(request):
    if request.method == "POST":
        search=request.POST.get('search','')
        print(search)
        product= Product.objects.filter(product_name__icontains=search, on_sale=True)
        context={'product':product}
        return render(request,'shop/search.html',context)
    return render(request, 'starter.html')




def dashboard(requests):
    user=requests.user
    product_count=Product.objects.filter(admin_id=user.id)
    product=Product.objects.filter(admin_id=user.id)[::-1][:5]


    arg1="<hr style='border-top: 2px solid black;'><marquee scrollamount='15'><h2>Welcome To Seller Dashboard</h2></marquee><hr style='border-top: 2px solid black;>'>"

    arg="You Have Not Added any Product For Sale yet, add your Product to Start Your Business on MyAwesomeCart"
    button="<a href='/shop/sellproduct' class='btn btn-secondary'>Sell Your Product</a>"
    

    if product_count:
        context={'product':product,'arg1':arg1}
    else:
        context={'arg':arg,'button':button}
    return render(requests,'shop/dashboard.html',context)



def index(request):
    allprods=[]
    filter_product=Product.objects.filter(on_sale=True)
    catprods= filter_product.values('category', 'id')
    cats= {item["category"] for item in catprods}
    for cat in cats:
        prod=Product.objects.filter(category=cat,on_sale=True)[::-1][:5]
        allprods.append(prod)
    user=request.user
    if request.method == "POST":
        cart_id=request.POST.get('cart_id','')
        image_p=request.POST.get('image_p','')
        name_pp=request.POST.get('name_p','')
        price_p=request.POST.get('price_p','')
        product_id=request.POST.get('product_id','')
        quantity=request.POST.get('quantity','')
        user_id=request.POST.get('user_id',f'{user.id}')

        name_p=Product.objects.get(id=name_pp,on_sale=True)

        cart=Cart(
            cart_id=cart_id,
            image_of_product=image_p,
            product_name=name_p,
            price_of_the_product=price_p,
            product_id=product_id,
            quantity=quantity,
            user_id=user_id)
        cart.save()
        return redirect('cart')
    return render(request, 'shop/index.html',{'allprods':allprods})



def check_login(request):
    if request.user.is_authenticated:
        return redirect('/shop')
    return render(request, 'accounts/login.html')




def about(requests):
    return render(requests,"shop/about.html")




def contact(request):
    contact_idd=Contact.objects.all()
    if contact_idd.count()==0:
        demo_contact=Contact(name="demo", email="demo@gmail.com", phone="demo_phone_number", des="demo", contact_id=0)
        demo_contact.save()
        integer_contact_id=int(demo_contact.id)+1
    else:
        contact_id=contact_idd[len(contact_idd)-1].id
        integer_contact_id=int(contact_id)+1

    context={"contact_id":integer_contact_id}
    if request.method=="POST":
        name=request.POST.get('name', '')
        email=request.POST.get('email', '')
        phone=request.POST.get('phone', '')
        des=request.POST.get('des', '')
        contact_id=request.POST.get('contact_id','')
        contact = Contact(name=name, email=email, phone=phone, des=des, contact_id=contact_id)
        if Contact.objects.filter(id=contact_id):
            return redirect(request.path)
        else:
            contact.save()
            main_context="Submitted"
            line_context="You Have Successfully Submitted"
            last_context="Thank You! We will Soon Contact on Your Email-Id"
            context={'main_context':main_context,'line_context':line_context,'last_context':last_context}
            return render(request,"shop/success.html",context)
    return render(request, "shop/contact.html",context)



def seller_contact(request):
    contact_idd=Contact.objects.all()
    if contact_idd.count()==0:
        demo_contact=Contact(name="demo", email="demo@gmail.com", phone="demo_phone_number", des="demo", contact_id=0)
        demo_contact.save()
        integer_contact_id=int(demo_contact.id)+1
    else:
        contact_id=contact_idd[len(contact_idd)-1].id
        integer_contact_id=int(contact_id)+1

    context={"contact_id":integer_contact_id}
    if request.method=="POST":
        name=request.POST.get('name', '')
        email=request.POST.get('email', '')
        phone=request.POST.get('phone', '')
        des=request.POST.get('des', '')
        contact_id=request.POST.get('contact_id','')
        contact = Contact(name=name, email=email, phone=phone, des=des, contact_id=contact_id)
        if Contact.objects.filter(id=contact_id):
            return redirect(request.path)
        else:
            contact.save()
            main_context="Submitted"
            line_context="You Have Successfully Submitted"
            last_context="Thank You! We will Soon Contact on Your Email-Id"
            context={'main_context':main_context,'line_context':line_context,'last_context':last_context}
            return render(request, "shop/success.html",context)
    return render(request, "shop/seller_contactus.html",context)







def prodview(request, myid):
    user=request.user
    if request.method == "POST":
        cart_id=request.POST.get('cart_id','')
        image_of_product=request.POST.get('image_p','')
        product_name=request.POST.get('name_p','')
        price_of_the_product=request.POST.get('price_p','')
        product_id=request.POST.get('product_id','')
        quantity=request.POST.get('quantity','')
        user_id=request.POST.get('user_id',f'{user.id}')
        cart=Cart(cart_id=cart_id,image_of_product=image_of_product,product_name=product_name,price_of_the_product=price_of_the_product,product_id=product_id,quantity=quantity,user_id=user_id)
        cart.save()
        return redirect('cart')
    product = Product.objects.filter(id=myid,on_sale=True)
    prod=Product.objects.filter(on_sale=True)
    return render(request,'shop/prodview.html', {'product':product[0],'prod':prod})



def show_file(request):
    product = Product.objects.filter(on_sale=True)
    paginator=Paginator(product,12)
    page_number = request.GET.get('page', 1)
    try:
        page = paginator.page(page_number)
    except EmptyPage:
        page = paginator.page(1)
    context = {'data':page }
    return render(request, 'shop/view.html', context)






def order(request, myid):
    order_idd=Order.objects.all()
    if order_idd.count()==0:
        demo_order=Order(product_image=None,
                         product_price=999,
                         product_name=None,
                         admin_id=0,
                         user_uid=0
                         )
        demo_order.save()
        integer_order_id=int(demo_order.id)+1
    else:
        order_id=order_idd[len(order_idd)-1].id
        integer_order_id=int(order_id)+1

    if request.method=="POST":
        product_image=request.POST.get('product_image', '')
        product_namee=request.POST.get('product_name', '')
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
        order_id=request.POST.get('order_id','')


        product_name=Product.objects.get(id=product_namee)
        
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
        order_id=order_id,
        paid=False,
        transaction_id="")
        if Order.objects.filter(id=order_id):
            return redirect(request.path)
        else:
            if order.order_method=="CASH ON DELIVERY":
                if Order.objects.filter(order_id=integer_order_id):
                    return redirect(request.path)
                else:
                    order.paid=True
                    order.save()
                    main_context="Ordered"
                    line_context="You Have Successfully Ordered the Product"
                    last_context="Thank You! We will Deliver You the product at your Home very Soon.."
                    context={'main_context':main_context,'line_context':line_context,'last_context':last_context}
                    return render(request,"shop/success.html",context)
            else:
                if Order.objects.filter(order_id=integer_order_id):
                    return redirect(request.path)
                else: 
                    amount_1=order.product_price.split('₹')
                    amount_in_int=int(amount_1[1])
                    amount=amount_in_int*10
                    client = razorpay.Client(auth=('rzp_test_RMrYVBgxH8sJdI', 'N8OvdMQXtE7WLVtsO38rNfA5'))
                    response_payment=client.order.create(dict(amount=amount,currency='INR',receipt=order_id, payment_capture=1))
                    order_id=response_payment['id']
                    order.transaction_id=order_id
                    order_status=response_payment['status']
                    if order_status=="created":
                        order.save()
            context={'payment':response_payment}
            return render(request, 'shop/order.html',context)


    product = Product.objects.filter(id=myid,on_sale=True)
    return render(request,'shop/order.html', {'product':product[0],'order_id':integer_order_id})






@csrf_exempt
def handlerequest(request):
    user = request.user
    response=request.POST
    print(response)
    params_dict={
    'razorpay_order_id':response['razorpay_order_id'],
    'razorpay_payment_id':response['razorpay_payment_id'],
    'razorpay_signature':response['razorpay_signature']
    }
    #client instance
    client = razorpay.Client(auth=('rzp_test_RMrYVBgxH8sJdI', 'N8OvdMQXtE7WLVtsO38rNfA5'))
    try:
        status=client.utility.verify_payment_signature(params_dict)
        order=Order.objects.get(transaction_id=response['razorpay_order_id'])
        order.paid=True
        order.save()
        return render(request, 'shop/paymentstatus.html', {'status':True})
    except:
        return render(request, 'shop/paymentstatus.html', {'status':False})




 
def sellproduct(request):
    category=Category.objects.all()
    product_idd=Product.objects.all()
    if product_idd.count()==0:
        demo_product=Product(image=None,
                             product_name="demo",
                             category=None,
                             price=0,
                             admin_id=0,
                             on_sale=False
                            )
        demo_product.save()
        integer_product_id=int(demo_product.id)+1
    else:
        product_id=product_idd[len(product_idd)-1].id
        integer_product_id=int(product_id)+1

    if request.method == 'POST':
        form = MyfileUploadForm(request.POST, request.FILES)
        
        if form.is_valid():
            name = form.cleaned_data['file_name']
            get_category = request.POST.get('category', '')
            price = form.cleaned_data['file_price']
            des = request.POST.get('des','')
            admin_id=form.cleaned_data['file_id']
            the_files = form.cleaned_data['files_data']
            product_id=request.POST.get('product_id','')

            category=Category.objects.get(id=get_category)

            product=Product(product_name=name, category=category, price=price ,des=des,admin_id=admin_id, image=the_files, product_id=product_id)
            if Product.objects.filter(id=product_id):
                return redirect(request.path)
            else:
                product.save()
                main_context="Added"
                line_context="Congratulations! Your Have Successfully Selled a Product"
                last_context="Thank You! For Selling for Choosing us "
                context={'main_context':main_context,'line_context':line_context,'last_context':last_context}
                return render(request, "shop/success.html",context)
        else:
            return HttpResponse('<h1>Error</h1>')
    else:
        context = {
            'form':MyfileUploadForm(),
            'category':category,
            'integer_product_id':integer_product_id
        }
        return render(request, 'shop/sellproduct.html', context)



def vieworder(request):
    user=request.user
    user_order=Order.objects.filter(user_uid=user.id,paid=True)
    my_order=""
    if user_order:
        my_order="yes"
    else:
        my_order="no"


    alert=""
    arr=""
    for order in user_order:
        if order.order_status == "Pending":
            alert="warning"
            arr="Pending"

        elif order.order_status == "Dispatched":
            alert="info"
            arr="Dispatched"

        else:
            alert="success"
            arr="Delivered"



    context={'arr':arr,'alert':alert,'order':user_order, 'my_order':my_order}
    return render(request, 'shop/vieworder.html',context)


def destroy(request,myid):
    if Order.objects.filter(id=myid):
        order=Order.objects.get(id=myid)
        main_context="Cancelled"
        line_context="Your Have Successfully Cancelled your Order"
        context={'main_context':main_context,'line_context':line_context}
        if order.user_uid == request.user.id:
            order.delete()  
            return render(request, 'shop/success.html',context)
        else:
            return redirect("/shop") 
    else:
        return redirect(request.path)






def orderrequest(requests):
    user=requests.user
    order= Order.objects.filter(admin_id=user.id,paid=True)
    order_request=""
    if Order.objects.filter(admin_id=user.id,paid=True):
        order_request="yes"
    else:
        order_request="no"
    context={'order':order, 'order_request':order_request}
    return render(requests, 'shop/orderrequest.html',context)



def moredetail(request,myid):
    if Order.objects.filter(admin_id=request.user.id,id=myid,paid=True):
        order= Order.objects.filter(admin_id=request.user.id,id=myid,paid=True)
        context={'order':order[0]}
    else:
        return redirect('/shop/orderrequest')
    return render(request, 'shop/moredetail.html',context)




def update2(request,myid):
    if Order.objects.filter(admin_id=request.user.id,id=myid,paid=True):
        order = Order.objects.get(admin_id=request.user.id,id=myid,paid=True)
        order.order_status = request.POST['order_status']
        order.save()
    else:
        return redirect('/shop/orderrequest')
    return redirect('/shop/orderrequest')



from taggit.models import Tag

def search(request):
    user=request.user
    if request.method == "POST":
        cart_id=request.POST.get('cart_id','')
        image_of_product=request.POST.get('image_p','')
        product_namee=request.POST.get('name_p','')
        price_of_the_product=request.POST.get('price_p','')
        product_id=request.POST.get('product_id','')
        quantity=request.POST.get('quantity','')
        user_id=request.POST.get('user_id',f'{user.id}')
        product_name=Product.objects.get(id=product_namee)
        cart=Cart(cart_id=cart_id,image_of_product=image_of_product,product_name=product_name,price_of_the_product=price_of_the_product,product_id=product_id,quantity=quantity,user_id=user_id)
        cart.save()
        return redirect('cart')  
    search=request.GET.get('search')
    category_1=Category.objects.all()
    product = Product.objects.filter(product_name__icontains=search,on_sale=True)
    # for products in product:
    #     category=Product.objects.filter(category=products.category,on_sale=True)
    # product=Product.objects.filter(category=search,on_sale=True)
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
    user=requests.user
    your_product=""
    if Product.objects.filter(admin_id=user.id):
        your_product="yes"
    else:
        your_product="no"
    context={'product':product, 'your_product':your_product}
    return render(requests, 'shop/yourproduct.html',context)



def edit(request,myid):  
    if Product.objects.filter(id=myid,admin_id=request.user.id):
        product = Product.objects.get(id=myid,admin_id=request.user.id) 
        product_category = Category.objects.get(category=product.category)
        all_category = Category.objects.all()
    else:
        return redirect('/shop/yourproduct')  
    return render(request,'shop/edit.html', {'product':product, 'product_category':product_category,'all_category':all_category}) 



def update(request,myid):
    if Product.objects.filter(id=myid,admin_id=request.user.id):
        product = Product.objects.get(id=myid)
        product.product_name = request.POST['product_name']
        category = request.POST['category']
        product.category = Category.objects.get(id=category)
        product.price = request.POST['price']
        product.des = request.POST['des']
        sale=request.POST['sale']
        if sale=="On Sale":
            product.on_sale=True
        else:
            product.on_sale=False
        product.save()
    else:
        return redirect(request.path)
    return redirect('/shop/yourproduct')




def delete(request,myid):  
    if Product.objects.filter(id=myid):
        product = Product.objects.get(id=myid)  
        if product.admin_id==request.user.id:
            product.delete()  
            main_context="Deleted"
            line_context=f"Your Have Successfully Deleted {product.product_name} from Your Products"
            context={'main_context':main_context,'line_context':line_context}
            return render(request, 'shop/success.html')
        else:
            return redirect('/shop/yourproduct')  
    else:
        return redirect(request.path)  









def cart(request):
    cart=Cart.objects.all()
    user=request.user
    cartt=Cart.objects.filter(user_id=user.id)

    price_listt = ([(item.price_of_the_product) for item in cartt])

    integer_map = map(int, price_listt)
    price_list = list(integer_map)

    quantity_list = ([(item.quantity) for item in cartt])

    count=len(price_list)

    grand_total=[]
    for i in range(0,count):
        grand_total=price_list[i]*quantity_list[i]
    cart_is=""
    if Cart.objects.filter(cart_id=user.id):
        cart_is="yes"
    else:
        cart_is="no"
    context={'cart':cart, 'cart_is':cart_is,'quantity_list':quantity_list,'price_list':price_list,'grand_total':grand_total}
    return render(request,'shop/cart.html',context) 



def cart_delete(request,myid):
    cart_delete = Cart.objects.get(id=myid)  
    cart_delete.delete() 
    return redirect('cart')
    return render(request,'shop/cart.html')




def my_earning(request):
    order=Order.objects.filter(admin_id=request.user.id, paid=True)
    # order_2 = list(order)
    # print(order_2)
    # order_3 = set(order_2)
    # print("")
    # print("")
    # print(order_3)
    # order_4=list(order_3)
    # qty=[]
    # for order in order:
    #     for order_3 in order_3:
    #         qty.append(order_2.count(order_3))
    #     break

    if order:
        order_product=Order.objects.filter(admin_id=request.user.id, paid=True).values("product_name").annotate(Count("product_name"))
        product_name = Product.objects.all()

        online_payment = len(Order.objects.filter(admin_id=request.user.id, paid=True, order_method="ONLINE PAYMENT"))
        offline_payment = len(Order.objects.filter(admin_id=request.user.id, paid=True, order_method="CASH ON DELIVERY"))

        labels = 'online Payment', 'Cash on Delivery'
        sizes = [online_payment, offline_payment]
        explode = (0.1, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')
        plt.savefig(str(BASE_DIR)+"/media/"+"/shop/earning_chart/earning_chart_"+request.user.username+".png")
    else:
        messages.error(request,'you have not any product')
        return redirect('/shop')
        # , {'order':order_4, 'qty':qty}
    return render(request, 'seller/my_earning.html',{'order':order_product, 'product':product_name})




#admin_panel
def Check_Admin(request):
    group=Group.objects.get(name="admin").id
    if User.objects.filter(id=request.user.id, groups=group):
        return True
    else:
        return False



def admin_panel_dashboard(request):
    if Check_Admin(request):
        return render(request, 'admin_panel/admin_panel_dashboard.html')
    else:
        messages.error(request, 'you cannot access the page')
        return redirect('/shop')



def send_bulk_email(request):
    global bulk_email
    global hh
    if Check_Admin(request):
        if request.method=="POST":
            subject=request.POST.get('subject','')
            main_body=request.POST.get('main_body','')
            attachment=request.FILES.getlist('attachment')
            send_to=request.POST.getlist('send_to','')
            send_to=send_to[0]


            email_attachment=[]
            for attachment in attachment:
                print(attachment)
                bulk_email=Bulk_Email(subject=subject, main_body=main_body, send_to=send_to, attachment=attachment)
                bulk_email.save()
                email_attachment.append(bulk_email.attachment)

            seller_group=Group.objects.get(name="seller").id
            buyer_group=Group.objects.get(name="buyer").id

            if send_to=="seller":
                seller_user=User.objects.filter(groups=seller_group)
                seller_mail=[]
                for seller in seller_user:
                    seller_email.append(seller.email)
                
                email_with_django=EmailMessage(
                    subject,
                    main_body,
                    'abheiraj1709w@gmail.com',
                    seller_email
                    )
                for email_attachment in email_attachment:
                    email_with_django.attach_file(str(BASE_DIR)+"/media/"+str(email_attachment))

                email_with_django.send()
                messages.success(request, 'Successfully Send the Email To All Seller')
                return redirect(request.path)
            


            elif send_to=="buyer":
                buyer_user=User.objects.filter(groups=buyer_group)
                buyer_email=[]
                for buyer in buyer_user:
                    buyer_email.append(buyer.email)
                email_with_django=EmailMessage(
                    subject,
                    main_body,
                    'abhiraj1709w@gmail.com',
                    buyer_email
                    )

                for email_attachment in email_attachment:
                    email_with_django.attach_file(str(BASE_DIR)+"/media/"+str(email_attachment))
                email_with_django.send()
                messages.success(request, 'Successfully Send the Email To All Buyer')
                return redirect(request.path)
            



            elif send_to=="all_user":
                all_user=User.objects.all()
                all_user_email=[]
                for all_user in all_user:
                    all_user_email.append(all_user.email)
                email_with_django=EmailMessage(
                    subject,
                    main_body,
                    'abhiraj1709w@gmail.com',
                    all_user_email
                    )
                for email_attachment in email_attachment:
                    email_with_django.attach_file(str(BASE_DIR)+"/media/"+str(email_attachment))
                email_with_django.send()
                

                messages.success(request, 'Successfully Send the Email To All Buyer')
                return redirect(request.path)
    else:
        messages.error(request, 'you cannot access the page')
        return redirect('/shop')

    return render(request, 'admin_panel/send_bulk_email.html')




def profile(request):
    return render(request, 'shop/profile.html')



def success(request):
    return render(request, 'shop/success.html')


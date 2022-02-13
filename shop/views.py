from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from .models import *
import razorpay
from django.db.models import Count
from math import ceil
from django.views.decorators.csrf import csrf_exempt
from .forms import *
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.models import *
from django.db.models import Count
from django.contrib.auth import login, authenticate, logout
from django.template import RequestContext
from django.contrib import messages
# Create your views here.

from django.contrib.auth.hashers import make_password
import hashlib 

def login_page(request):
    if request.user.is_authenticated:
        return redirect('/shop')
    if request.method=="POST":
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        u_d=User.objects.get(username=username)
        user_password = u_d.check_password(password)

        if u_d and user_password==True:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/shop")
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

            if password==re_password:
                user_detail=User.objects.create_user(username=username,
                                 password=password,
                                 email=email)
                user_detail.save()
                return redirect('/shop/login')
            else:
                return HttpResponse('</h1>Error</h1>')
    return render(request, 'accounts/register.html')


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
                order.paid=True
                order.save()
                main_context="Ordered"
                line_context="You Have Successfully Ordered the Product"
                last_context="Thank You! We will Deliver You the product at your Home very Soon.."
                context={'main_context':main_context,'line_context':line_context,'last_context':last_context}
                return render(request,"shop/success.html",context)
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
    search=request.GET['search']
    category_1=Category.objects.all()
    product = Product.objects.filter(product_name__icontains=search,on_sale=True)
    # for products in product:
    #     category=Product.objects.filter(category=products.category,on_sale=True)
    product=Product.objects.filter(category=search,on_sale=True)
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


def profile(request):
    return render(request, 'shop/profile.html')



def success(request):
    return render(request, 'shop/success.html')


from django.db import migrations,models
import time as _time
import datetime
from django.contrib.auth.models import User
from datetime import timedelta, tzinfo
from threading import local


delivery_status=(
    ("Pending", "Pending"),
    ("Dispatched", "Dispatched"),
    ("Delivered", "Delivered")
    )


class Category(models.Model):
    category=models.CharField(max_length=1000, null=True, blank=True, default="")

    def __str__(self):
        return self.category


# Create your models here.
class Product(models.Model):
    product_name=models.CharField(max_length=150,blank=True,null=True)
    category=models.ForeignKey(Category, on_delete=models.CASCADE,blank=True,null=True)
    price=models.IntegerField(default=0,blank=True,null=True)
    des=models.CharField(max_length=10000,blank=True,null=True)
    admin_id=models.IntegerField(default="",blank=True,null=True)
    image=models.ImageField(upload_to="shop/images", null=True, blank=True) 
    product_id=models.IntegerField(default=0,blank=True,null=True)
    on_sale=models.BooleanField(default=True)
    
    def __str__(self):
        return self.product_name
    
    
    
    
    
class Contact(models.Model):
    name=models.CharField(max_length=50)
    email=models.CharField(max_length=50, default="")
    phone=models.CharField(max_length=50, default="")
    des=models.CharField(max_length=1000, default="")
    contact_id=models.IntegerField(blank=True, null=True, default=0)
    
    def __str__(self):
        return self.name
    
    
    
    

class Order(models.Model):
    product_image=models.ImageField(upload_to="shop/images")
    product_name=models.ForeignKey(Product, on_delete=models.CASCADE,blank=True,null=True)
    product_price=models.CharField(max_length=200)
    name=models.CharField(max_length=50)
    email=models.CharField(max_length=50, default="",blank=True,null=True)
    address1=models.CharField(max_length=100, default="")
    address2=models.CharField(max_length=400, default="")
    city=models.CharField(max_length=100, default="")
    state=models.CharField(max_length=50, default="")
    zip=models.IntegerField(default=0,blank=True,null=True)
    phone=models.CharField(max_length=10,default="0")
    order_method=models.CharField(max_length=50, default="")
    product_id=models.IntegerField(default=0,blank=True,null=True)
    admin_id=models.IntegerField(default=0,blank=True,null=True)
    user_uid=models.IntegerField(default=0,blank=True,null=True)
    transaction_id=models.CharField(default="",max_length=10000, blank=True,null=True)
    paid=models.BooleanField(default=False)

    order_status=models.CharField(choices=delivery_status, default="Pending", max_length=200)
    order_id=models.IntegerField(blank=True, null=True, default=0)

    def get_id_count(self):
        return self.id


    def __str__(self):
        return "(Email Id:-)"+self.email+"~~~~~~~~~~~~"+"(Product ID:-)"+str(self.product_id)



class Cart(models.Model):
    image_of_product=models.ImageField(upload_to="shop/images")
    cart_id=models.IntegerField(default=0)
    product_name=models.ForeignKey(Product, on_delete=models.CASCADE, default=None)
    price_of_the_product=models.CharField(default="0", max_length=100000000)
    product_id=models.IntegerField(default=0)
    quantity=models.IntegerField(default=1)
    user_id=models.IntegerField(default=0)


    def __str__(self):
        return str(self.product_name) if self.product_name else ''

        



class Bulk_Email(models.Model):
    subject=models.CharField(max_length=250,blank=True,null=True)
    main_body=models.CharField(max_length=550,blank=True,null=True)
    send_to=models.CharField(max_length=250,blank=True,null=True)
    attachment=models.FileField(max_length=1000000,upload_to="shop/bulk_email_file", null=True, blank=True) 
  
    def __str__(self):
        return self.subject
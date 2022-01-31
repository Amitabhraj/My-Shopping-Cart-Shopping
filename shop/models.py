from django.db import migrations,models
import time as _time
import datetime
from datetime import timedelta, tzinfo
from threading import local



delivery_status=(
    ("Pending", "Pending"),
    ("Dispatched", "Dispatched"),
    ("Delivered", "Delivered")
    )


# Create your models here.
class Product(models.Model):
    product_id=models.AutoField
    product_name=models.CharField(max_length=150)
    category=models.CharField(max_length=30, default="")
    subcategory=models.CharField(max_length=50, default="")
    price=models.IntegerField(default=0)
    des=models.CharField(max_length=10000)
    admin_id=models.IntegerField(default="")
    image=models.ImageField(upload_to="media/shop/images") 
    
    def __str__(self):
        return self.product_name
    
    
    
    
    
class Contact(models.Model):
    name=models.CharField(max_length=50)
    email=models.CharField(max_length=50, default="")
    phone=models.CharField(max_length=50, default="")
    des=models.CharField(max_length=1000, default="")
    
    def __str__(self):
        return self.name
    
    
    
    

class Order(models.Model):
    product_image=models.ImageField(upload_to="media/shop/images")
    product_name=models.ForeignKey(Product, on_delete=models.CASCADE)
    product_price=models.CharField(max_length=200)
    name=models.CharField(max_length=50)
    email=models.CharField(max_length=50, default="")
    address1=models.CharField(max_length=100, default="")
    address2=models.CharField(max_length=400, default="")
    city=models.CharField(max_length=100, default="")
    state=models.CharField(max_length=50, default="")
    zip=models.IntegerField(default=0)
    phone=models.CharField(max_length=10,default="0")
    order_method=models.CharField(max_length=50, default="")
    product_id=models.IntegerField(default=0)
    admin_id=models.IntegerField(default="")
    user_uid=models.IntegerField(default=0)
    paid=models.BooleanField(default=False)

    order_status=models.CharField(choices=delivery_status, default="Pending", max_length=200)


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

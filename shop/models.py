from sqlite3 import Timestamp
from django.db import models

# Create your models here.

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_cat = models.CharField(max_length= 100)
    product_subcat = models.CharField(max_length= 100)
    product_name = models.CharField(max_length = 50)
    product_price = models.IntegerField()
    product_desc = models.CharField(max_length= 300)
    product_date = models.DateField()
    product_image = models.ImageField(upload_to = 'shop/images' , default = " " )

    def __str__(self):
        return self.product_name 

class Contact(models.Model):
    user_id = models.AutoField(primary_key=True)
    contact_name = models.CharField(max_length = 50)
    contact_email = models.CharField(max_length=50)
    contact_phone = models.IntegerField()
    contact_desc = models.CharField(max_length=10000)

    def __str__(self):
        return self.contact_name

# for checkout page
class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    itemJson= models.CharField(max_length=100)
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=100)
    tel = models.CharField(max_length=10 , default=" ")
    address = models.CharField(max_length=100) 
    state = models.CharField(max_length=100)
    zip = models.CharField(max_length=6)
    amount = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name

# for tracker page
class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.CharField(max_length=100)
    update_desc = models.CharField(max_length=1000000)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:20] + '...'

class AboutUs(models.Model):
    about_id = models.AutoField(primary_key=True)
    Head = models.CharField(max_length=10000)
    HeadMute = models.CharField(max_length=1000, default=" ")
    SHead = models.CharField(max_length=1000000000)
    Image = models.ImageField(upload_to = 'shop/images' , default = " " )

    def __str__(self):
        return self.Head







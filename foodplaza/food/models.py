from django.db import models

# Create your models here.

class Food(models.Model):
    foodid = models.AutoField(primary_key=True)
    foodname = models.CharField(max_length=30)
    foodcat = models.CharField(max_length=30)
    foodtype = models.CharField(max_length=15)
    foodprice = models.FloatField(max_length=15)
    foodquantity = models.IntegerField(default=0)
    foodimg = models.ImageField(upload_to='media', default='')
    class Meta:
        db_table = "Food"

    def __str__(self):
        return self.foodname

class Customer(models.Model):
    custname = models.CharField(max_length=20)
    custemail = models.CharField(max_length=20)
    custpass = models.CharField(max_length=20)
    custcontact = models.CharField(max_length=10)
    custaddress = models.CharField(max_length=30)
    class Meta:
        db_table = "Customer"

    def __str__(self):
        return self.custname

class Admin(models.Model):
    adminname = models.CharField(primary_key=True, max_length=10)
    adminpass = models.CharField(max_length=10)

    class Meta:
        db_table = "Admin"

    def __str__(self):
        return self.adminname

class Cart(models.Model):
    cartid = models.AutoField(primary_key=True)
    custemail = models.CharField(max_length=30)
    fid = models.IntegerField()
    foodqnty = models.IntegerField(default=1)
    total = models.IntegerField(default=0, null=True)

    class Meta:
        db_table = "Cart"

    def __str__(self):
        return self.custemail

class Orders(models.Model):
    orderid = models.AutoField(primary_key=True)
    custemail = models.CharField(max_length=30)
    totalbill = models.IntegerField()
    date = models.CharField(max_length=30)

    class Meta:
        db_table = "Orders"

    def __str__(self):
        return self.custemail

class OrderSummary(models.Model):
    fid = models.IntegerField()
    odrid = models.IntegerField()
    foodquant = models.IntegerField()
    price = models.FloatField()

    class Meta:
        db_table = "OrderSummary"
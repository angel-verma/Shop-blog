from django.db import models


class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default="")
    subcategory = models.CharField(max_length=50)
    price = models.IntegerField()
    desc = models.CharField(max_length=300)
    pub_date = models.DateField()
    image = models.ImageField(upload_to="shop/images")

    def __str__(self):
        return self.product_name


class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default="")
    email = models.CharField(max_length=50, default="")
    phone = models.CharField(max_length=50, default="")
    msg = models.CharField(max_length=500, default="")

    def __str__(self):
        return self.name


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    itemsJson = models.CharField(max_length=5000)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    _zip = models.CharField(max_length=100)
    phone = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.name
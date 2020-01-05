from django.contrib import admin
from .models import Product, Contact, Order, orderUpdate

admin.site.register(Product)
admin.site.register(Contact)
admin.site.register(Order)
admin.site.register(orderUpdate)

from django.contrib import admin
from .models import Food, Customer, Admin, Cart, Orders, OrderSummary

# Register your models here.

admin.site.register(Food)
admin.site.register(Customer)
admin.site.register(Admin)
admin.site.register(Cart)
admin.site.register(Orders)
admin.site.register(OrderSummary)
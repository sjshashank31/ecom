from django.contrib import admin
from .models import Customer, Product, Order, OrderItem, ShippingAddress
# Register your models here.


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'name']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'digital']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'transaction_id', 'date_ordered', 'complete']


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'get_order', 'quantity', 'date_added']

    def get_order(self, obj):
        return obj.order.customer
    get_order.short_description = 'customer'


class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ['customer', 'order', 'zip_code']


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(ShippingAddress ,ShippingAddressAdmin)
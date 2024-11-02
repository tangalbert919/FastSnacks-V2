"""
Admin module for FastSnacks.
Responsible for determining what will appear in the admin panel and how
each of them will appear.
"""

from django.contrib import admin
from .models import Cart, Customer, Favorites, Item, Order, PaymentMethod, \
    Reward, Stock, VendingMachine, SupportTicket

# Admin models should be created here.
class OrderAdmin(admin.ModelAdmin):
    '''Allows for more advanced view of orders in the admin panel.'''
    list_display = ['user', 'machine', 'quantity', 'date', 'price']
    readonly_fields = ['price']

    def price(self, obj):
        '''Fetch the total order price.'''
        return obj.price()
    price.short_description = 'Price'

# All models registered here will be visible in the admin panel.
admin.site.register(Item)
admin.site.register(Order, OrderAdmin)
admin.site.register(VendingMachine)
admin.site.register(Stock)
admin.site.register(Cart)
admin.site.register(PaymentMethod)
admin.site.register(SupportTicket)
admin.site.register(Reward)
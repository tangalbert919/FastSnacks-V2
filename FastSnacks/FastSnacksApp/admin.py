from django.contrib import admin
from .models import *

# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'machine', 'quantity', 'date', 'price']
    readonly_fields = ['price']

    def price(self, obj):
        return obj.price()
    price.short_description = 'Price'

admin.site.register(Item)
admin.site.register(Order, OrderAdmin)
admin.site.register(VendingMachine)
admin.site.register(Stock)
admin.site.register(Cart)
admin.site.register(PaymentMethod)
admin.site.register(SupportTicket)
admin.site.register(Reward)
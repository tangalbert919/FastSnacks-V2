from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Item)
admin.site.register(Order)
admin.site.register(VendingMachine)
admin.site.register(Stock)
admin.site.register(Cart)
admin.site.register(PaymentMethod)
admin.site.register(SupportTicket)
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
# Extend user model
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reward_points = models.IntegerField(default=0)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.customer.save()

class PaymentMethod(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    card_no = models.CharField(max_length=16, null=False)
    security_code = models.CharField(max_length=4, null=False)
    exp_month = models.IntegerField()
    exp_year = models.IntegerField()
    account_bal = models.DecimalField(max_digits=7, decimal_places=2)

class SupportTicket(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    info = models.TextField(max_length=10000)
    date = models.DateField()
    resolved = models.BooleanField(default=False)

class Item(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    # TODO: Merge all of these
    calories = models.IntegerField()
    carbs = models.IntegerField()
    fat = models.IntegerField()
    protein = models.IntegerField()
    sugar = models.IntegerField()

    def __str__(self) -> str:
        return self.name

class VendingMachine(models.Model):
    location = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.location

class Stock(models.Model):
    machine = models.OneToOneField(VendingMachine, on_delete=models.CASCADE)
    item = models.OneToOneField(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()

class Order(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    machine = models.OneToOneField(VendingMachine, on_delete=models.CASCADE)
    item = models.OneToOneField(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date = models.DateField()

class Favorites(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    item = models.OneToOneField(Item, on_delete=models.CASCADE)

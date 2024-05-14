from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
# Extend user model
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reward_points = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.user.get_username()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.customer.save()

class PaymentMethod(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_no = models.CharField(max_length=16, null=False)
    security_code = models.CharField(max_length=4, null=False)
    exp_month = models.IntegerField()
    exp_year = models.IntegerField()
    account_bal = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self) -> str:
        return self.user.get_username() + str(self.pk)

class BillingInformation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2)
    zip = models.IntegerField(validators=
                              [MaxValueValidator(99999),
                               MinValueValidator(1)])

class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.query}"

class SupportTicket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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
    machine = models.ForeignKey(VendingMachine, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    machine = models.ForeignKey(VendingMachine, on_delete=models.CASCADE)
    item = models.ManyToManyField(Item)
    quantity = models.IntegerField()
    date = models.DateTimeField()

    def price(self):
        total = 0.00
        for item in self.item.all():
            total += float(item.price)
        return total

    def description(self):
        description = []
        for item in self.item.all():
            description.append(item.name)
        return ', '.join(description)

class Favorites(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item, blank=True)

    def __str__(self) -> str:
        return self.user.get_username() + "'s favorites"

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item, blank=True)

    def price(self):
        total = 0.00
        for item in self.items.all():
            total += float(item.price)
        return total

    def __str__(self) -> str:
        return self.user.get_username() + "'s cart"

class Reward(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
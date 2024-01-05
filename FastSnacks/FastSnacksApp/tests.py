from django.contrib.auth.models import User
from django.test import TestCase
from FastSnacksApp.models import Customer

# Create your tests here.
class CustomerTest(TestCase):
    def setUp(self):
        User.objects.create(username="asdf",password="$2b$10$bknqYeOqxkynPOZ9HlPlZu31SE7VaJ6Wv8Z83/g441GdJ9UNglM7y",is_superuser=True)

    def test_get_customer(self):
        customer = Customer.objects.get(user=User.objects.get(username="asdf"))
        self.assertEqual(0, customer.reward_points)
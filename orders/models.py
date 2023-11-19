import random
import string

from django.conf import settings
from django.db import models

from shop.models import Product


class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    stripe_id = models.CharField(max_length=250, blank=True)
    token = models.SlugField(max_length=32, blank=True, null=True)


    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]


    def get_total(self):
        return sum(item.get_price() for item in self.items.all())


    def get_stripe_url(self):
        if not self.stripe_id:
            return ''
        if '_test_' in settings.STRIPE_SECRET_KEY:
            path = '/test/'
        else:
            path = '/'

        return f'https://dashboard.stripe.com{path}payments/{self.stripe_id}'
    

    def generate_token(self):
        letters = string.ascii_letters
        digits = string.digits

        random.seed(self.id)

        characters = letters + digits

        token = random.choices(characters, k=32)
        token = ''.join(token)

        return token

    def save(self, **kwargs):
        if not self.token:
            self.token = self.generate_token()
        super(Order, self).save(**kwargs)

    def __str__(self):
        return f'Order {self.id}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_price(self):
        return self.price

    def __str__(self):
        return str(self.id)

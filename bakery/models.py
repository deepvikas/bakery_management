from django.db import models
from users.models import BakeryUser
from django.utils import timezone

# Create your models here.

DISCOUNT_RULE = [
    ('based_on_order', 'Based On Order Amount'),
    ('based_on_quantity', 'Based On Quantity')
]

DISCOUNT_TYPE = [
    ('fixed_price', 'Fixed Price'),
    ('percentage', 'Percentage')
]

class Discount(models.Model):

    discount_rule = models.CharField(max_length=40,choices=DISCOUNT_RULE)
    discount_type = models.CharField(max_length=40,choices=DISCOUNT_TYPE)
    discount_value = models.FloatField()
    message = models.CharField(max_length=200)
    is_enable = models.BooleanField()


class Product(models.Model):

    name = models.CharField(max_length=200)
    cost_price = models.FloatField()
    selling_price = models.FloatField()
    description = models.CharField(max_length=200)
    barcode = models.CharField(max_length=200)
    quantity = models.IntegerField()
    discount_id = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True)


class Order(models.Model):
    
    product_id = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    user_id = models.ForeignKey(BakeryUser, on_delete=models.SET_NULL, null=True)
    amount = models.FloatField()
    order_date = models.DateTimeField(default=timezone.now)



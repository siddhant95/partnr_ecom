import datetime

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Base(models.Model):
    id = models.AutoField(primary_key=True)
    created_on = models.DateTimeField(default=datetime.datetime.now(), editable=False)
    updated_at = models.DateTimeField(default=datetime.datetime.now())

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()
        super(Base, self).save(*args, **kwargs)


class Category(Base):
    name = models.CharField(max_length=50, unique=True)


class Product(Base):
    name = models.CharField(max_length=80, unique=True)
    # Keeping default as 1 rupee rather than free(0.0)
    price = models.FloatField(default=1.0, null=False, blank=False)
    stock = models.IntegerField(default=0, null=False, blank=False)
    category_id = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    is_approved = models.BooleanField(default=False)


class Cart(Base):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False)

    def save(self, *args, **kwargs):
        self.product.stock -= self.quantity
        super(Cart, self).save(*args, **kwargs)

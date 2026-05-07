from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse


# Temporary model
class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=63)
    email = models.EmailField()

    def __str__(self):
        return self.name


class ProductType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'product type'
        verbose_name_plural = 'product types'


class Product(models.Model):
    AVAILABLE = 'A'
    ON_SALE = 'OS'
    OUT_OF_STOCK = 'OOS'
    PRODUCT_STATUS_CHOICES = {
        AVAILABLE: 'Available',
        ON_SALE: 'On Sale',
        OUT_OF_STOCK: 'Out of Stock',
    }

    name = models.CharField(max_length=255)
    type = models.ForeignKey(
        ProductType,
        on_delete=models.SET_NULL,
        related_name='products',
        null=True,
    )
    owner = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='products',
        null=True,
    )
    image = models.ImageField(blank=True)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
    )
    stock = models.IntegerField(validators=[MinValueValidator(0)])
    status = models.CharField(
        max_length=3,
        choices=PRODUCT_STATUS_CHOICES,
        default=AVAILABLE,
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.stock == 0:
            self.status = self.OUT_OF_STOCK

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('merchstore:item_detail', args=[int(self.pk)])

    class Meta:
        ordering = ['name']
        verbose_name = 'product'
        verbose_name_plural = 'products'


class Transaction(models.Model):
    ON_CART = 'OC'
    TO_PAY = 'TP'
    TO_SHIP = 'TS'
    TO_RECEIVE = 'TR'
    DELIVERED = 'D'
    TRANSACTION_STATUS_CHOICES = {
        ON_CART: 'On Cart',
        TO_PAY: 'To Pay',
        TO_SHIP: 'To Ship',
        TO_RECEIVE: 'To Receive',
        DELIVERED: 'Delivered',
    }

    buyer = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        related_name='transactions',
        null=True,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='transactions',
        null=True,
    )
    amount = models.IntegerField(validators=[MinValueValidator(1)])
    status = models.CharField(
        max_length=2,
        choices=TRANSACTION_STATUS_CHOICES,
        default=ON_CART,
    )
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'transaction'
        verbose_name_plural = 'transactions'

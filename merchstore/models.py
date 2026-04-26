from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse


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
    name = models.CharField(max_length=255)
    type = models.ForeignKey(
        ProductType,
        on_delete=models.SET_NULL,
        related_name='products',
        null=True,
    )
    description = models.TextField()
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
    )
    stock = models.IntegerField(
        validators=[MinValueValidator(0)],
    )
    status = models.CharField(
        choices=[
            ("A", "Available"),
            ("OS", "On Sale"),
            ("OOS" "Out of Stock"),
        ]
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('merchstore:item_detail', args=[int(self.pk)])

    class Meta:
        ordering = ['name']
        verbose_name = 'product'
        verbose_name_plural = 'products'


class Transaction(models.Model):
    buyer = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        related_name='profiles',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='products',
        null=True,
    )
    amount = models.IntegerField(
        validators=[MinValueValidator(1)]
    )
    status = models.CharField(
        choices=[
            ("OC", "On Cart"),
            ("TP", "To Pay"),
            ("TS", "To Ship"),
            ("TR", "To Receive"),
            ("D", "Delivered"),
        ]
    )
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'transaction'
        verbose_name_plural = 'transactions'

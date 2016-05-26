from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from category.models import Category


class Product(models.Model):
    product_number = models.IntegerField(verbose_name='Product ID', unique=True, db_index=True)
    name = models.CharField(verbose_name='Product name', max_length=255, db_index=True)

    url = models.URLField(verbose_name='Product URL')

    last_updated = models.DateTimeField(verbose_name='Last updated', auto_now=True)

    volume = models.DecimalField(verbose_name='Volume', max_digits=5, decimal_places=2, db_index=True)
    price = models.DecimalField(verbose_name='Price', max_digits=8, decimal_places=2, db_index=True)
    litre_price = models.DecimalField(verbose_name='Price per litre', max_digits=8, decimal_places=2, db_index=True)
    alcohol_price = models.DecimalField(
        verbose_name='Price per unit of alcohol', max_digits=8, decimal_places=2, blank=True, null=True, db_index=True
    )

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', db_index=True)

    fullness = models.IntegerField(
        verbose_name='Fullness', validators=[MinValueValidator(1), MaxValueValidator(12)], blank=True, null=True
    )
    freshness = models.IntegerField(
        verbose_name='Freshness', validators=[MinValueValidator(1), MaxValueValidator(12)], blank=True, null=True
    )
    tannins = models.IntegerField(
        verbose_name='Tannins', validators=[MinValueValidator(1), MaxValueValidator(12)], blank=True, null=True
    )
    bitterness = models.IntegerField(
        verbose_name='Bitterness', validators=[MinValueValidator(1), MaxValueValidator(12)], blank=True, null=True
    )
    sweetness = models.IntegerField(
        verbose_name='Sweetness', validators=[MinValueValidator(1), MaxValueValidator(12)], blank=True, null=True
    )

    color = models.TextField(verbose_name='Color description', blank=True, null=True)
    smell = models.TextField(verbose_name='Smell description', blank=True, null=True)
    taste = models.TextField(verbose_name='Taste description', blank=True, null=True)

    country = models.CharField(verbose_name='Country of origin', max_length=255, db_index=True)
    district = models.CharField(verbose_name='District of origin', max_length=255, blank=True, null=True)
    sub_district = models.CharField(verbose_name='Sub district of origin', max_length=255, blank=True, null=True)

    vintage = models.IntegerField(verbose_name='Vintage', blank=True, null=True, db_index=True)

    feedstock = models.TextField(verbose_name='Ingredients', blank=True, null=True)
    production_method = models.TextField(verbose_name='Production method', blank=True, null=True)

    alcohol = models.DecimalField(verbose_name='Alcohol percentage', max_digits=4, decimal_places=2, db_index=True)
    sugar = models.DecimalField(
        verbose_name='Grams of sugar per litre', max_digits=5, decimal_places=2, blank=True, null=True
    )
    acid = models.DecimalField(
        verbose_name='Grams of acid per litre', max_digits=5, decimal_places=2, blank=True, null=True
    )

    storage = models.TextField(verbose_name='How to store product', blank=True, null=True)

    producer = models.CharField(verbose_name='Producer', max_length=255, blank=True, null=True, db_index=True)
    wholesaler = models.CharField(verbose_name='Wholesaler', max_length=255, blank=True, null=True)
    distributor = models.CharField(verbose_name='Distributor', max_length=255, blank=True, null=True)

    packaging = models.CharField(verbose_name='Packaging type', max_length=255)
    cork = models.CharField(verbose_name='Cork type', max_length=255, blank=True, null=True)

    class Meta:
        ordering = ('name', 'volume', )

    def __str__(self):
        return '%s %f%% (%f)' % (self.name, float(self.alcohol), float(self.volume))

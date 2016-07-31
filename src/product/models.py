from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from finmonopolet.models import BaseModel
from store.models import StoreCategory


class Category(BaseModel):
    pass


class Country(BaseModel):
    pass


class Producer(BaseModel):
    pass


class Suits(BaseModel):
    pass


class Selection(BaseModel):
    pass


class Product(BaseModel):
    product_number = models.IntegerField(verbose_name='Product ID', unique=True, db_index=True)

    url = models.URLField(verbose_name='Product URL')

    last_updated = models.DateTimeField(verbose_name='Last updated', auto_now=True)

    volume = models.DecimalField(verbose_name='Volume', max_digits=5, decimal_places=2, db_index=True)
    price = models.DecimalField(verbose_name='Price', max_digits=8, decimal_places=2, db_index=True)
    litre_price = models.DecimalField(verbose_name='Price per litre', max_digits=8, decimal_places=2, db_index=True)
    alcohol_price = models.DecimalField(
        verbose_name='Price per unit of alcohol', max_digits=8, decimal_places=2, null=True, db_index=True
    )

    category = models.ForeignKey(
        Category, verbose_name='Category', on_delete=models.CASCADE,
        related_name='products', db_index=True,
    )

    fullness = models.IntegerField(
        verbose_name='Fullness', validators=[MinValueValidator(1), MaxValueValidator(12)], null=True
    )
    freshness = models.IntegerField(
        verbose_name='Freshness', validators=[MinValueValidator(1), MaxValueValidator(12)], null=True
    )
    tannins = models.IntegerField(
        verbose_name='Tannins', validators=[MinValueValidator(1), MaxValueValidator(12)], null=True
    )
    bitterness = models.IntegerField(
        verbose_name='Bitterness', validators=[MinValueValidator(1), MaxValueValidator(12)], null=True
    )
    sweetness = models.IntegerField(
        verbose_name='Sweetness', validators=[MinValueValidator(1), MaxValueValidator(12)], null=True
    )

    color = models.TextField(verbose_name='Color description', null=True)
    smell = models.TextField(verbose_name='Smell description', null=True)
    taste = models.TextField(verbose_name='Taste description', null=True)

    country = models.ForeignKey(
        Country, verbose_name='Country of origin', on_delete=models.CASCADE, related_name='products', db_index=True
    )
    district = models.CharField(verbose_name='District of origin', max_length=255, null=True)
    sub_district = models.CharField(verbose_name='Sub district of origin', max_length=255, null=True)

    vintage = models.IntegerField(verbose_name='Vintage', null=True, db_index=True)

    feedstock = models.TextField(verbose_name='Ingredients', null=True)
    production_method = models.TextField(verbose_name='Production method', null=True)

    selection = models.ForeignKey(
        Selection, verbose_name='Selection', on_delete=models.CASCADE, related_name='products', db_index=True
    )

    alcohol = models.DecimalField(verbose_name='Alcohol percentage', max_digits=4, decimal_places=2, db_index=True)
    sugar = models.DecimalField(
        verbose_name='Grams of sugar per litre', max_digits=5, decimal_places=2, null=True
    )
    acid = models.DecimalField(
        verbose_name='Grams of acid per litre', max_digits=5, decimal_places=2, null=True
    )

    storage = models.TextField(verbose_name='How to store product', null=True)

    producer = models.ForeignKey(
        Producer, verbose_name='Producer', on_delete=models.CASCADE, related_name='products',
        null=True, db_index=True
    )
    wholesaler = models.CharField(verbose_name='Wholesaler', max_length=255, null=True)
    distributor = models.CharField(verbose_name='Distributor', max_length=255, null=True)

    packaging = models.CharField(verbose_name='Packaging type', max_length=255)
    cork = models.CharField(verbose_name='Cork type', max_length=255, null=True)

    suits = models.ManyToManyField(
        Suits, verbose_name='Suits', related_name='products', db_index=True,
    )
    store_category = models.ForeignKey(
        StoreCategory, verbose_name='Store category', on_delete=models.CASCADE, related_name='products',
        null=True, db_index=True
    )

    active = models.BooleanField(verbose_name='Tilgjengelig', default=True)

    class Meta:
        ordering = ('canonical_name', 'volume', )

    def __str__(self):
        return '%s %.2f%% (%.2fl)' % (self.name, float(self.alcohol), float(self.volume))

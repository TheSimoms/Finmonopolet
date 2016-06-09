# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-06 14:26
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255, verbose_name='Name')),
                ('canonical_name', models.CharField(db_index=True, max_length=255, verbose_name='Canonical name')),
                ('slug', models.SlugField(allow_unicode=True, max_length=255, verbose_name='Slug')),
            ],
            options={
                'ordering': ('canonical_name',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255, verbose_name='Name')),
                ('canonical_name', models.CharField(db_index=True, max_length=255, verbose_name='Canonical name')),
                ('slug', models.SlugField(allow_unicode=True, max_length=255, verbose_name='Slug')),
            ],
            options={
                'ordering': ('canonical_name',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Producer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255, verbose_name='Name')),
                ('canonical_name', models.CharField(db_index=True, max_length=255, verbose_name='Canonical name')),
                ('slug', models.SlugField(allow_unicode=True, max_length=255, verbose_name='Slug')),
            ],
            options={
                'ordering': ('canonical_name',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255, verbose_name='Name')),
                ('canonical_name', models.CharField(db_index=True, max_length=255, verbose_name='Canonical name')),
                ('slug', models.SlugField(allow_unicode=True, max_length=255, verbose_name='Slug')),
                ('product_number', models.IntegerField(db_index=True, unique=True, verbose_name='Product ID')),
                ('url', models.URLField(verbose_name='Product URL')),
                ('last_updated', models.DateTimeField(auto_now=True, verbose_name='Last updated')),
                ('volume', models.DecimalField(db_index=True, decimal_places=2, max_digits=5, verbose_name='Volume')),
                ('price', models.DecimalField(db_index=True, decimal_places=2, max_digits=8, verbose_name='Price')),
                ('litre_price', models.DecimalField(db_index=True, decimal_places=2, max_digits=8, verbose_name='Price per litre')),
                ('alcohol_price', models.DecimalField(blank=True, db_index=True, decimal_places=2, max_digits=8, null=True, verbose_name='Price per unit of alcohol')),
                ('fullness', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)], verbose_name='Fullness')),
                ('freshness', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)], verbose_name='Freshness')),
                ('tannins', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)], verbose_name='Tannins')),
                ('bitterness', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)], verbose_name='Bitterness')),
                ('sweetness', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)], verbose_name='Sweetness')),
                ('color', models.TextField(blank=True, null=True, verbose_name='Color description')),
                ('smell', models.TextField(blank=True, null=True, verbose_name='Smell description')),
                ('taste', models.TextField(blank=True, null=True, verbose_name='Taste description')),
                ('district', models.CharField(blank=True, max_length=255, null=True, verbose_name='District of origin')),
                ('sub_district', models.CharField(blank=True, max_length=255, null=True, verbose_name='Sub district of origin')),
                ('vintage', models.IntegerField(blank=True, db_index=True, null=True, verbose_name='Vintage')),
                ('feedstock', models.TextField(blank=True, null=True, verbose_name='Ingredients')),
                ('production_method', models.TextField(blank=True, null=True, verbose_name='Production method')),
                ('alcohol', models.DecimalField(db_index=True, decimal_places=2, max_digits=4, verbose_name='Alcohol percentage')),
                ('sugar', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Grams of sugar per litre')),
                ('acid', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Grams of acid per litre')),
                ('storage', models.TextField(blank=True, null=True, verbose_name='How to store product')),
                ('wholesaler', models.CharField(blank=True, max_length=255, null=True, verbose_name='Wholesaler')),
                ('distributor', models.CharField(blank=True, max_length=255, null=True, verbose_name='Distributor')),
                ('packaging', models.CharField(max_length=255, verbose_name='Packaging type')),
                ('cork', models.CharField(blank=True, max_length=255, null=True, verbose_name='Cork type')),
                ('active', models.BooleanField(default=True, verbose_name='Tilgjengelig')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='product.Category')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='product.Country', verbose_name='Country of origin')),
                ('producer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='product.Producer', verbose_name='Producer')),
                ('store_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='store.StoreCategory', verbose_name='Store category')),
            ],
            options={
                'ordering': ('canonical_name', 'volume'),
            },
        ),
        migrations.CreateModel(
            name='Suits',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255, verbose_name='Name')),
                ('canonical_name', models.CharField(db_index=True, max_length=255, verbose_name='Canonical name')),
                ('slug', models.SlugField(allow_unicode=True, max_length=255, verbose_name='Slug')),
            ],
            options={
                'ordering': ('canonical_name',),
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='product',
            name='suits',
            field=models.ManyToManyField(blank=True, db_index=True, related_name='products', to='product.Suits', verbose_name='Suits'),
        ),
    ]
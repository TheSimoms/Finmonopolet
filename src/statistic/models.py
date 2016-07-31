import jsonfield

from django.db import models

from product.models import Category, Country


class Statistics(models.Model):
    timestamp = models.DateTimeField(verbose_name='Timestamp', auto_now_add=True, db_index=True)

    category = models.ForeignKey(Category, verbose_name='Category', db_index=True, null=True)
    country = models.ForeignKey(Country, verbose_name='Country', db_index=True, null=True)

    count = jsonfield.JSONField()

    volume = jsonfield.JSONField()
    price = jsonfield.JSONField()
    litre_price = jsonfield.JSONField()
    alcohol_price = jsonfield.JSONField()
    vintage = jsonfield.JSONField()


    class Meta:
        ordering = ('timestamp', 'country', )

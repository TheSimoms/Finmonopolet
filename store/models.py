import jsonfield

from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator

from finmonopolet.models import BaseModel


class StoreCategory(BaseModel):
    category_number = models.IntegerField(
        verbose_name='Category number', validators=[MinValueValidator(0), MaxValueValidator(7)], unique=True,
        db_index=True
    )

    class Meta:
        # FIXME: Use BaseModel fields + override
        ordering = ('category_number', 'canonical_name', )


class Store(BaseModel):
    last_updated = models.DateTimeField(verbose_name='Last updated', auto_now=True)

    address = models.CharField(verbose_name='Store address', max_length=255, db_index=True)
    zip_code = models.CharField(
        verbose_name='Zip code', max_length=4, validators=[MinLengthValidator(4), MaxLengthValidator(4)], db_index=True
    )
    postal = models.CharField(verbose_name='Postal', max_length=255, db_index=True)

    category = models.ForeignKey(StoreCategory, on_delete=models.CASCADE, related_name='stores', db_index=True)

    latitude = models.DecimalField(verbose_name='GPS latitude', max_digits=9, decimal_places=7, db_index=True)
    longitude = models.DecimalField(verbose_name='GPS longitude', max_digits=10, decimal_places=7, db_index=True)

    opening_times = jsonfield.JSONField()
    opening_times_next = jsonfield.JSONField()
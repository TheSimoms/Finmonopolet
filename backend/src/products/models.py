from django.db import models


class BaseModel(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    sort_name = models.CharField(max_length=255, db_index=True)

    class Meta:
        abstract = True
        ordering = ['sort_name']

    def __str__(self):
        return '%s' % self.name

    def save(self, *args, **kwargs):
        self.sort_name = self.name.strip().lower()

        super().save(*args, **kwargs)


class ProductType(BaseModel):
    pass


class Country(BaseModel):
    pass


class Producer(BaseModel):
    pass


class Product(BaseModel):
    product_number = models.CharField(max_length=255, unique=True, db_index=True)

    alcohol_content = models.DecimalField(max_digits=4, decimal_places=2, db_index=True)
    volume = models.DecimalField(max_digits=5, decimal_places=2, db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    litre_price = models.DecimalField(max_digits=12, decimal_places=2, db_index=True)
    alcohol_price = models.DecimalField(max_digits=12, decimal_places=2, db_index=True)
    vintage = models.IntegerField(null=True, db_index=True)
    stock = models.IntegerField(null=True, db_index=True)

    product_type = models.ForeignKey(
        ProductType, on_delete=models.CASCADE, related_name='products', db_index=True,
    )
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name='products', db_index=True,
    )
    producer = models.ForeignKey(
        Producer, on_delete=models.CASCADE, related_name='products', null=True,
        db_index=True,
    )

    active = models.BooleanField(default=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} {:.2f}% ({:.2f} l)'.format(
            self.name, self.alcohol_content, self.volume
        )

    class Meta:
        ordering = ['sort_name', 'volume']

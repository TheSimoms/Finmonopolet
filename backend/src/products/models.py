from django.db import models


class Product(models.Model):
    product_number = models.CharField(max_length=255, unique=True, db_index=True)
    name = models.CharField(max_length=255, db_index=True)
    sort_name = models.CharField(max_length=255, db_index=True)

    active = models.BooleanField(default=True)
    last_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.sort_name = self.name.strip().lower()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['sort_name']

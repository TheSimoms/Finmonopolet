from django.db import models


class Category(models.Model):
    name = models.CharField(verbose_name='Category name', unique=True, max_length=255, db_index=True)
    canonical_name = models.CharField(
        verbose_name='Canonical category name', max_length=255, db_index=True
    )

    class Meta:
        ordering = ('canonical_name', )

    def __str__(self):
        return '%s' % self.name

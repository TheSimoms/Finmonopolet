from django.db import models


class Category(models.Model):
    name = models.CharField(
        verbose_name='Category name', unique=True, max_length=255, blank=False, null=False, db_index=True
    )

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return '%s' % self.name

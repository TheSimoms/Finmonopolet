from django.db import models
from django.utils.text import slugify


class BaseModel(models.Model):
    name = models.CharField(verbose_name='Name', max_length=255, db_index=True)
    canonical_name = models.CharField(verbose_name='Canonical name', max_length=255, db_index=True)

    slug = models.SlugField(verbose_name='Slug', max_length=255, db_index=True, allow_unicode=True)

    class Meta:
        abstract = True
        ordering = ('canonical_name', )

    def __str__(self):
        return '%s' % self.name

    def save(self, *args, **kwargs):
        self.canonical_name = self.name.lower()
        self.slug = slugify(self.name)

        super(BaseModel, self).save(*args, **kwargs)

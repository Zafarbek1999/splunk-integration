from django.db import models
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('name'))
    price = models.IntegerField(verbose_name=_('price'))
    count = models.IntegerField(verbose_name=_('count'))
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')

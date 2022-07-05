from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    splunk_key = models.CharField(max_length=255, default=None, null=True, blank=True)

    class Meta:
        abstract = True


class Product(BaseModel):
    name = models.CharField(max_length=255, verbose_name=_('name'))
    price = models.IntegerField(verbose_name=_('price'))
    count = models.IntegerField(verbose_name=_('count'))
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')

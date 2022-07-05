from itertools import chain
from datetime import datetime

from django.db.transaction import atomic

from core.models import Product
from core.splunk.service import SplunkClient


@atomic
def upload_all():
    splunk_client = SplunkClient()
    for item in Product.objects.all():
        data = {}
        opts = item._meta
        for f in chain(opts.concrete_fields, opts.private_fields):
            if f.name != 'splunk_key':
                if isinstance(f.value_from_object(item), datetime):
                    data[f.name] = str(f.value_from_object(item))
                else:
                    data[f.name] = f.value_from_object(item)
        for f in opts.many_to_many:
            data[f.name] = [i.id for i in f.value_from_object(item)]
        if item.splunk_key is None:
            item.splunk_key = splunk_client.insert(collection_name=item.__class__.__name__, item_data=data)
            item.save()
        else:
            splunk_client.update(collection_name=item.__class__.__name__, splunk_key=item.splunk_key, item_data=data)

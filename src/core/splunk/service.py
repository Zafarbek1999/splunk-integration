import json

from django.conf import settings
import splunklib.client as client
from rest_framework.exceptions import ValidationError


class SplunkClient:
    def __init__(self):
        self.service = client.connect(
            host=settings.SPLUNK_HOST,
            port=settings.SPLUNK_PORT,
            username=settings.SPLUNK_USERNAME,
            password=settings.SPLUNK_PASSWORD,
        )

    def search(self, collection_name, **query):
        if collection_name not in self.service.kvstore:
            ValidationError({'splunk': 'Collection not found'})
        collection = self.service.kvstore[collection_name]
        return collection.data.query(query=query)

    def insert(self, collection_name, item_data):
        if collection_name not in self.service.kvstore:
            self.service.kvstore.create(name=collection_name)
        collection = self.service.kvstore[collection_name]
        response = collection.data.insert(item_data)
        return response.get('_key')

    def update(self, collection_name, splunk_key, item_data):
        if collection_name not in self.service.kvstore:
            ValidationError({'splunk': 'Collection not found'})
        collection = self.service.kvstore[collection_name]
        response = collection.data.update(splunk_key, item_data)
        return response.get('_key')

    def delete(self, collection_name, query=None):
        if collection_name not in self.service.kvstore:
            ValidationError({'splunk': 'Collection not found'})
        collection = self.service.kvstore[collection_name]
        if isinstance(query, dict):
            query = json.dumps(query)
        collection.data.delete(query=query)

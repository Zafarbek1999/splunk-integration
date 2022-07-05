import secrets

from django.core.management.base import BaseCommand
from django.db.transaction import atomic
from django.utils.crypto import get_random_string

from core.models import Product


class Command(BaseCommand):
    help = 'Generate products'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of products to be created')

    @atomic
    def handle(self, *args, **kwargs):
        total = kwargs.get('total')
        created = 0
        while created < total:
            step = min(total - created, 1000)
            Product.objects.bulk_create(
                [
                    Product(
                        name=get_random_string(length=10),
                        price=secrets.choice(range(1, 1000)),
                        count=secrets.choice(range(1, 1000)),
                        description=get_random_string(length=100)
                    ) for _ in range(step)
                ]
            )
            created += step
        self.stdout.write(self.style.SUCCESS(f'Successfully created {total} products'))

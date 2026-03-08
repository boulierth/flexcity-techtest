from django.core.management.base import BaseCommand
from faker import Faker
from flexcity_techtest.activation.models import Asset, Availability
import random
from datetime import date, timedelta

class Command(BaseCommand):
    help = "Generate random assets using Faker"

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=10, help='Number of assets to create')

    def handle(self, *args, **options):
        fake = Faker()
        count = options['count']
        created = 0

        for _ in range(count):
            volume = random.randint(1, 100)
            activation_cost = round(random.uniform(1, 20) * volume, 3)
            asset = Asset(
                code=fake.unique.bothify(text='???-#####'),
                name=fake.company(),
                volume=volume,
                activation_cost=activation_cost,
            )
            asset.save()
            # Create 1-5 availabilities in the next week
            num_avail = random.randint(1, 5)
            days = random.sample(range(7), num_avail)
            for d in days:
                avail_date = date.today() + timedelta(days=d)
                Availability.objects.create(asset=asset, date=avail_date)

            created += 1
        self.stdout.write(self.style.SUCCESS(f"Created {created} assets with availabilities."))


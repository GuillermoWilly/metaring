import csv
from django.core.management.base import BaseCommand
from myapp.models import Airports


class Command(BaseCommand):
    help = 'Import airports from CSV'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        with open(csv_file, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            airports = []

            for row in reader:
                airport = Airports(
                    icao=row.get('icao', ''),
                    iata=row.get('iata', ''),
                    name=row.get('name', ''),
                    city=row.get('city', ''),
                    subd=row.get('subd', ''),
                    country=row.get('country', ''),
                    elevation=row.get('elevation', ''),
                    lat=row.get('lat', ''),
                    lon=row.get('lon', ''),
                    tz=row.get('tz', ''),
                    lid=row.get('lid', ''),
                )
                airports.append(airport)

            Airports.objects.bulk_create(airports)

        self.stdout.write(self.style.SUCCESS('Import completed'))
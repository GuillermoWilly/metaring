from django.core.management.base import BaseCommand
from django.db.models import Count
from myapp.models import Airports


class Command(BaseCommand):
    help = "Clean duplicate airports based on ICAO"

    def handle(self, *args, **kwargs):
        duplicates = (
            Airports.objects
            .values('icao')
            .annotate(count=Count('id'))
            .filter(count__gt=1)
        )

        total_deleted = 0
        total_groups = 0

        if not duplicates:
            self.stdout.write(self.style.SUCCESS("No duplicates found."))
            return

        for dup in duplicates:
            icao = dup['icao']
            total_groups += 1

            airports = Airports.objects.filter(icao=icao).order_by('id')

            keep = airports.first()
            duplicates_qs = airports.exclude(id=keep.id)

            self.stdout.write(f"\nProcessing ICAO: {icao}")
            self.stdout.write(f"Keeping ID: {keep.id}")

            for airport in duplicates_qs:
                
                if hasattr(airport, "favorited_by"):
                    users = airport.favorited_by.all()
                    for user in users:
                        keep.favorited_by.add(user)

                self.stdout.write(f"Deleting duplicate ID: {airport.id}")
                airport.delete()
                total_deleted += 1

        self.stdout.write("\n" + "="*40)
        self.stdout.write(self.style.SUCCESS(
            f"Done. Cleaned {total_groups} ICAO groups, deleted {total_deleted} duplicates."
        ))
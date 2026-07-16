"""
----------------------------------------------------
Smart Angkor Tourist Guide
Load Data Command
----------------------------------------------------
Run with:  python manage.py load_data
Reads guide/data/temples.csv and guide/data/roads.csv
and loads them into the SQLite database.
----------------------------------------------------
"""

import csv
import os

from django.core.management.base import BaseCommand
from django.conf import settings

from guide.models import Temple, Road


class Command(BaseCommand):
    help = "Load temples.csv and roads.csv into the database"

    def handle(self, *args, **options):

        data_dir = os.path.join(settings.BASE_DIR, "guide", "data")

        # ---- Load Temples ----
        temples_path = os.path.join(data_dir, "temples.csv")
        created_temples = 0

        with open(temples_path, "r", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)

            for row in reader:
                temple, created = Temple.objects.update_or_create(
                    temple_id=row["ID"],
                    defaults={
                        "name": row["Name"],
                        "category": row["Category"],
                        "rating": float(row["Rating"]),
                        "open_time": row["Open"],
                        "close_time": row["Close"],
                        "visit_time": float(row["VisitTime"]),
                        "description": row["Description"],
                    },
                )
                if created:
                    created_temples += 1

        # ---- Load Roads ----
        roads_path = os.path.join(data_dir, "roads.csv")
        created_roads = 0
        skipped = []

        with open(roads_path, "r", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)

            for row in reader:
                try:
                    source = Temple.objects.get(name=row["Source"])
                    destination = Temple.objects.get(name=row["Destination"])
                except Temple.DoesNotExist:
                    skipped.append((row["Source"], row["Destination"]))
                    continue

                _, created = Road.objects.update_or_create(
                    source=source,
                    destination=destination,
                    defaults={"distance": float(row["Distance"])},
                )
                if created:
                    created_roads += 1

        self.stdout.write(self.style.SUCCESS(
            f"Loaded {Temple.objects.count()} temples "
            f"({created_temples} new) and {Road.objects.count()} roads "
            f"({created_roads} new)."
        ))

        if skipped:
            self.stdout.write(self.style.WARNING(
                f"Skipped {len(skipped)} road row(s) with unknown temple name: {skipped}"
            ))

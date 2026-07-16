"""
----------------------------------------------------
Smart Angkor Tourist Guide
Models (SQLite storage via Django ORM)
----------------------------------------------------
"""

from django.db import models


class Temple(models.Model):

    temple_id = models.CharField(max_length=10, unique=True, verbose_name="ID")
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=50)
    rating = models.FloatField()
    open_time = models.CharField(max_length=10)
    close_time = models.CharField(max_length=10)
    visit_time = models.FloatField(help_text="Visit time in hours")
    description = models.TextField()

    class Meta:
        ordering = ["temple_id"]

    def __str__(self):
        return self.name

    # Convenience dict matching the original CSV-based dict shape,
    # so the ported HashTable / algorithm code keeps working unchanged.
    def as_dict(self):
        return {
            "ID": self.temple_id,
            "Name": self.name,
            "Category": self.category,
            "Rating": self.rating,
            "Open": self.open_time,
            "Close": self.close_time,
            "VisitTime": self.visit_time,
            "Description": self.description,
        }


class Road(models.Model):

    source = models.ForeignKey(Temple, related_name="roads_from", on_delete=models.CASCADE)
    destination = models.ForeignKey(Temple, related_name="roads_to", on_delete=models.CASCADE)
    distance = models.FloatField(help_text="Distance in km")

    class Meta:
        unique_together = ("source", "destination")

    def __str__(self):
        return f"{self.source.name} -> {self.destination.name} ({self.distance} km)"

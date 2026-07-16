"""
----------------------------------------------------
Smart Angkor Tourist Guide
Utility Functions
----------------------------------------------------
Small helpers ported from the original help_fun.py.
----------------------------------------------------
"""


def estimate_travel_time(distance):

    walk = round(distance / 5 * 60)
    bicycle = round(distance / 15 * 60)
    motorcycle = round(distance / 30 * 60)
    tuktuk = round(distance / 25 * 60)
    car = round(distance / 35 * 60)

    return {
        "walk": walk,
        "bicycle": bicycle,
        "motorcycle": motorcycle,
        "tuktuk": tuktuk,
        "car": car,
    }

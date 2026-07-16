"""
----------------------------------------------------
Smart Angkor Tourist Guide
Decision Tree
----------------------------------------------------
This file recommends temples based on
available time and visitor interest.

Ported from the original console-app decision_tree.py
(names normalised to match temples.csv exactly: "Kravan"
and "Sras Srang").
----------------------------------------------------
"""


def recommend_tour(time, interest):

    recommend = []

    # Short Visit
    if time == "Short time":

        if interest == "History":
            recommend = ["Bayon", "Baphuon"]

        elif interest == "Nature":
            recommend = ["Ta Prohm"]

        elif interest == "Architecture":
            recommend = ["Thommanon", "Chau Say Tevoda"]

        elif interest == "Photography":
            recommend = ["Neak Pean"]

        elif interest == "Sunrise":
            recommend = ["Angkor Wat"]

        elif interest == "Sunset":
            recommend = ["Pre Rup"]

    # Half Day
    elif time == "Half day":

        if interest == "History":
            recommend = ["Angkor Wat", "Bayon", "Baphuon"]

        elif interest == "Nature":
            recommend = ["Ta Prohm", "Neak Pean"]

        elif interest == "Architecture":
            recommend = ["Thommanon", "Chau Say Tevoda", "Preah Khan"]

        elif interest == "Photography":
            recommend = ["Angkor Wat", "Ta Prohm", "Bayon"]

        elif interest == "Sunrise":
            recommend = ["Angkor Wat", "Kravan", "Sras Srang"]

        elif interest == "Sunset":
            recommend = ["Phnom Bakheng", "Pre Rup", "Neak Pean"]

    # Full Day
    elif time == "Full day":

        if interest == "History":
            recommend = ["Angkor Wat", "Bayon", "Baphuon", "Preah Khan"]

        elif interest == "Nature":
            recommend = ["Ta Prohm", "Neak Pean", "Sras Srang", "Terrace of the Elephants"]

        elif interest == "Architecture":
            recommend = ["Angkor Wat", "Baphuon", "Bayon", "Thommanon", "Chau Say Tevoda", "Preah Khan"]

        elif interest == "Photography":
            recommend = ["Angkor Wat", "Ta Prohm", "Phnom Bakheng", "Pre Rup", "Preah Khan"]

        elif interest == "Sunrise":
            recommend = ["Angkor Wat", "Kravan", "Sras Srang"]

        elif interest == "Sunset":
            recommend = ["Phnom Bakheng", "Pre Rup", "Neak Pean"]

    return recommend

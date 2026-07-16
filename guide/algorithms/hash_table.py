"""
----------------------------------------------------
Smart Angkor Tourist Guide
Hash Table
----------------------------------------------------
This file stores temple information in a Hash Table
for fast searching.

Ported from the original console-app hash_table.py.
The Django views build one of these from the Temple
model each time they need fast ID/name lookup.
----------------------------------------------------
"""


class HashTable:

    def __init__(self):

        self.size = 20
        self.table = []

        for i in range(self.size):
            self.table.append([])

    # Hash Function
    def hash_function(self, key):

        total = 0

        for letter in key:
            total = total + ord(letter)

        index = total % self.size
        return index

    # Insert Temple
    def insert(self, temple):

        key = temple["ID"]
        index = self.hash_function(key)
        self.table[index].append(temple)

    # Search Temple by ID
    def search_by_id(self, temple_id):

        index = self.hash_function(temple_id)
        bucket = self.table[index]

        for temple in bucket:
            if temple["ID"] == temple_id:
                return temple

        return None

    # Search Temple by Name
    def search_by_name(self, temple_name):

        for bucket in self.table:
            for temple in bucket:
                if temple["Name"].lower() == temple_name.lower():
                    return temple

        return None

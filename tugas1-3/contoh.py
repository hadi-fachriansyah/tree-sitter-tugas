import os
from pathlib import Path


def tambah(a, b):
    """Menjumlahkan dua angka."""
    return a + b


def kali(a, b, c):
    print(a, b)
    return a * b * c


def sapa():
    print("halo")
    return None


class Hewan:
    def bunyi(self):
        return "..."

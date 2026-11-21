"""Tugas 2 - Penjelajah node (versi rekursif + versi TreeCursor).
Pakai: python jelajah.py file.py
"""
import sys
import tree_sitter_python as tspython
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))


def jelajah(node, kedalaman=0, field=None):
    baris, kolom = node.start_point
    label = f"{field}: " if field else ""
    print("  " * kedalaman + f"{label}{node.type} [{baris + 1}:{kolom}]")
    # i = indeks di node.children (SEMUA child), supaya field_name_for_child benar
    for i, child in enumerate(node.children):
        if not child.is_named:
            continue
        jelajah(child, kedalaman + 1, node.field_name_for_child(i))


def jelajah_cursor(tree):
    """[Pengayaan] Versi TreeCursor: output harus identik dengan jelajah()."""
    cursor = tree.walk()
    kedalaman = 0
    while True:
        node = cursor.node
        if node.is_named:
            baris, kolom = node.start_point
            f = cursor.field_name
            label = f"{f}: " if f else ""
            print("  " * kedalaman + f"{label}{node.type} [{baris + 1}:{kolom}]")
            # hanya turun lewat node bernama; anonim tidak punya anak bernama yang perlu dicetak
        if node.is_named and cursor.goto_first_child():
            kedalaman += 1
            continue
        if cursor.goto_next_sibling():
            continue
        # naik sampai ada saudara berikutnya
        while True:
            if not cursor.goto_parent():
                return
            kedalaman -= 1
            if cursor.goto_next_sibling():
                break


if __name__ == "__main__":
    with open(sys.argv[1], "rb") as f:
        tree = parser.parse(f.read())
    if len(sys.argv) > 2 and sys.argv[2] == "--cursor":
        jelajah_cursor(tree)
    else:
        jelajah(tree.root_node)

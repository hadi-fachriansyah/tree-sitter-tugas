"""Tugas 1 - Membaca pohon.
Parse 3 potongan kode Python, cetak pohonnya, tampilkan node anonim,
lalu rusak kodenya dengan sengaja untuk melihat ERROR / MISSING.
"""
import tree_sitter_python as tspython
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))

POTONGAN = {
    "fungsi": b"def sapa(nama): return nama\n",
    "if/else": b"if x > 1:\n    y = 2\nelse:\n    y = 3\n",
    "kelas": b"class Kucing:\n    def bunyi(self):\n        return 'meong'\n",
}


def cetak_anak(judul, node):
    print(f"  {judul}:")
    for c in node.children:
        print("   ", c.type, "-> bernama" if c.is_named else "-> anonim")


for nama, kode in POTONGAN.items():
    tree = parser.parse(kode)
    print(f"=== {nama} ===")
    print(tree.root_node)
    pertama = tree.root_node.children[0]
    cetak_anak("children (semua, termasuk anonim)", pertama)
    print("  named_children:", [c.type for c in pertama.named_children])
    print()

# Node anonim di dalam parameters: ( dan )
tree = parser.parse(POTONGAN["fungsi"])
params = tree.root_node.children[0].child_by_field_name("parameters")
cetak_anak("anak dari node parameters", params)
print()

# Rusak sengaja: hapus ':' setelah def sapa(nama)
rusak = b"def sapa(nama) return nama\n"
tree = parser.parse(rusak)
print("=== kode rusak (':' dihapus) ===")
print(tree.root_node)
print("has_error:", tree.root_node.has_error)

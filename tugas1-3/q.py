"""Tugas 3 - Penjalan query.
Pakai: python q.py file.py query.scm
Untuk pasangan (nama fungsi, jumlah parameter) pakai: python q.py file.py fungsi.scm --matches
"""
import sys
import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor

PY = Language(tspython.language())
parser = Parser(PY)

kode = open(sys.argv[1], "rb").read()
pola = open(sys.argv[2]).read()
tree = parser.parse(kode)
query = Query(PY, pola)

if "--matches" in sys.argv:
    for _, cap in QueryCursor(query).matches(tree.root_node):
        nama = cap["nama"][0].text.decode()
        jumlah = cap["params"][0].named_child_count
        print(f"{nama}: {jumlah} parameter")
else:
    hasil = QueryCursor(query).captures(tree.root_node)
    for nama, nodes in hasil.items():
        for n in nodes:
            print(f"@{nama}  baris {n.start_point[0] + 1}: {n.text.decode()}")

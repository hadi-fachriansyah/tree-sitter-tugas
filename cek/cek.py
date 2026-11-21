"""cek.py - pemeriksa kode Python berbasis tree-sitter.

Melaporkan:
  1. komentar TODO / FIXME
  2. fungsi dengan body lebih dari 30 baris
  3. file yang pohonnya mengandung error sintaks

Pakai: python cek.py <folder>
"""
import sys
from pathlib import Path

import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor

PY = Language(tspython.language())
parser = Parser(PY)

BATAS_BARIS = 30
SKIP = {"venv", ".venv", ".git", "node_modules", "__pycache__"}

Q_TODO = Query(PY, '((comment) @c (#match? @c "TODO|FIXME"))')
Q_FUNGSI = Query(PY, "(function_definition name: (identifier) @nama) @fungsi")


def error_pertama(node):
    """Cari node ERROR / MISSING pertama (urutan dokumen) secara rekursif."""
    if node.is_error or node.is_missing:
        return node
    for child in node.children:
        if child.has_error or child.is_error or child.is_missing:
            hasil = error_pertama(child)
            if hasil:
                return hasil
    return None


def cek_file(path):
    tree = parser.parse(path.read_bytes())
    root = tree.root_node

    # Fitur 1: komentar TODO/FIXME
    for node in QueryCursor(Q_TODO).captures(root).get("c", []):
        teks = node.text.decode(errors="replace").strip()
        print(f"{path}:{node.start_point[0] + 1}: TODO/FIXME: {teks}")

    # Fitur 2: fungsi lebih dari 30 baris (semua fungsi dihitung, termasuk method & bersarang)
    for _, cap in QueryCursor(Q_FUNGSI).matches(root):
        fungsi = cap["fungsi"][0]
        nama = cap["nama"][0].text.decode(errors="replace")
        jumlah = fungsi.end_point[0] - fungsi.start_point[0] + 1
        if jumlah > BATAS_BARIS:
            print(f"{path}:{fungsi.start_point[0] + 1}: fungsi '{nama}' terlalu panjang ({jumlah} baris)")

    # Fitur 3: error sintaks
    if root.has_error:
        err = error_pertama(root)
        if err:
            jenis = "MISSING" if err.is_missing else "ERROR"
            print(f"{path}:{err.start_point[0] + 1}: error sintaks ({jenis}) di kolom {err.start_point[1]}")
        else:
            print(f"{path}: error sintaks")


def main():
    if len(sys.argv) != 2:
        print("Pakai: python cek.py <folder>")
        sys.exit(1)
    for path in sorted(Path(sys.argv[1]).rglob("*.py")):
        if SKIP & set(path.parts):
            continue
        cek_file(path)


if __name__ == "__main__":
    main()

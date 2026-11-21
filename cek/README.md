# cek.py - pemeriksa kode Python dengan tree-sitter

Skrip kecil yang membaca semua file `.py` di sebuah folder dan melaporkan:

1. Komentar yang mengandung `TODO` atau `FIXME` (query tree-sitter + `#match?`)
2. Fungsi yang panjangnya lebih dari 30 baris (dari `start_point` dan `end_point`)
3. File dengan error sintaks (`root_node.has_error`) beserta baris pertama yang bermasalah

## Instalasi

Butuh Python 3.10+.

```
python -m pip install tree-sitter tree-sitter-python
```

## Menjalankan

```
python cek.py <folder>
```

Folder `venv/`, `.venv/`, `.git/`, `node_modules/`, dan `__pycache__/` dilewati.

## Contoh output

```
uji/panjang.py:1: fungsi 'panjang' terlalu panjang (37 baris)
uji/rusak.py:1: error sintaks (ERROR) di kolom 0
uji/todo.py:1: TODO/FIXME: # TODO: tambahkan validasi
uji/todo.py:3: TODO/FIXME: # FIXME: belum menangani x negatif
```

## Catatan

- Semua fungsi dihitung: method di dalam kelas dan fungsi bersarang ikut diperiksa.
- Panjang fungsi dihitung dari baris `def` sampai baris terakhir body (termasuk baris kosong dan komentar di dalamnya).
- Folder `uji/` berisi tiga file uji buatan sendiri.

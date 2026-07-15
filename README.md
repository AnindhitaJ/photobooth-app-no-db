# LUX Photobooth — Local Edition

Versi ini mempertahankan visual dan alur kamera utama dari project awal, tetapi seluruh backend telah dilepas.

## Produk aktif

- Photostrip 5×15.
- Photobox 4R.
- Ganci.
- Gabung dua photostrip dari galeri HP menjadi satu lembar 4R siap download.

## Arsitektur

- HTML, CSS, dan JavaScript statis tanpa build framework.
- Tidak memakai login, Supabase, API server, database server, storage cloud, analytics, CMS, event mode, atau galeri online.
- Foto diproses di browser. `localStorage` dan `IndexedDB` hanya dipakai sebagai penyimpanan sementara pada perangkat agar perpindahan halaman kamera → filter → hasil tetap berjalan dan gambar besar tidak mudah melebihi batas browser.
- Hasil tidak disinkronkan ke perangkat lain dan tidak diunggah otomatis.

## Template bawaan

- Photostrip: 146 template bawaan, terdiri dari 26 warna Basic dan 120 tema dekoratif. Seluruh template memiliki identitas LUX Photobooth berupa wordmark, camera mark, monogram, atau tagline yang disesuaikan dengan gaya kategorinya. Pada kategori Social Media, seluruh identitas akun, channel, album, player, dan header chat memakai luxphotobootd.id agar konsisten dan tidak bertabrakan dengan likes, replies, atau action bar.
- Photobox 4R: 30 template bawaan dengan layout 1–8 slot. Pemilih template memakai kategori yang sama seperti photostrip: Basic, Korean, Film, Elegant, Floral, Seasonal, Gaming, Pattern, dan Social Media. Template 1-slot memakai area foto yang lebih dominan, tanpa tulisan ukuran cetak, jumlah frame, atau badge nomor di dalam desain.
- Ganci: frame bawaan tetap tersedia pada halaman Ganci. Generator layout cetak mengekspor JPG langsung dari Canvas lokal dan tidak bergantung pada modul login atau helper backend.

## Gabung 2 Photostrip

Halaman `merge-strips.html` menerima dua gambar dari galeri perangkat, menyusunnya berdampingan pada kanvas 4R portrait 1181 × 1772 px, lalu menghasilkan file JPG. Pengguna dapat memutar gambar, menukar posisi, memilih mode fit, pemisah tengah, latar, dan kualitas JPG. Semua proses berlangsung lokal.

Jumlah template dan struktur paket divalidasi oleh `scripts/validate_repo.py`.

## Menjalankan lokal

```bash
npm run serve
```

Lalu buka `http://localhost:4173`.

Kamera browser membutuhkan secure context. Untuk deployment produksi gunakan HTTPS; Vercel menyediakan HTTPS otomatis.

## Deployment Vercel

Import folder ini sebagai project Vercel dengan Framework Preset **Other**. Tidak ada build command dan tidak ada environment variable yang diperlukan.

## Batas versi tanpa backend

QR lintas perangkat, galeri cloud, akun, template upload permanen, event mode, analytics, dan sinkronisasi tidak tersedia karena fitur tersebut membutuhkan server atau storage bersama. Download, share, print, GIF, live photo, filter, layout ganci, dan penggabungan strip tetap berjalan secara lokal bila browser mendukung API terkait.

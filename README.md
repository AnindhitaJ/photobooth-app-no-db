# LUX Photobooth — Local Edition

Versi ini mempertahankan visual dan alur kamera utama dari project awal, tetapi seluruh backend telah dilepas.

## Produk aktif

- Photostrip 5×15
- Photobox 4R / 10×15
- Ganci photo insert

## Arsitektur

- HTML, CSS, dan JavaScript statis tanpa build framework.
- Tidak memakai login, Supabase, API server, database server, storage cloud, analytics, CMS, event mode, atau galeri online.
- Foto diproses di browser. `localStorage` dan `IndexedDB` hanya dipakai sebagai penyimpanan sementara pada perangkat agar perpindahan halaman kamera → filter → hasil tetap berjalan dan gambar besar tidak mudah melebihi batas browser.
- Hasil tidak disinkronkan ke perangkat lain dan tidak diunggah otomatis.

## Template bawaan

- Photostrip: 136 template bawaan (16 basic colors + 120 tema dekoratif).
- Photobox 4R: 18 template bawaan.
- Ganci: frame bawaan tetap tersedia pada halaman Ganci.

Jumlah di atas divalidasi oleh `scripts/validate_repo.py`.

## Menjalankan lokal

```bash
npm run serve
```

Lalu buka `http://localhost:4173`.

Kamera browser membutuhkan secure context. Untuk deployment produksi gunakan HTTPS; Vercel sudah menyediakan HTTPS otomatis.

## Deployment Vercel

Import folder ini sebagai project Vercel dengan Framework Preset **Other**. Tidak ada build command dan tidak ada environment variable yang diperlukan.

## Batas versi tanpa backend

QR lintas perangkat, galeri cloud, akun, template upload permanen, event mode, analytics, dan sinkronisasi tidak tersedia karena fitur tersebut membutuhkan server atau storage bersama. Download, share, print, GIF, live photo, filter, dan layout ganci tetap berjalan secara lokal bila browser mendukung API terkait.

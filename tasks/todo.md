# Rencana Kerja: Pembaruan Komprehensif Website Prodi SI

- **Workspace**: `~/projects/website-prodi-si`
- **SOP Live Preview**: Berjalan aktif di sesi tmux `dev-prodi` (`http://localhost:4321/`)
- **Kebijakan Git**: Commit lokal bertahap, **DILARANG KERAS `git push` otomatis** (Dipatuhi 100%).

---

### Fase 13: Standardisasi Simetri Foto Civitas, Format Foto Asdos, Web Profile Dr. Dwi & Dropdown Civitas
- [x] 13.1 Tambahkan Web Profile Dr. Dwi Wahyu Prabowo (`https://bowo.staff.unda.ac.id/`) pada data `civitas.json` dan tampilkan di halaman detail dosen (`/civitas/dosen/[slug]/` dan `/en/faculty/[slug]/`) pada header dan kartu tautan riset resmi.
- [x] 13.2 Ubah label menu dropdown Civitas di `navigation.json` dari "Direktori Dosen Tetap" menjadi "Direktori Dosen".
- [x] 13.3 Standardisasi Simetri & Proporsi Wajah Foto Dosen:
  - Eksekusi crop 1:1 persegi terpusat (*face-centered 800x800 Lanczos*) untuk seluruh foto dosen (`bowo.jpg`, `eka.jpg`, `nurahman.jpg`, `aziz.jpg`, `elika.jpg`, `lukman.jpg`, `serika.jpg`, `agung.jpg`, `deny.jpg`, `dwika.jpg`, `selviana.jpg`) guna mengeliminasi ketimpangan headroom dan pergeseran sumbu wajah.
  - Perbarui CSS `object-position: center` pada antarmuka civitas.
- [x] 13.4 Penyelarasan Format Foto Asisten Dosen (Asdos):
  - Terapkan format kartu foto yang identik dengan dosen (`w-24 h-24 sm:w-28 sm:h-28 rounded-2xl border-2 border-gold-500/80 shadow-md overflow-hidden bg-navy-950 flex items-center justify-center shrink-0`) di seksi Asdos (`civitas/index.astro` dan `en/faculty/index.astro`).
  - Eksekusi crop 1:1 persegi terpusat untuk foto asdos (`dody.jpg`, `fauzan.jpg`).
  - Perbesar avatar pada halaman detail asdos (`/civitas/asdos/[slug]/`).
- [x] 13.5 Kompilasi SSG (`npm run build` lulus 100%, 0 error), verifikasi via browser CDP, dan commit git lokal: `[main 9cdd352]`.

---

### Fase 14: Simetri Foto Lanjutan, Integrasi PkM, Struktur Organisasi & Rebranding "Sistem Informasi"
- [x] 14.1 Penyesuaian Foto Dr. Dwi (Geser ke Kanan) & Foto Pak Aziz (Naikkan Sumbu Wajah):
  - `bowo.jpg`: geser crop window ke x1=195, x2=735 agar subjek bergeser ke kanan simetris di tengah bingkai.
  - `aziz.jpg`: potong headroom berlebih (mulai y=170) dan pusatkan sumbu kepala di x=390 agar wajah naik proporsional.
- [x] 14.2 Integrasi Foto Asdos Prio Jaka Arsyad (`prio.jpg`):
  - Ambil dari `/Works - UNDA/Web-Sisfo-UNDA/public/prio.jpg`, crop 1:1 persegi (800x800 Lanczos), simpan ke `public/images/dosen/prio.jpg`.
  - Hubungkan ke `src/data/civitas.json` pada properti `image` Prio.
- [x] 14.3 Pembaruan Struktur Organisasi Prodi (`profil/index.astro` & `en/about/index.astro`):
  - Dekan & Ketua Program Studi: Dr. Dwi Wahyu Prabowo, S.Si., M.Eng.
  - Sekretaris Program Studi: Eka Prasetyaningrum, S.Kom., M.M.
  - Pengelola MBKM: Elika Thea Kirana, S.T., M.Kom.
  - Gugus Kendali Mutu: Nurahman, S.Kom., M.M., M.Kom.
  - Koordinator Kemahasiswaan & Alumni: Abdul Aziz, S.Pd., M.Pd.
  - Kepala Laboratorium: Dody Erlangga, S.Kom. (diperbarui di Fase 15).
  - Koordinator Sarana & Prasarana: Prio Jaka Arsyad, S.Kom.
- [x] 14.4 Integrasi Halaman Pengabdian kepada Masyarakat (PkM):
  - Buat halaman `src/pages/riset/pengabdian/index.astro` dan `src/pages/en/research/community-service/index.astro`.
  - Masukkan ke menu dropdown Riset di `navigation.json` dan Footer.
  - Sajikan 5 pilar program PkM dosen berbasis riset terapan bagi UMKM, sekolah, desa cerdas, dan ASN daerah.
- [x] 14.5 Rebranding Frasa Nama Prodi:
  - Ubah seluruh frasa "S1 Sistem Informasi" menjadi "Sistem Informasi" saja (Header, Drawer, Footer, BaseLayout, judul halaman, dan metadata).
- [x] 14.6 Kompilasi SSG (`npm run build`), verifikasi visual via browser CDP, dan commit git lokal: `[main 8c9570b]`.

---

### Fase 15: Pembaruan Kepala Lab (Dody), Integrasi Logo Diktisaintek & Favicon Tab SisfoUNDA
- [x] 15.1 Penetapan Kepala Laboratorium menjadi Dody Erlangga, S.Kom. pada struktur organisasi (`profil/index.astro` dan `en/about/index.astro`).
- [x] 15.2 Integrasi logo resmi DIKTISAINTEK BERDAMPAK (`logo-diktisaintek.png`) di seksi Akreditasi dan Footer institusi.
- [x] 15.3 Penggantian ikon tab browser (*favicon*) dengan logo resmi SisfoUNDA:
  - Dihasilkan berkas multi-resolusi: `favicon.ico`, `favicon-16x16.png`, `favicon-32x32.png`, `favicon-48x48.png`, `favicon-64x64.png`, `favicon-192x192.png`, `favicon-512x512.png`, `apple-touch-icon.png` (180x180), dan `favicon.svg`.
  - Dihubungkan lengkap di `src/layouts/BaseLayout.astro`.
- [x] 15.4 Kompilasi SSG (`npm run build` lulus 100%, 0 error), verifikasi via browser CDP, dan commit git lokal: `[main b1de0f1]`.

---

### Fase 16: Eksekusi Opsi 1 (CTA SPMB ke /pmb/), Audit Orphan Pages, Eliminasi Penomoran Dua Digit & Kalibrasi Foto Aziz/Dody
- [x] 16.1 Eksekusi Opsi 1 (Integrasi Halaman PMB):
  - Hubungkan tombol utama Header `DAFTAR SPMB →` (Desktop & Mobile Drawer) langsung ke `/pmb/` (ID) dan `/en/admissions/` (EN).
  - Hubungkan tautan SPMB di Footer ke `/pmb/` dan `/en/admissions/`.
- [x] 16.2 Hasil Audit Orphan Pages:
  - Terverifikasi 100% dari 33 berkas rute halaman di `src/pages/` telah terhubung ke navigasi global dan footer (zero orphan pages).
- [x] 16.3 Eliminasi Penomoran Dua Digit:
  - Hapus `01`, `02`, `03`, `04` dari kartu 4 Pilar Akademik di Beranda (`AcademicPillars.astro`).
  - Hapus `01`, `02`, `03`, `04` dari sticky sub-navigasi dan judul bab seksi di Halaman Profil (`profil/index.astro` dan `en/about/index.astro`).
- [x] 16.4 Kalibrasi Foto Pak Aziz & Kak Dody:
  - `aziz.jpg`: geser x1=95 (Pak Aziz bergeser ke kanan simetris di tengah bingkai).
  - `dody.jpg`: potong headroom berlebih (mulai y=880) agar wajah Kak Dody naik proporsional sejajar dengan dosen lainnya.
- [x] 16.5 Kompilasi SSG (`npm run build`), verifikasi visual via browser CDP, dan commit git lokal: `[main 5cb514f]`.

---

### Fase 17: Dokumentasi Vault & Pembaruan Nomor WhatsApp Resmi
- [x] 17.1 Buat dokumen panduan komprehensif di Obsidian Vault: `Projects/website_prodi/Panduan Upload GitHub dan Deployment Website Prodi.md`.
- [x] 17.2 Perbarui nomor WhatsApp resmi prodi menjadi `0851-7158-8808` (`https://wa.me/6285171588808`) pada `navigation.json`, Footer, halaman Kontak ID, dan halaman Kontak EN.
- [x] 17.3 Kompilasi SSG (`npm run build` lulus 100%, 0 error) dan commit git lokal: `[main 0cc1f07]`.

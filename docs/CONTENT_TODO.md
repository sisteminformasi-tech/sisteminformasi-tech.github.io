# Checklist Konten & Pemutakhiran Berkala (CONTENT_TODO)

Daftar aset dan materi yang dapat diperbarui secara berkala oleh staf prodi atau pengelola website:

- [ ] **Foto Representatif Dosen**: Mengunggah foto formal seluruh 12 dosen tetap dan 3 asisten dosen ke folder `public/images/dosen/[slug].jpg`. Saat ini sistem menggunakan inisial monogram berwibawa khas universitas yang rapi dan elegan.
- [ ] **Foto Gedung & Laboratorium**: Menambahkan dokumentasi visual fasilitas laboratorium komputer FIK UNDA untuk melengkapi galeri beranda dan laman mahasiswa.
- [ ] **Update Metrik SINTA & Scopus Semesteran**: Memperbarui skor SINTA dan H-Index dosen di `src/data/civitas.json` setiap akhir tahun anggaran penelitian.
- [ ] **Penambahan Publikasi Kelompok Riset**: Memasukkan publikasi jurnal terbaru tahun berjalan ke dalam 5 kelompok riset di `src/data/research_groups.json`.
- [ ] **Formulir Kontak Backend**: Menghubungkan action form di `src/pages/kontak/index.astro` dengan endpoint form serverless (seperti Formspree, Formkeep, atau Web3Forms) jika ingin formulir langsung terkirim tanpa membuka email client pengunjung.

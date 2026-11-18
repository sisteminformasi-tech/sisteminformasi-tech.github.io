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
- [ ] 14.1 Penyesuaian Foto Dr. Dwi (Geser ke Kanan) & Foto Pak Aziz (Naikkan Sumbu Wajah):
  - `bowo.jpg`: geser crop window agar subjek bergeser ke kanan simetris di tengah bingkai.
  - `aziz.jpg`: potong headroom berlebih (mulai y=170) dan pusatkan sumbu kepala di x=390 agar wajah naik proporsional.
- [ ] 14.2 Integrasi Foto Asdos Prio Jaka Arsyad (`prio.jpg`):
  - Ambil dari `/Works - UNDA/Web-Sisfo-UNDA/public/prio.jpg`, crop 1:1 persegi (800x800 Lanczos), simpan ke `public/images/dosen/prio.jpg`.
  - Hubungkan ke `src/data/civitas.json` pada properti `image` Prio.
- [ ] 14.3 Pembaruan Struktur Organisasi Prodi (`profil/index.astro` & `en/about/index.astro`):
  - Dekan & Ketua Program Studi: Dr. Dwi Wahyu Prabowo, S.Si., M.Eng.
  - Sekretaris Program Studi: Eka Prasetyaningrum, S.Kom., M.M.
  - Pengelola MBKM: Elika Thea Kirana, S.T., M.Kom.
  - Gugus Kendali Mutu: Nurahman, S.Kom., M.M., M.Kom.
  - Koordinator Kemahasiswaan & Alumni: Abdul Aziz, S.Pd., M.Pd.
  - Kepala Laboratorium: Agung Purwanto, S.Kom., M.Kom.
  - Koordinator Sarana & Prasarana: Prio Jaka Arsyad, S.Kom.
- [ ] 14.4 Integrasi Halaman Pengabdian kepada Masyarakat (PkM):
  - Buat halaman `src/pages/riset/pengabdian/index.astro` dan `src/pages/en/research/community-service/index.astro`.
  - Masukkan ke menu dropdown Riset di `navigation.json` dan Footer.
  - Sajikan 5 pilar program PkM dosen berbasis riset terapan bagi UMKM, sekolah, desa cerdas, dan ASN daerah.
- [ ] 14.5 Rebranding Frasa Nama Prodi:
  - Ubah seluruh frasa "S1 Sistem Informasi" menjadi "Sistem Informasi" saja (Header, Drawer, Footer, BaseLayout, judul halaman, dan metadata).
- [ ] 14.6 Kompilasi SSG (`npm run build`), verifikasi visual via browser CDP, dan commit git lokal.

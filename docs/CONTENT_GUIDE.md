# Panduan Pemutakhiran Konten Website Prodi S1 Sistem Informasi

Panduan ini ditujukan bagi pengelola portal prodi, asisten dosen, atau staf administrasi untuk memutakhirkan data kurikulum, RPS, profil dosen, dan publikasi berita secara mudah tanpa merusak tata letak website.

---

## 1. Menambah atau Mengubah Data Dosen / Asdos

Seluruh master data profil dosen dan asisten dosen tersimpan pada file JSON terstruktur:
`src/data/civitas.json`

### Format Entri Dosen:
```json
{
  "name": "Nama Lengkap, Gelar Resmi",
  "position": "Dosen Tetap S1 Sistem Informasi",
  "functional_rank": "Asisten Ahli / Lektor",
  "nuptk": "16 Digit NUPTK Resmi",
  "sinta_id": "6027394",
  "sinta_url": "https://sinta.kemdiktisaintek.go.id/authors/profile/...",
  "sinta_score_overall": "372",
  "sinta_score_3yr": "143",
  "scopus_url": "https://www.scopus.com/authid/detail.uri?authorId=...",
  "scopus_docs": "7",
  "scopus_cits": "85",
  "scopus_hindex": "4",
  "gs_url": "https://scholar.google.com/citations?user=...",
  "gs_docs": "30",
  "gs_cits": "204",
  "gs_hindex": "7",
  "email": "nama@unda.ac.id",
  "personal_web": "http://staff.unda.ac.id/...",
  "education": [
    "S1: Sarjana Sains (S.Si.), Universitas Indonesia",
    "S2: Master of Engineering (M.Eng.), Universitas Gadjah Mada",
    "S3: Doktor (Dr.), Universitas Gadjah Mada"
  ],
  "expertise": ["Kecerdasan Buatan", "Sains Data", "Bio-Signal EEG"],
  "selected_publications": [
    "Judul paper bereputasi Scopus Q1...",
    "Judul paper bereputasi lainnya..."
  ],
  "courses_taught": ["Kecerdasan Buatan", "Sains Data", "Skripsi"],
  "slug": "nama-dosen-slug",
  "role_category": "faculty"
}
```

*Catatan Keras: DILARANG mengarang nomor NIDN atau NUPTK. Wajib mengacu pada master data institusi.*

---

## 2. Menambah Berkas Master RPS PDF Baru

1. Salin berkas PDF RPS baru ke folder:
   `public/rps/`
   *Contoh nama berkas:* `RPS_KODEMK_Nama_Mata_Kuliah.pdf`
2. Tambahkan metadata berkas ke:
   `src/data/rps.json`
   ```json
   {
     "code": "KODEMK",
     "name": "Nama Mata Kuliah",
     "filename": "RPS_KODEMK_Nama_Mata_Kuliah.pdf",
     "category": "C.1. MATA KULIAH PONDASI RUMPUN KEILMUAN SISTEM INFORMASI",
     "size_kb": 450.5,
     "semester": 1,
     "download_url": "/rps/RPS_KODEMK_Nama_Mata_Kuliah.pdf"
   }
   ```
3. Jalankan `npm run build` agar Pagefind mengindeks berkas baru.

---

## 3. Menambah Warta Berita & Pengumuman Baru

Buka file halaman berita:
- Bahasa Indonesia: `src/pages/berita/index.astro`
- English: `src/pages/en/news/index.astro`

Tambahkan objek berita ke dalam array `newsItems`:
```ts
{
  title: 'Judul Berita Menarik dan Formal',
  date: 'DD Bulan YYYY',
  category: 'Akademik / Riset / Prestasi',
  author: 'Sekretariat Prodi SI',
  summary: 'Ringkasan singkat berita 1 kalimat...',
  content: 'Paragraf isi lengkap berita...'
}
```

---

## 4. Memverifikasi Perubahan

Setelah mengubah file JSON atau halaman:
```bash
npm run build
```
Pastikan kompilasi berakhir dengan status:
`[build] Complete!` dan Pagefind berhasil mengindeks seluruh halaman.

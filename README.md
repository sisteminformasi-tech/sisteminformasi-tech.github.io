# Website Resmi Program Studi S1 Sistem Informasi — Universitas Darwan Ali

> **Program Studi S1 Sistem Informasi**  
> Fakultas Ilmu Komputer, Universitas Darwan Ali, Sampit, Kotawaringin Timur  
> Status Akreditasi: **Baik Sekali** (BAN-PT / LAM INFOKOM)  
> Generator: **Astro v5 (Pure Static SSG)** · Styling: **Tailwind CSS (Royal Academic Palette)** · Search: **Pagefind** · Bilingual: **ID / EN**

---

## 🏛️ Gambaran Umum

Repositori ini memuat kode sumber website statis resmi Program Studi S1 Sistem Informasi FIK UNDA. Website ini dirancang dengan standar kualitas institusional tinggi, bebas dari gaya klise kecerdasan buatan (*Anti AI Slop*), cepat dibuka pada koneksi internet daerah (*zero client JS framework overhead*), dan terintegrasi dengan ekosistem digital kampus.

### Fitur Kunci:
1. **Kurikulum OBE 144 SKS Penuh**: Pemetaan 3 Profil Lulusan (PL), 10 Capaian Pembelajaran Lulusan (CPL), 14 Bahan Kajian (BK), matriks sebaran semester 1 s.d. 8, dan Taksonomi Bloom interaktif.
2. **Repositori Master RPS PDF**: 83 dokumen RPS PDF resmi dengan fitur filter instan dan unduhan langsung.
3. **Direktori Civitas Akademika Ber-NUPTK**: Profil 12 Dosen Tetap ber-NUPTK resmi dan 3 Asisten Dosen dengan metrik sitasi (SINTA, Scopus, Google Scholar).
4. **5 Kelompok Riset Dosen**: AIML-RG, SETK-RG, MHUI-RG, DSDSS-RG, dan EDUTECH-RG lengkap dengan roadmap dan topik skripsi terbuka bagi mahasiswa.
5. **Dukungan Bilingual Penuh (ID/EN)**: Toggle switcher `[ID | EN]` pada header desktop dan mobile drawer tanpa 404.
6. **Pencarian Statis Pagefind**: Mesin pencari client-side super cepat tanpa backend server.

---

## 🛠️ Persyaratan Lingkungan

- Node.js `>= 20.x` (Direkomendasikan Node.js v22+)
- npm `>= 10.x`

---

## 🚀 Panduan Menjalankan di Lokal

### 1. Kloning dan Instalasi Dependensi
```bash
cd ~/projects/website-prodi-si
npm install
```

### 2. Mode Pengembangan (Development)
```bash
npm run dev
```
Akses server lokal di `http://localhost:4321/` atau `http://localhost:4321/website-prodi-si/`.

### 3. Build Produksi & Pengindeksan Pagefind
```bash
npm run build
```
Perintah ini akan menjalankan pemeriksaan tipe (`astro check`), kompilasi statis (`astro build`), dan pengindeksan dokumen (`pagefind --site dist`).

### 4. Menjalankan Preview Hasil Build
```bash
npm run preview
```

---

## 📂 Struktur Direktori Proyek

```
website-prodi-si/
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Pages CI/CD workflow
├── docs/
│   ├── CONTENT_GUIDE.md        # Panduan admin/staf memperbarui konten
│   ├── CONTENT_TODO.md         # Checklist pembaruan data berkala
│   └── DEPLOY.md               # Panduan remote setup, push mandiri, custom domain
├── public/
│   ├── favicon.svg
│   ├── robots.txt
│   ├── CNAME                   # Diisi nama subdomain resmi (.unda.ac.id)
│   ├── pagefind/               # Aset statis UI pencarian
│   └── rps/                    # 83 Berkas RPS PDF resmi
├── src/
│   ├── components/
│   │   ├── common/             # Header, Footer, LanguageToggle, SearchModal
│   │   └── home/               # Hero, PortalQuickAccess, DeanMessage, CurriculumHighlights
│   ├── data/
│   │   ├── civitas.json        # Master data 12 dosen tetap & 3 asdos
│   │   ├── curriculum.json     # Data kurikulum OBE 144 SKS & Bloom
│   │   ├── navigation.json     # Menu navigasi & tautan portal kampus
│   │   ├── research_groups.json# 5 Kelompok riset dosen
│   │   └── rps.json            # Katalog 83 dokumen RPS PDF
│   ├── i18n/
│   │   ├── ui.ts               # Kamus terjemahan antarmuka (ID & EN)
│   │   └── utils.ts            # Helper rute & pemetaan bahasa aktif
│   ├── layouts/
│   │   └── BaseLayout.astro    # Master layout (SEO, Schema.org, skip-link)
│   ├── pages/                  # Halaman statis Bahasa Indonesia (default /)
│   │   └── en/                 # Halaman statis English (/en/)
│   └── styles/
│       └── global.css          # Design tokens Royal Academic Palette
└── astro.config.mjs
```

---

## 🔒 Kebijakan Git & Deployment

- Repositori lokal ini **TIDAK PERNAH melakukan auto-push** ke GitHub.
- Unggah mandiri dilakukan oleh Bapak ke repositori: `https://github.com/sisteminformasi-tech/website-prodi-si`.
- Panduan deployment lengkap dan integrasi custom domain `.unda.ac.id` dapat dibaca pada [`docs/DEPLOY.md`](docs/DEPLOY.md).

---

## 📄 Hak Cipta & Lisensi

&copy; 2026 Program Studi S1 Sistem Informasi, Fakultas Ilmu Komputer, Universitas Darwan Ali.
Hak Cipta Dilindungi Undang-Undang.

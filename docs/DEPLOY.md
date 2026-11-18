# Panduan Deployment Mandiri ke GitHub Pages & Custom Domain

Sesuai kebijakan keamanan dan doktrin AI-OS, Hermes dan agen AI **DILARANG KERAS melakukan `git push` otomatis** ke repositori luar. Pengunggahan kode ke remote dilakukan secara sadar dan mandiri oleh Bapak (Dr. Dwi Wahyu Prabowo).

---

## 1. Remote Setup Mandiri

Repositori lokal telah diinisialisasi pada branch `main` dengan seluruh commit tersimpan rapi.

Jalankan perintah berikut pada terminal:
```bash
cd ~/projects/website-prodi-si

# Tambahkan remote organisasi
git remote add origin https://github.com/sisteminformasi-tech/website-prodi-si.git

# Pastikan branch berada di main
git branch -M main

# Unggah seluruh commit lokal
git push -u origin main
```

---

## 2. Mengundang Akun Personal sebagai Kolaborator

1. Buka repositori di browser:
   `https://github.com/sisteminformasi-tech/website-prodi-si/settings/access`
2. Klik tombol **"Add people"**.
3. Masukkan username GitHub personal Bapak: `akhbow`
4. Pilih peran akses (Admin / Write).
5. Akun `akhbow` kini dapat mengelola repositori secara langsung.

---

## 3. Mengaktifkan GitHub Pages

1. Masuk ke tab **Settings** → **Pages** pada repositori GitHub.
2. Pada bagian **Build and deployment**:
   - **Source**: Pilih **GitHub Actions**.
3. Workflow `.github/workflows/deploy.yml` yang telah disiapkan akan otomatis terpicu saat push ke branch `main`, mengompilasi Astro SSG, menjalankan pengindeksan Pagefind, dan mempublikasikan situs ke:
   `https://sisteminformasi-tech.github.io/website-prodi-si/`

---

## 4. Mengonfigurasi Custom Subdomain Resmi (`.unda.ac.id`)

Bila pihak universitas / UPT TIK UNDA telah menyiapkan subdomain resmi (misalnya `sisfo.unda.ac.id` atau `si.fikom.unda.ac.id`):

1. **DNS Record di Cloudflare / BIND Server Kampus**:
   - Tipe: `CNAME`
   - Name: `sisfo` (atau `si`)
   - Target: `sisteminformasi-tech.github.io`
2. **Konfigurasi CNAME Repositori**:
   - Tulis nama domain ke file `public/CNAME`:
     ```bash
     echo "sisfo.unda.ac.id" > ~/projects/website-prodi-si/public/CNAME
     ```
   - Ubah parameter `base` di `astro.config.mjs` menjadi `'/'` (root domain).
   - Commit lokal dan push ke GitHub.
3. Di dashboard GitHub Pages repositori, masukkan domain pada kolom **Custom domain** dan centang **Enforce HTTPS**.

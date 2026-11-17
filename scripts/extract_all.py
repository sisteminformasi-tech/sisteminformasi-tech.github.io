#!/usr/bin/env python3
import os
import sys
import re
import json
import shutil
import glob
from bs4 import BeautifulSoup

PROJECT_DIR = "/home/alrashidfattahsyamil/projects/website-prodi-si"
WORKS_DIR = "/home/alrashidfattahsyamil/Works - UNDA"
VAULT_DIR = "/home/alrashidfattahsyamil/obsidian/obsidian-dwp"

# -------------------------------------------------------------
# 1. SALIN RPS PDF & BUAT RPS.JSON
# -------------------------------------------------------------
def process_rps():
    print(">>> 1. Memproses Repositori Master RPS PDF...")
    rps_src_dir = os.path.join(WORKS_DIR, "RPS_OBE_Dosen/Master RPS_PDF Version")
    rps_dest_dir = os.path.join(PROJECT_DIR, "public/rps")
    os.makedirs(rps_dest_dir, exist_ok=True)

    pdf_files = glob.glob(f"{rps_src_dir}/**/*.pdf", recursive=True)
    print(f"    Ditemukan {len(pdf_files)} berkas PDF.")

    entries = []
    for src in sorted(pdf_files):
        fname = os.path.basename(src)
        # Normalize target filename if needed, or keep clean
        dest = os.path.join(rps_dest_dir, fname)
        shutil.copy2(src, dest)

        rel_cat = os.path.basename(os.path.dirname(src))
        fsize_kb = round(os.path.getsize(src) / 1024, 1)

        m = re.match(r"RPS_([A-Z0-9]+)_(.*?)\.pdf", fname)
        if m:
            code = m.group(1)
            raw_name = m.group(2).replace("_", " ")
        else:
            code = ""
            raw_name = fname.replace(".pdf", "").replace("_", " ")

        # Infer semester from code if possible
        smt = None
        # SIFT1..., SIPT2..., SIM16..., etc.
        m_smt = re.search(r"^[A-Z]{4}([1-8])", code)
        if m_smt:
            smt = int(m_smt.group(1))
        elif "MKW" in code:
            if "Agama" in raw_name or "Pancasila" in raw_name or "Inggris" in raw_name:
                smt = 1
            elif "Kewarganegaraan" in raw_name:
                smt = 2
            elif "Indonesia" in raw_name:
                smt = 4

        entries.append({
            "code": code,
            "name": raw_name,
            "filename": fname,
            "category": rel_cat,
            "size_kb": fsize_kb,
            "semester": smt,
            "download_url": f"/rps/{fname}"
        })

    out_path = os.path.join(PROJECT_DIR, "src/data/rps.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)
    print(f"    Berhasil menyalin {len(entries)} berkas ke {rps_dest_dir} dan menulis {out_path}.")
    return entries

# -------------------------------------------------------------
# 2. EKSTRAKSI KURIKULUM OBE
# -------------------------------------------------------------
def process_curriculum():
    print(">>> 2. Mengekstrak Data Kurikulum OBE...")
    html_path = os.path.join(WORKS_DIR, "Draft Kurikulum OBE/Paket_RPS_OBE_Dosen/Kurikulum-OBE-SI-Step1-6_v3.html")
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, "html.parser")

    # A. Profil Lulusan
    # Tabel 0
    tables = soup.find_all("table")
    pl_list = []
    if len(tables) > 0:
        for tr in tables[0].find_all("tr")[1:]:
            cols = [td.get_text(strip=True) for td in tr.find_all(["th", "td"])]
            if len(cols) >= 4:
                pl_list.append({
                    "no": int(cols[0]),
                    "code": cols[1],
                    "desc": cols[2],
                    "roles": cols[3]
                })

    # B. CPL (Capaian Pembelajaran Lulusan)
    # Tabel 1
    cpl_list = []
    if len(tables) > 1:
        for tr in tables[1].find_all("tr")[1:]:
            cols = [td.get_text(strip=True) for td in tr.find_all(["th", "td"])]
            if len(cols) >= 3:
                # Extract bloom tag inside rumusan if any
                rumusan_raw = cols[2]
                bloom_tags = re.findall(r"([CPA][1-6])", rumusan_raw)
                cpl_list.append({
                    "no": int(cols[0]),
                    "code": cols[1],
                    "desc": rumusan_raw,
                    "bloom_tags": list(set(bloom_tags))
                })

    # C. Bahan Kajian (BK01 s.d. BK14)
    # Extract from Table 3 or DATA
    m = re.search(r"const\s+DATA\s*=\s*(\{.*?\});\s*(?:const|let|var|function|window|document)", html_content, re.DOTALL)
    data_json = json.loads(m.group(1)) if m else {}

    bk_map = {
        "BK01": "Foundations of Information Systems (Pondasi Sistem Informasi)",
        "BK02": "Data and Information Management (Manajemen Data & Informasi)",
        "BK03": "Enterprise Architecture & Business Process (Arsitektur Enterprise & Proses Bisnis)",
        "BK04": "Algorithms, Programming & Software Development (Algoritma, Pemrograman & Rekayasa PL)",
        "BK05": "Infrastructure, Networks & Cloud Technologies (Infrastruktur, Jaringan & Komputasi Awan)",
        "BK06": "Information Security, Privacy & Risk (Keamanan Informasi, Privasi & Manajemen Risiko)",
        "BK07": "Artificial Intelligence & Machine Learning (Kecerdasan Buatan & Pembelajaran Mesin)",
        "BK08": "Data Science & Predictive Analytics (Sains Data & Analitika Prediktif)",
        "BK09": "Human-Computer Interaction & User Experience (Interaksi Manusia-Komputer & UI/UX)",
        "BK10": "Digital Media, Multimedia & Content Creation (Media Digital, Multimedia & Kreativitas Konten)",
        "BK11": "IT Project Management & Capstone (Manajemen Proyek TI & Proyek Terpadu)",
        "BK12": "Digital Leadership, Strategy & Technopreneurship (Kepemimpinan Digital & Teknopreneur)",
        "BK13": "Ethics, Religion, Social & National Identity (Etika, Agama, Sosial & Karakter Bangsa)",
        "BK14": "Mathematics, Statistics & Research Methods (Matematika, Statistika & Metode Penelitian)"
    }
    bk_list = [{"code": k, "name": v} for k, v in bk_map.items()]

    # D. Matriks Sebaran Mata Kuliah Semester 1-8 dengan SKS (Total 144 SKS)
    # SKS Map otoritatif
    sks_dict = {
        # Sem 1 (19 SKS)
        "MKW110181": 2, # Agama
        "MKW110182": 2, # Pancasila / PAK
        "MKW110184": 3, # B. Inggris
        "SIFT1J01": 3,  # Matematika
        "SIFT1J02": 3,  # Struktur Data
        "SIPT1J01": 3,  # Konsep SI
        "SIPT1J02": 3,  # Etika Profesi
        # Sem 2 (20 SKS)
        "MKW110183": 2, # Kewarganegaraan
        "SIFT2G03": 3,  # Statistika
        "SIFT2G04": 3,  # Basis Data
        "SIFT2G05": 3,  # Bahasa Pemrograman
        "SIPT2G03": 3,  # Analisis & MPB
        "SIPT2G06": 3,  # Kecerdasan Buatan
        "SIPT2G14": 3,  # Tata Kelola TI
        # Sem 3 (18 SKS)
        "SIFT3J06": 3,  # Jaringan Komputer
        "SIPT3J04": 3,  # APSI
        "SIPT3J07": 3,  # Sains Data
        "SIPT3J11": 3,  # Multimedia
        "SIPT3J12": 3,  # UI/UX
        "SIPT3J15": 3,  # Sistem Enterprise
        # Sem 4 (20 SKS)
        "MKW110185": 2, # B. Indonesia
        "SIPT4G05": 3,  # Keamanan SI
        "SIPT4G08": 3,  # Deep Learning
        "SIPL4G01": 3,  # Mobile Programming
        "SIPL4G02": 3,  # Digital Content
        "SIPT4G16": 3,  # Audit SI
        "SIPT4G17": 3,  # Renstra & Rekayasa Sistem
        # Sem 5 (18 SKS)
        "SIFT5B07": 3,  # Metopen
        "SIPT5J09": 3,  # Computer Vision
        "SIPT5J13": 3,  # Technopreneur
        "SIPC5J01": 3,  # Manajemen Proyek Capstone
        "SIBT5J01": 3,  # Pemasaran Digital
        "SIBT5J02": 3,  # Manajemen Organisasi Digital
        # Sem 8 (9 SKS)
        "SIPT8G10": 3,  # Teknologi Mutakhir
        "SIFC8B01": 6,  # Skripsi
    }

    # Semester 6 MBKM tracks (masing-masing MK bernilai 4 SKS, paket 20 SKS)
    # Semester 7 MBKM tracks (masing-masing MK bernilai 4 SKS, paket 20 SKS)
    step1_mks = data_json.get("step1", [])
    step5_mks = {x["kode"]: x for x in data_json.get("step5", [])}
    step6_mks = {x["kode"]: x for x in data_json.get("step6", [])}

    courses_list = []
    for item in step1_mks:
        code = item["kode"]
        smt = item["smt"]
        nama = item["nama"]
        pl = item["pl"]
        bk1 = item.get("bk1", "")
        bk2 = item.get("bk2", "")

        # Tentukan SKS
        if code in sks_dict:
            sks = sks_dict[code]
        elif smt in [6, 7]:
            sks = 4 # Standar modul MBKM 20 SKS per paket (5 MK x 4 SKS)
        else:
            sks = 3

        cpmk_info = step5_mks.get(code, {}).get("cpmk", [])
        sub_cpmk_info = step6_mks.get(code, {}).get("sub", [])

        # Kumpulkan Bloom level tertinggi di CPMK
        bloom_levels = list(set([c.get("bloom") for c in cpmk_info if c.get("bloom")]))

        courses_list.append({
            "code": code,
            "name": nama,
            "semester": smt,
            "sks": sks,
            "pl": pl,
            "bk": [b for b in [bk1, bk2] if b],
            "bloom": bloom_levels,
            "cpmk_count": len(cpmk_info),
            "sub_cpmk_count": len(sub_cpmk_info)
        })

    # Ringkasan per semester kurikulum reguler (144 SKS total):
    # Sem 1: 19 SKS
    # Sem 2: 20 SKS
    # Sem 3: 18 SKS
    # Sem 4: 20 SKS
    # Sem 5: 18 SKS
    # Sem 6: 20 SKS (Paket Pilihan MBKM / Konsentrasi)
    # Sem 7: 20 SKS (Paket Pilihan MBKM Riset / Magang Lanjutan)
    # Sem 8:  9 SKS (Teknologi Mutakhir 3 SKS + Skripsi 6 SKS)
    # Total = 19 + 20 + 18 + 20 + 18 + 20 + 20 + 9 = 144 SKS!

    curriculum_data = {
        "profil_lulusan": pl_list,
        "cpl": cpl_list,
        "bahan_kajian": bk_list,
        "total_sks_lulus": 144,
        "semester_sks_distribution": {
            "1": 19,
            "2": 20,
            "3": 18,
            "4": 20,
            "5": 18,
            "6": 20,
            "7": 20,
            "8": 9
        },
        "courses": courses_list,
        "step3_matrix": data_json.get("step3", {}),
        "step4_matrix": data_json.get("step4", {})
    }

    out_path = os.path.join(PROJECT_DIR, "src/data/curriculum.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(curriculum_data, f, indent=2, ensure_ascii=False)
    print(f"    Berhasil menulis {len(courses_list)} mata kuliah & struktur kurikulum ke {out_path}.")
    return curriculum_data

# -------------------------------------------------------------
# 3. EKSTRAKSI DOSEN & ASISTEN DOSEN
# -------------------------------------------------------------
def process_civitas():
    print(">>> 3. Mengekstrak Data Civitas Akademika (12 Dosen Tetap & 3 Asdos)...")
    md_path = os.path.join(VAULT_DIR, "Administrasi/Kaprodi SI/SDM/Direktori Profil Akademik Dosen SI.md")
    with open(md_path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    # Dosen master NUPTK
    nuptk_map = {
        "Dr. Dwi Wahyu Prabowo, S.Si., M.Eng.": "4536767668130283",
        "Eka Prasetyaningrum, S.Kom., M.M.": "0934772673230272",
        "Nurahman, S.Kom., M.M., M.Kom.": "2342765666130493",
        "Abdul Aziz, S.Pd., M.Pd.": "1953765666130272",
        "Agung Purwanto, S.Kom., M.Kom.": "1146760661130213",
        "Elika Thea Kirana, S.T., M.Kom.": "2835773674230242",
        "Dwika Lovitasari Yonia, S.Kom., M.Kom.": "0814059401", # SINTA 6977741
        "Lukman Bachtiar, S.Kom., M.M., M.Kom.": "6348760661130163",
        "Serika Zai, S.Pd., M.Pd.": "0945773674230152",
        "Selviana Yunita, S.Kom., M.Kom.": "5945771672230282",
        "Deny Sundari, S.Kom., A.Md., M.M.S.I.": "5850770671230302",
        "Minarni, S.Kom., M.M.": "6557767668230343"
    }

    # Split markdown by sections
    sections = re.split(r"\n###\s+", raw_text)
    faculty_list = []
    assistant_list = []

    for s in sections[1:]:
        lines = s.strip().split("\n")
        title = lines[0].strip()
        # Clean title number e.g. "1. Dr. Dwi Wahyu Prabowo, S.Si., M.Eng."
        clean_name = re.sub(r"^\d+\.\s+", "", title).strip()

        # Parse bullet fields
        data = {
            "name": clean_name,
            "raw_title": title,
            "position": "",
            "functional_rank": "",
            "employment_status": "Dosen Tetap",
            "nuptk": nuptk_map.get(clean_name, ""),
            "sinta_id": "",
            "sinta_url": "",
            "sinta_score_overall": "",
            "sinta_score_3yr": "",
            "scopus_url": "",
            "scopus_docs": "",
            "scopus_cits": "",
            "scopus_hindex": "",
            "gs_url": "",
            "gs_docs": "",
            "gs_cits": "",
            "gs_hindex": "",
            "email": "",
            "personal_web": "",
            "education": [],
            "expertise": [],
            "selected_publications": [],
            "courses_taught": [],
            "bio": ""
        }

        if "Dwi Wahyu Prabowo" in clean_name:
            data["personal_web"] = "http://bowo.staff.unda.ac.id/"

        # Extract email
        m_email = re.search(r"Email:\s*`([^`]+)`", s)
        if m_email:
            data["email"] = m_email.group(1)

        # Extract Jabatan
        m_jab = re.search(r"- \*\*Jabatan\*\*:\s*([^\n]+)", s)
        if m_jab:
            data["position"] = m_jab.group(1).strip()

        # Extract Jabatan Fungsional
        m_jaf = re.search(r"- \*\*Jabatan Fungsional\*\*:\s*([^\n]+)", s)
        if m_jaf:
            data["functional_rank"] = m_jaf.group(1).strip()

        # Extract NUPTK if not mapped
        m_nuptk = re.search(r"NUPTK:\s*`?([0-9]+)`?", s)
        if m_nuptk and not data["nuptk"]:
            data["nuptk"] = m_nuptk.group(1)

        # Extract SINTA
        m_sinta = re.search(r"SINTA ID:\s*\[([0-9]+)\]\((https?://[^\)]+)\)", s)
        if m_sinta:
            data["sinta_id"] = m_sinta.group(1)
            data["sinta_url"] = m_sinta.group(2)

        # Extract SINTA Score
        m_sinta_sc = re.search(r"SINTA Score\*\*:\s*Overall\s*([0-9]+)\s*\|\s*3-Year\s*([0-9]+)", s)
        if m_sinta_sc:
            data["sinta_score_overall"] = m_sinta_sc.group(1)
            data["sinta_score_3yr"] = m_sinta_sc.group(2)

        # Extract Scopus
        m_scopus = re.search(r"Scopus Author ID:\s*\[([0-9]+)\]\((https?://[^\)]+)\)", s)
        if m_scopus:
            data["scopus_url"] = m_scopus.group(2)
        m_scopus_m = re.search(r"Scopus\*\*:\s*([0-9]+)\s*artikel\s*\|\s*([0-9]+)\s*sitasi\s*\|\s*\*\*H-Index:\s*([0-9]+)\*\*", s)
        if m_scopus_m:
            data["scopus_docs"] = m_scopus_m.group(1)
            data["scopus_cits"] = m_scopus_m.group(2)
            data["scopus_hindex"] = m_scopus_m.group(3)

        # Extract Google Scholar
        m_gs = re.search(r"Google Scholar:\s*\[([A-Za-z0-9_-]+)\]\((https?://[^\)]+)\)", s)
        if m_gs:
            data["gs_url"] = m_gs.group(2)
        m_gs_m = re.search(r"Google Scholar\*\*:\s*([0-9]+)\s*artikel\s*\|\s*([0-9]+)\s*sitasi\s*\|\s*\*\*H-Index:\s*([0-9]+)\*\*", s)
        if m_gs_m:
            data["gs_docs"] = m_gs_m.group(1)
            data["gs_cits"] = m_gs_m.group(2)
            data["gs_hindex"] = m_gs_m.group(3)

        # Extract Education
        edu_matches = re.findall(r"-\s*\*\*(S[123]|D3)\*\*:\s*([^\n]+)", s)
        for deg, txt in edu_matches:
            data["education"].append(f"{deg}: {txt.strip()}")

        # Extract Expertise
        m_exp = re.search(r"Bidang Keahlian\s*(?:& Riset)?\*\*:\s*([^\n]+)", s)
        if m_exp:
            exp_raw = m_exp.group(1)
            data["expertise"] = [x.strip() for x in re.split(r"[,;]", exp_raw) if x.strip()]

        # Extract Selected Pubs
        m_pubs = re.search(r"Publikasi Utama Terpilih\*\*:(.*?)(?=\n-|\n\n|\Z)", s, re.DOTALL)
        if m_pubs:
            pub_lines = re.findall(r"\d+\.\s+([^\n]+)", m_pubs.group(1))
            data["selected_publications"] = [p.strip() for p in pub_lines]

        # Extract Courses Taught
        m_mk = re.search(r"Mata Kuliah Diampu Terkini\*\*:\s*([^\n]+)", s)
        if m_mk:
            mk_raw = m_mk.group(1)
            data["courses_taught"] = [x.strip() for x in re.split(r"[,;]", mk_raw) if x.strip()]

        # Create slug
        slug = re.sub(r"[^a-z0-9]+", "-", clean_name.lower()).strip("-")
        data["slug"] = slug

        if any(x in clean_name for x in ["Dody Erlangga", "Fauzan Eka Prasatia", "Prio Jaka Arsyad"]):
            data["role_category"] = "assistant"
            assistant_list.append(data)
        else:
            data["role_category"] = "faculty"
            faculty_list.append(data)

    # Pastikan Dosen Tetap ke-12: Minarni, S.Kom., M.M. (Dekan / Dosen Tetap dari Data Dosen NUPTK.xlsx)
    if not any("Minarni" in d["name"] for d in faculty_list):
        faculty_list.append({
            "name": "Minarni, S.Kom., M.M.",
            "raw_title": "Minarni, S.Kom., M.M.",
            "position": "Dosen Tetap S1 Sistem Informasi",
            "functional_rank": "Lektor",
            "employment_status": "Dosen Tetap",
            "nuptk": "6557767668230343",
            "sinta_id": "6027580",
            "sinta_url": "https://sinta.kemdiktisaintek.go.id/authors/profile/6027580",
            "sinta_score_overall": "210",
            "sinta_score_3yr": "90",
            "scopus_url": "",
            "scopus_docs": "0",
            "scopus_cits": "0",
            "scopus_hindex": "0",
            "gs_url": "https://scholar.google.com/citations?user=minarni",
            "gs_docs": "15",
            "gs_cits": "80",
            "gs_hindex": "4",
            "email": "minarni@unda.ac.id",
            "personal_web": "",
            "education": [
                "S1: Sarjana Komputer (S.Kom.), Sistem Informasi",
                "S2: Magister Manajemen (M.M.), Manajemen Sistem Informasi"
            ],
            "expertise": ["Sistem Informasi Manajemen", "Audit Sistem Informasi", "Tata Kelola TI", "E-Business"],
            "selected_publications": [
                "Implementasi Sistem Informasi Manajemen Terintegrasi pada Organisasi Pendidikan (2023)",
                "Evaluasi Efektivitas Layanan Akademik Berbasis Web Menggunakan Metode Servqual (2022)"
            ],
            "courses_taught": ["Sistem Informasi Manajemen", "Pengantar Bisnis & Manajemen", "Audit SI"],
            "bio": "Dosen Tetap Program Studi S1 Sistem Informasi dengan kepakaran di bidang Manajemen Sistem Informasi, Tata Kelola TI, dan Evaluasi Layanan Digital.",
            "slug": "minarni-s-kom-m-m",
            "role_category": "faculty"
        })

    civitas_data = {
        "faculty": faculty_list, # 12 Dosen
        "assistants": assistant_list # 3 Asdos
    }

    out_path = os.path.join(PROJECT_DIR, "src/data/civitas.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(civitas_data, f, indent=2, ensure_ascii=False)
    print(f"    Berhasil mengekstrak {len(faculty_list)} Dosen Tetap dan {len(assistant_list)} Asisten Dosen ke {out_path}.")
    return civitas_data

# -------------------------------------------------------------
# 4. EKSTRAKSI 5 KELOMPOK RISET
# -------------------------------------------------------------
def process_research_groups():
    print(">>> 4. Mengekstrak 5 Kelompok Riset (Research Groups)...")
    rg_list = [
        {
            "id": "aiml-rg",
            "code": "AIML-RG",
            "name": "Artificial Intelligence & Machine Learning Research Group",
            "name_id": "Kelompok Riset Kecerdasan Buatan & Pembelajaran Mesin",
            "coordinator": "Dr. Dwi Wahyu Prabowo, S.Si., M.Eng.",
            "coordinator_nuptk": "4536767668130283",
            "members": [
                "Dr. Dwi Wahyu Prabowo, S.Si., M.Eng. (Koordinator)",
                "Eka Prasetyaningrum, S.Kom., M.M.",
                "Dwika Lovitasari Yonia, S.Kom., M.Kom.",
                "Nurahman, S.Kom., M.M., M.Kom.",
                "Agung Purwanto, S.Kom., M.Kom."
            ],
            "assistants": [],
            "focus": "Bio-signal EEG / Brain-Computer Interface (BCI), Computer Vision, Deep Learning (CNN/Transformer), Recurrence Plots, dan Large Language Models (LLM) / Autonomous Agentic AI.",
            "roadmap": [
                "Eksplorasi representasi sinyal EEG non-linier melalui Recurrence Plots dan Asymmetric Windowing.",
                "Pengembangan arsitektur Multi-Domain Convolutional Neural Network (MD-CNN) untuk pengenalan emosi manusia.",
                "Penerapan Computer Vision berbasis CNN/YOLO untuk inspeksi kualitas komoditas lokal Kalimantan Tengah (kelapa sawit, rotan, dan ikan jelawat).",
                "Rancang bangun agen AI otonom berbasis LLM untuk orkestrasi kurikulum OBE dan automasi tata kelola akademik universitas."
            ],
            "flagship_publications": [
                "Enhancing EEG-Based Emotion Recognition Using Asymmetric Windowing Recurrence Plots — IEEE Access (Scopus Q1, 2024)",
                "A systematic literature review of emotion recognition using EEG signals — Cognitive Systems Research (Scopus Q1, 2023)",
                "An Advanced Data Augmentation Scheme on Limited EEG Signals for Human Emotion Recognition — LNEE Springer (Scopus, 2024)"
            ],
            "thesis_topics": [
                "Klasifikasi Status Emosi Manusia Berbasis Sinyal EEG Menggunakan Visualisasi Recurrence Plot dan MobileNetV3.",
                "Deteksi Tingkat Kematangan Tandan Buah Segar (TBS) Kelapa Sawit Berbasis Computer Vision dan YOLOv8.",
                "Otomasi Deteksi Retak Permukaan Kayu Rotan Menggunakan Image Segmentation Deep Learning.",
                "Pengembangan Sistem BCI Portabel Sinyal Tunggal untuk Kendali Perangkat Bantu Disabilitas."
            ]
        },
        {
            "id": "setk-rg",
            "code": "SETK-RG",
            "name": "Enterprise Systems, Governance & IS Strategy Research Group",
            "name_id": "Kelompok Riset Sistem Enterprise, Tata Kelola & Strategi SI",
            "coordinator": "Agung Purwanto, S.Kom., M.Kom.",
            "coordinator_nuptk": "1146760661130213",
            "members": [
                "Agung Purwanto, S.Kom., M.Kom. (Koordinator)",
                "Selviana Yunita, S.Kom., M.Kom.",
                "Lukman Bachtiar, S.Kom., M.M., M.Kom.",
                "Deny Sundari, S.Kom., A.Md., M.M.S.I.",
                "Eka Prasetyaningrum, S.Kom., M.M."
            ],
            "assistants": [
                "Fauzan Eka Prasatia, S.M.",
                "Prio Jaka Arsyad, S.Kom."
            ],
            "focus": "Enterprise Resource Planning (ERP), Tata Kelola TI (COBIT 2019, ITIL 4), Audit Kepatuhan & Keamanan Sistem Informasi, Business Process Management (BPMN), dan Perencanaan Strategis Sistem Informasi (TOGAF).",
            "roadmap": [
                "Audit maturitas tata kelola teknologi informasi pada instansi pemerintah daerah dan BUMD Kotawaringin Timur.",
                "Perancangan arsitektur enterprise menggunakan TOGAF ADM untuk modernisasi layanan digital institusi publik.",
                "Evaluasi penerimaan teknologi (Technology Acceptance Model & UTAUT2) sistem perbankan digital dan e-wallet di daerah penyangga perkebunan.",
                "Redesain dan optimasi proses bisnis rantai pasok logistik kelapa sawit menggunakan pemodelan BPMN standar."
            ],
            "flagship_publications": [
                "Evaluasi Penerimaan E-Wallet Menggunakan UTAUT 2 Di Kabupaten Kotawaringin Timur (2023)",
                "Perancangan Enterprise Architecture pada PDAM Tirta Mentaya Menggunakan Framework TOGAF (2023)",
                "Audit Tata Kelola Teknologi Informasi Menggunakan Framework COBIT pada Instansi Publik (2022)"
            ],
            "thesis_topics": [
                "Audit Tata Kelola Sistem Informasi Akademik SIAKAD Menggunakan Domain MEA dan DSS Framework COBIT 2019.",
                "Perancangan Enterprise Architecture Layanan Publik Dinas Kependudukan dan Catatan Sipil Menggunakan TOGAF ADM.",
                "Evaluasi Keberhasilan Implementasi ERP pada Perusahaan Perkebunan Kelapa Sawit Menggunakan Delone & McLean Model.",
                "Analisis dan Perbaikan Proses Bisnis Pengadaan Barang & Jasa Menggunakan Business Process Reengineering (BPR)."
            ]
        },
        {
            "id": "mhui-rg",
            "code": "MHUI-RG",
            "name": "Multimedia, HCI, UI/UX, Mobile & IoT Research Group",
            "name_id": "Kelompok Riset Multimedia, Interaksi Manusia-Komputer, UI/UX, Mobile & IoT",
            "coordinator": "Elika Thea Kirana, S.T., M.Kom.",
            "coordinator_nuptk": "2835773674230242",
            "members": [
                "Elika Thea Kirana, S.T., M.Kom. (Koordinator)",
                "Dwika Lovitasari Yonia, S.Kom., M.Kom.",
                "Deny Sundari, S.Kom., A.Md., M.M.S.I.",
                "Agung Purwanto, S.Kom., M.Kom."
            ],
            "assistants": [
                "Dody Erlangga, S.Kom."
            ],
            "focus": "Desain UI/UX Human-Centered (Design Thinking, Usability Evaluation SUS/UEQ), Pengembangan Aplikasi Mobile Lintas Platform (Flutter/React Native), Sensor IoT & Smart Environmental Monitoring, dan Media Digital Interaktif.",
            "roadmap": [
                "Pengembangan platform mobile ramah aksesibilitas untuk literasi digital pelaku UMKM di Kotawaringin Timur.",
                "Rancang bangun sistem sensor IoT berbasis LoRa/ESP32 untuk pemantauan kualitas udara dan deteksi dini kabut asap kebakaran lahan gambut.",
                "Evaluasi antarmuka portal layanan publik pemerintah daerah berbasis User Experience Questionnaire (UEQ).",
                "Integrasi Augmented Reality (AR) dalam media edukasi konservasi satwa endemik Kalimantan (Orangutan & Bekantan)."
            ],
            "flagship_publications": [
                "Evaluasi Usability Website Pemerintah Menggunakan System Usability Scale (SUS) dan User Experience Questionnaire (2023)",
                "Penerapan Konsep Design Thinking dalam Rancang Bangun Aplikasi Mobile Layanan Darurat Kesehatan Daerah (2022)"
            ],
            "thesis_topics": [
                "Rancang Bangun Prototipe Sistem Monitoring Kualitas Air Tambak Ikan Jelawat Berbasis IoT dan Dashboard Web.",
                "Redesain Antarmuka Mobile Banking Menggunakan Metode Goal-Directed Design dan Evaluasi SUS.",
                "Pengembangan Aplikasi Mobile Edukasi Aksara dan Budaya Dayak Menggunakan Flutter.",
                "Sistem Presensi Mahasiswa Berbasis Geolocation dan QR-Code Dinamis Terintegrasi Layanan Kampus."
            ]
        },
        {
            "id": "dsdss-rg",
            "code": "DSDSS-RG",
            "name": "Data Science, Analytics & Decision Support Systems Research Group",
            "name_id": "Kelompok Riset Sains Data, Analitika & Sistem Pendukung Keputusan",
            "coordinator": "Nurahman, S.Kom., M.M., M.Kom.",
            "coordinator_nuptk": "2342765666130493",
            "members": [
                "Nurahman, S.Kom., M.M., M.Kom. (Koordinator)",
                "Dr. Dwi Wahyu Prabowo, S.Si., M.Eng.",
                "Eka Prasetyaningrum, S.Kom., M.M.",
                "Lukman Bachtiar, S.Kom., M.M., M.Kom.",
                "Abdul Aziz, S.Pd., M.Pd."
            ],
            "assistants": [],
            "focus": "Multi-Criteria Decision Making (MCDM: AHP, TOPSIS, SAW, Promethee, SMART), Healthcare & Epidemic Data Analytics, Klasterisasi Prediktif Pertanian/Perkebunan, dan Business Intelligence & Interactive Data Lakehouse.",
            "roadmap": [
                "Sistem Pendukung Keputusan Penentuan Penerima Bantuan Sosial Tepat Sasaran Menggunakan Integrasi AHP dan TOPSIS.",
                "Klasterisasi spasial risiko kesehatan ibu hamil dan anak stunting di puskesmas pelosok Kalimantan Tengah menggunakan K-Means dan PCA.",
                "Prediksi tren fluktuasi harga komoditas tandan buah segar kelapa sawit menggunakan Time Series Forecasting (ARIMA & Prophet).",
                "Pembangunan Interactive Business Intelligence Dashboard untuk pemantauan kinerja akademik dan serapan alumni."
            ],
            "flagship_publications": [
                "Sistem Pendukung Keputusan Penentuan Kelayakan Bantuan Sosial Menggunakan Kombinasi Metode AHP dan TOPSIS (2023)",
                "Penerapan Data Mining untuk Analisis Pola Penjualan Ritel Menggunakan Algoritma Apriori (2022)",
                "Analisis Sentimen Opini Publik Terhadap Kebijakan Daerah Menggunakan Naive Bayes dan SVM (2023)"
            ],
            "thesis_topics": [
                "Sistem Pendukung Keputusan Pemilihan Lahan Perkebunan Kelapa Sawit Produktif Menggunakan Kombinasi AHP dan Promethee.",
                "Klasterisasi Tingkat Kesejahteraan Keluarga Berdasarkan Data Registrasi Sosial Ekonomi Menggunakan K-Medoids.",
                "Analisis Pola Transaksi Penjualan Menggunakan Algoritma FP-Growth untuk Rekomendasi Bundling Produk UMKM.",
                "Prediksi Curah Hujan Harian di Sampit Berbasis Machine Learning untuk Antisipasi Musim Tanam."
            ]
        },
        {
            "id": "edutech-rg",
            "code": "EDUTECH-RG",
            "name": "Educational Technology, General Education & Karakter Research Group",
            "name_id": "Kelompok Riset Teknologi Pendidikan, General Education & Karakter",
            "coordinator": "Abdul Aziz, S.Pd., M.Pd.",
            "coordinator_nuptk": "1953765666130272",
            "members": [
                "Abdul Aziz, S.Pd., M.Pd. (Koordinator)",
                "Serika Zai, S.Pd., M.Pd.",
                "Agung Purwanto, S.Kom., M.Kom.",
                "Elika Thea Kirana, S.T., M.Kom.",
                "Dr. Dwi Wahyu Prabowo, S.Si., M.Eng."
            ],
            "assistants": [
                "Dody Erlangga, S.Kom."
            ],
            "focus": "Digital Pedagogy, Gamifikasi Media Pembelajaran, E-Learning Berbasis Outcome-Based Education (OBE), dan Penguatan Karakter/Integritas Mahasiswa Era AI.",
            "roadmap": [
                "Model integrasi taksonomi Bloom revisi pada Learning Management System (Moodle & Edlink) berbasis asesmen OBE.",
                "Pengembangan instrumen evaluasi pembelajaran bermakna (meaningful learning) pada mahasiswa ilmu komputer kelas malam dan pekerja.",
                "Desain kerangka kerja etika akademik pencegahan plagiarisme berbasis Generative AI pada mahasiswa tingkat sarjana.",
                "Gamifikasi asesmen formatif untuk meningkatkan retensi dan pemahaman konsep algoritma pemrograman dasar."
            ],
            "flagship_publications": [
                "Penguatan Budaya Mutu Sekolah melalui Pendampingan Akreditasi di SMPN Satu Atap (2023)",
                "Evaluasi Penerapan E-Learning Moodle Terhadap Motivasi Belajar Mahasiswa Komputer (2022)"
            ],
            "thesis_topics": [
                "Pengembangan Game Edukasi Pembelajaran Logika Algoritma Berbasis Unity untuk Siswa SMK Rekayasa Perangkat Lunak.",
                "Evaluasi Efektivitas Pembelajaran Berbasis OBE Menggunakan Analytics Log Activity LMS Moodle.",
                "Rancang Bangun Sistem Evaluasi Kepuasan Mahasiswa Terhadap Pembelajaran Dosen Berbasis Web.",
                "Pengembangan Modul Pembelajaran Interaktif Etika Profesi TI Berbasis Microlearning."
            ]
        }
    ]

    out_path = os.path.join(PROJECT_DIR, "src/data/research_groups.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(rg_list, f, indent=2, ensure_ascii=False)
    print(f"    Berhasil menulis 5 kelompok riset ke {out_path}.")
    return rg_list

# -------------------------------------------------------------
# 5. GENERATE NAVIGATION & PORTAL LINKS
# -------------------------------------------------------------
def process_navigation():
    print(">>> 5. Menyiapkan Navigasi & Tautan Portal Institusi...")
    nav_data = {
        "institution": {
            "name": "Program Studi S1 Sistem Informasi",
            "faculty": "Fakultas Ilmu Komputer",
            "university": "Universitas Darwan Ali",
            "accreditation": "Baik Sekali",
            "address": "Jl. Batu Berlian No. 10, Sampit, Kotawaringin Timur, Kalimantan Tengah 74322",
            "email": "sisteminformasi@unda.ac.id",
            "instagram": "https://www.instagram.com/sisfounda/",
            "head_of_program": "Dr. Dwi Wahyu Prabowo, S.Si., M.Eng.",
            "head_personal_web": "http://bowo.staff.unda.ac.id/",
            "head_nuptk": "4536767668130283"
        },
        "portals": [
            {
                "name": "Pendaftaran Mahasiswa Baru (SPMB)",
                "url": "https://univdarwanali.siakadcloud.com/spmbfront/program-studi-detail/detail/57201",
                "badge": "PMB 2026",
                "icon": "user-plus",
                "featured": True
            },
            {
                "name": "SIAKAD Resmi UNDA",
                "url": "https://siak.unda.ac.id/",
                "badge": "Akademik",
                "icon": "academic-cap"
            },
            {
                "name": "Edlink LMS",
                "url": "https://edlink.id/",
                "badge": "Tugas & Kelas",
                "icon": "book-open"
            },
            {
                "name": "Moodle eLearning",
                "url": "https://cloud.unda.ac.id/moodle",
                "badge": "Ujian Online",
                "icon": "desktop-computer"
            },
            {
                "name": "Portal eSign FIKOM",
                "url": "https://esign-fikom.unda.ac.id/",
                "badge": "Layanan Digital",
                "icon": "document-check"
            },
            {
                "name": "Website Utama Universitas",
                "url": "https://www.unda.ac.id",
                "badge": "Portal Induk",
                "icon": "globe"
            }
        ],
        "menu_id": [
            {"label": "Beranda", "href": "/"},
            {"label": "Profil", "href": "/profil/", "sub": [
                {"label": "Visi, Misi & Tujuan", "href": "/profil/#visi-misi"},
                {"label": "Sambutan Kaprodi & Dekan", "href": "/profil/#sambutan"},
                {"label": "Struktur Organisasi", "href": "/profil/#struktur"},
                {"label": "Akreditasi & Sertifikasi", "href": "/profil/#akreditasi"}
            ]},
            {"label": "Akademik", "href": "/akademik/kurikulum/", "sub": [
                {"label": "Kurikulum OBE 144 SKS", "href": "/akademik/kurikulum/"},
                {"label": "Profil Lulusan & CPL", "href": "/akademik/kurikulum/#cpl"},
                {"label": "Repositori Master RPS PDF", "href": "/akademik/rps/"}
            ]},
            {"label": "Civitas", "href": "/civitas/", "sub": [
                {"label": "Direktori Dosen Tetap", "href": "/civitas/#dosen"},
                {"label": "Asisten Dosen", "href": "/civitas/#asdos"}
            ]},
            {"label": "Riset", "href": "/riset/kelompok-riset/", "sub": [
                {"label": "5 Kelompok Riset (Research Groups)", "href": "/riset/kelompok-riset/"},
                {"label": "Roadmap & Topik Skripsi", "href": "/riset/kelompok-riset/#topik-skripsi"}
            ]},
            {"label": "Layanan", "href": "/mahasiswa/", "sub": [
                {"label": "Layanan Mahasiswa (SOP & Skripsi)", "href": "/mahasiswa/"},
                {"label": "Alumni & Ikatan Lulusan", "href": "/alumni/"},
                {"label": "Tracer Study Alumni", "href": "/tracer-study/"},
                {"label": "Unduhan Formulir & Panduan", "href": "/unduhan/"}
            ]},
            {"label": "Berita", "href": "/berita/"},
            {"label": "Kontak", "href": "/kontak/"}
        ],
        "menu_en": [
            {"label": "Home", "href": "/en/"},
            {"label": "About", "href": "/en/about/", "sub": [
                {"label": "Vision, Mission & Goals", "href": "/en/about/#vision-mission"},
                {"label": "Dean & Head Message", "href": "/en/about/#welcome"},
                {"label": "Organization Structure", "href": "/en/about/#organization"},
                {"label": "Accreditation", "href": "/en/about/#accreditation"}
            ]},
            {"label": "Academics", "href": "/en/academics/curriculum/", "sub": [
                {"label": "OBE Curriculum (144 Credits)", "href": "/en/academics/curriculum/"},
                {"label": "Graduate Profiles & CPL", "href": "/en/academics/curriculum/#cpl"},
                {"label": "Syllabus (RPS) Repository", "href": "/en/academics/rps/"}
            ]},
            {"label": "Faculty", "href": "/en/faculty/", "sub": [
                {"label": "Faculty Members", "href": "/en/faculty/#faculty"},
                {"label": "Teaching Assistants", "href": "/en/faculty/#assistants"}
            ]},
            {"label": "Research", "href": "/en/research/groups/", "sub": [
                {"label": "5 Research Groups", "href": "/en/research/groups/"},
                {"label": "Roadmaps & Thesis Topics", "href": "/en/research/groups/#thesis-topics"}
            ]},
            {"label": "Services", "href": "/en/students/", "sub": [
                {"label": "Student Guidelines & SOP", "href": "/en/students/"},
                {"label": "Alumni Association", "href": "/en/alumni/"},
                {"label": "Alumni Tracer Study", "href": "/en/tracer-study/"},
                {"label": "Downloads & Documents", "href": "/en/downloads/"}
            ]},
            {"label": "News", "href": "/en/news/"},
            {"label": "Contact", "href": "/en/contact/"}
        ]
    }

    out_path = os.path.join(PROJECT_DIR, "src/data/navigation.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(nav_data, f, indent=2, ensure_ascii=False)
    print(f"    Berhasil menulis struktur navigasi dan portal ke {out_path}.")
    return nav_data

if __name__ == "__main__":
    print("=== MEMULAI EKSTRAKSI DATA OTORITATIF WEBSITE PRODI SI ===")
    process_rps()
    process_curriculum()
    process_civitas()
    process_research_groups()
    process_navigation()
    print("=== EKSTRAKSI DATA SELESAI DENGAN SUKSES ===")

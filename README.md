# Rule-Based Expert System for Maternal Complication Risk Detection

Sebuah aplikasi Sistem Pakar yang dibangun untuk mendeteksi risiko komplikasi maternal pada ibu hamil. Sistem ini menggunakan metode inferensi **Forward Chaining** untuk mengevaluasi gejala dan kondisi klinis berdasarkan basis pengetahuan (rule-based) dari pakar obgyn.
Proyek ini merupakan implementasi *source code* dari penelitian skripsi program studi Sistem Informasi.

## 🌟 Fitur Utama
* **Inferensi Forward Chaining:** Mesin inferensi yang memproses data masukan pengguna (gejala/kondisi) untuk menghasilkan kesimpulan risiko secara runut.
* **Rule-Based System:** Basis pengetahuan yang dirancang sesuai dengan standar dan pedoman pakar kesehatan.
* **Diagnosis Real-time:** Memberikan hasil deteksi tingkat risiko secara langsung setelah pengguna memasukkan data observasi.
* **Manajemen Basis Data:** Menggunakan koneksi SQL untuk memfasilitasi penyimpanan riwayat konsultasi dan aturan pakar secara terstruktur.

## 💻 Teknologi yang Digunakan
* **Bahasa Pemrograman:** Python
* **Framework Antarmuka (Web):** Streamlit
* **Database:** MySQL
* **Manajemen Dependensi:** pip (`requirements.txt`)
* **Algoritma:** Forward Chaining Inference Engine

## ⚙️ Cara Instalasi (Instruksi Lokal)
Untuk menjalankan aplikasi sistem pakar ini di komputer lokal, ikuti langkah-langkah berikut:

### 1. Persiapan Database (MySQL)
* Pastikan Anda sudah menginstal aplikasi server lokal seperti **XAMPP**.
* Buka XAMPP Control Panel dan aktifkan modul **MySQL**.
* Buka antarmuka phpMyAdmin di **browser** (biasanya `http://localhost/phpmyadmin`).
* Buat **database** baru dengan nama `db_maternal`.
* Lakukan **Import** file `db_maternal.sql` ke dalam *database* yang baru dibuat tersebut.

### 2. Persiapan Aplikasi (Streamlit)
* Pastikan **Python** sudah terinstal di komputer Anda.
* **Clone** repositori ini ke komputer lokal:
```bash
  git clone (https://github.com/likesagitri7/sistem-pakar-forward-chaining.git)
```
### 3. Masuk ke dalam direktori proyek: 
```bash
cd nama-repository
```
### 4. (Opsional namun disarankan) Buat dan aktifkan Virtual Environment: 
```bash
python -m venv venv
```
* Untuk Windows: venv\Scripts\activate
* Untuk Mac/Linux: source venv/bin/activate
### 5. Instal semua pustaka (library) yang dibutuhkan melalui terminal: 
```bash
pip install -r requirements.txt
```
### 6. Jalankan aplikasi menggunakan Streamlit: 
```bash
streamlit run app.py
```

## ⚠️ Disclaimer
Aplikasi ini dikembangkan untuk tujuan penelitian akademis dan demonstrasi logika pemrograman. Hasil diagnosis dari sistem pakar ini tidak dapat menggantikan diagnosis medis profesional, konsultasi dokter, atau tenaga medis yang sah. Tidak ada data riwayat rekam medis pasien nyata yang disertakan dalam repositori ini demi menjaga privasi dan etika data.

## 👨‍💻 Penulis
Like Sagitri 
Fresh Graduate | Information Systems

Data Analytics | Data Science | Machine Learning
[LinkedIn](https://www.linkedin.com/in/like-sagitri-helen)

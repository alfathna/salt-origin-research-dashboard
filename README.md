# Salt Origin Research Dashboard

Dashboard penelitian interaktif berbasis **Streamlit** untuk mengeksplorasi data mineral garam dan mengevaluasi pengaruh transformasi **Box-Cox** terhadap kinerja **Gaussian Naive Bayes (GNB)** dalam klasifikasi asal geografis garam.

Aplikasi menyajikan **hasil eksperimen yang telah tersimpan**. Pengguna dapat memfilter dan membandingkan hasil, tetapi aplikasi tidak melatih ulang model atau memprediksi sampel baru.

## Ringkasan penelitian

- **Data:** 59 sampel garam dari Brazil (11), Spain (16), France (16), dan Portugal (16).
- **Fitur:** K, Na, Ca, Mg, Fe, Mn, Zn, dan Cu.
- **Sumber:** data mineral FAAS pada *Supplementary Table S2* dari Zanela Lima et al. (2025).
- **Konfigurasi:** M0 (data asli), M1 (konversi satuan dan standardisasi), serta M2 (konversi satuan, Box-Cox, dan standardisasi).
- **Evaluasi:** stratified hold-out 80:20, 70:30, 60:40; Stratified 5-Fold CV; dan Repeated Stratified 5-Fold CV (10 pengulangan).

Pada Repeated Stratified 5-Fold CV × 10, rata-rata **macro F1** yang diperoleh adalah **60,26% (M0)**, **68,22% (M1)**, dan **86,42% (M2)**. Angka ini merupakan hasil pada dataset penelitian, bukan jaminan performa pada sampel baru.

## Fitur dashboard

| Halaman | Fungsi |
|---|---|
| **Overview** | Ringkasan dataset, konfigurasi GNB, dan temuan utama. |
| **Eksplorasi Data** | Filter negara dan mineral, statistik deskriptif, histogram, boxplot, korelasi Spearman, dan tabel sampel. |
| **Analisis Box-Cox** | Perbandingan skewness dan distribusi sebelum–sesudah transformasi, termasuk diagnostik data latih untuk tiga rasio hold-out. |
| **Evaluasi Model** | Perbandingan M0–M2 pada hold-out dan cross-validation, termasuk variasi skor. |
| **Hasil Klasifikasi** | Confusion matrix, metrik per negara, prediksi historis data uji, dan perubahan prediksi antarmodel. |

## Panduan instalasi dan menjalankan aplikasi

### 1. Prasyarat sistem
- **Python**: versi 3.10 atau lebih baru (minimal Python 3.9).
- **pip**: manajer paket Python versi terbaru.

### 2. Langkah instalasi

1. **Clone atau unduh repositori:**
   ```bash
   git clone https://github.com/alfathna/salt-origin-research-dashboard.git
   cd salt-origin-research-dashboard
   ```

2. **Buat dan aktifkan virtual environment (disarankan):**
   - **Windows:**
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   - **macOS / Linux:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Pasang paket dependensi:**
   ```bash
   pip install -r requirements.txt
   ```
   *(Dependensi utama: `streamlit`, `pandas`, dan `plotly`)*

4. **Verifikasi kelengkapan berkas dan data (opsional):**
   ```bash
   python tests/check_installation.py
   python tests/smoke_headless.py
   ```

### 3. Menjalankan dashboard
Jalankan perintah berikut melalui terminal:
```bash
streamlit run app.py
```
Aplikasi akan otomatis terbuka pada peramban di alamat `http://localhost:8501`.

## Catatan metodologi

- **M0** menggunakan fitur pada satuan asli; **M1** dan **M2** mengonversi Na dari mg/g menjadi µg/g sebelum pengolahan fitur.
- Diagnostik Box-Cox menggunakan **data latih masing-masing rasio**, bukan seluruh dataset sekaligus.
- Visualisasi dan metrik dibaca dari file hasil eksperimen. **Tidak ada upload dataset, tuning hyperparameter, pelatihan ulang, atau prediksi bebas** dalam aplikasi.
- Confusion matrix dan tabel prediksi individual bersumber dari **evaluasi hold-out**, bukan dari prediksi sampel eksternal.
- Dataset yang terbatas pada 59 sampel dari empat negara tidak dapat digunakan untuk mengklaim autentikasi asal seluruh jenis garam. Skewness yang mendekati nol juga tidak otomatis membuktikan distribusi Gaussian pada setiap kelas.

## Sumber data dan referensi

Zanela Lima, L. R., et al. (2025). *Origin Identification of Table Salt Using Flame Atomic Absorption and Portable Near-Infrared Spectrometries.* **Chemosensors, 13**(7), 231. https://doi.org/10.3390/chemosensors13070231

Dataset yang digunakan dalam dashboard merupakan **data kandungan mineral FAAS** dari materi suplementer penelitian tersebut, **bukan** data spektrum NIR. Analisis GNB, transformasi Box-Cox, dan hasil evaluasi merupakan bagian dari penelitian yang ditampilkan melalui dashboard ini.

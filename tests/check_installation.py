"""Pemeriksaan cepat tanpa dependensi eksternal. Jalankan sebelum Streamlit."""
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parents[1]
REQUIRED = [
    "data/table_salt_origin.csv",
    "data/results/repeated_cv_summary.csv",
    "data/results/holdout_metrics_all_models.csv",
    "data/results/holdout_predictions.csv",
    "data/results/holdout_classification_reports.csv",
    "data/results/cv5_fold_metrics.csv",
    "data/results/cv5_summary.csv",
    "data/results/repeated_cv_50fold_metrics.csv",
    "data/results/paired_macro_f1_differences.csv",
    "data/results/audit_bab3/perubahan_prediksi_holdout.csv",
    "data/results/audit_bab3/diagnostik_lintas_rasio/skewness_boxcox_training_3rasio_rinci.csv",
    "data/results/audit_bab3/diagnostik_lintas_rasio/ringkasan_skewness_boxcox_training_3rasio.csv",
    "data/results/audit_bab3/diagnostik_lintas_rasio/profil_boxcox_training_3rasio.csv",
    "data/results/audit_bab3/diagnostik_lintas_rasio/skewness_per_negara_training_3rasio.csv",
]
missing = [x for x in REQUIRED if not (BASE / x).is_file()]
if missing:
    print("GAGAL: berkas data yang diperlukan belum lengkap:")
    for x in missing:
        print(" -", x)
    print("\nSolusi: ekstrak seluruh ZIP versi terbaru ke folder baru; jangan hanya menimpa file .py.")
    sys.exit(1)
# Pastikan CSV yang dibutuhkan betul-betul bisa dibaca, tidak sekadar ada.
try:
    import pandas as pd
    d = pd.read_csv(BASE / "data/table_salt_origin.csv", encoding="utf-8-sig")
    if len(d) != 59 or d["Country"].nunique() != 4:
        raise ValueError("Dataset tidak berisi 59 sampel / 4 kelas seperti pada penelitian.")
    profiles = pd.read_csv(BASE / "data/results/audit_bab3/diagnostik_lintas_rasio/profil_boxcox_training_3rasio.csv")
    per_country = pd.read_csv(BASE / "data/results/audit_bab3/diagnostik_lintas_rasio/skewness_per_negara_training_3rasio.csv")
    if len(profiles) != 984 or len(per_country) != 96:
        raise ValueError("Jumlah baris diagnostik Box-Cox tidak sesuai.")
    if set(profiles["Skenario"]) != {"80:20", "70:30", "60:40"}:
        raise ValueError("Rasio diagnostik Box-Cox tidak lengkap.")
except (ImportError, OSError, ValueError, KeyError) as e:
    print(f"GAGAL: isi CSV tidak terbaca atau tidak sesuai: {e}")
    sys.exit(1)
print(f"OK: {len(REQUIRED)} berkas utama ditemukan dan CSV diagnostik terbaca.")
print("Folder proyek:", BASE)

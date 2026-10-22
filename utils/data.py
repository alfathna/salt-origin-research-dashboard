"""Reader dan pengecekan ringan untuk berkas hasil eksperimen final.

Angka hasil evaluasi dalam CSV tersimpan pada skala 0–100 (%), bukan 0–1.
"""
from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
RESULTS_DIR = DATA_DIR / "results"
LABELS = ["Brazil", "Spain", "France", "Portugal"]
FEATURES = ["K_ug_g", "Na_mg_g", "Ca_ug_g", "Mg_ug_g", "Fe_ug_g", "Mn_ug_g", "Zn_ug_g", "Cu_ug_g"]
DISPLAY_MINERALS = {"K_ug_g": "K", "Na_mg_g": "Na", "Ca_ug_g": "Ca", "Mg_ug_g": "Mg", "Fe_ug_g": "Fe", "Mn_ug_g": "Mn", "Zn_ug_g": "Zn", "Cu_ug_g": "Cu"}


@st.cache_data(show_spinner=False)
def read_dataset():
    file = DATA_DIR / "table_salt_origin.csv"
    if not file.is_file():
        raise FileNotFoundError("data/table_salt_origin.csv tidak ditemukan. "
                                "Pastikan seluruh folder data ikut diekstrak dari ZIP.")
    df = pd.read_csv(file, encoding="utf-8-sig")
    expected = {"Sample", "Country", *FEATURES}
    if set(df.columns) != expected:
        raise ValueError(f"Kolom dataset tidak sesuai. Ditemukan: {list(df.columns)}")
    if len(df) != 59 or df["Country"].value_counts().to_dict() != {"Brazil": 11, "Spain": 16, "France": 16, "Portugal": 16}:
        raise ValueError("Jumlah sampel atau distribusi negara tidak sesuai dataset penelitian.")
    if df[FEATURES].isna().any().any():
        raise ValueError("Dataset memiliki nilai mineral kosong; periksa berkas sumber.")
    return df



@st.cache_data(show_spinner=False)
def read_result(relative_path: str):
    """Baca CSV dari folder hasil; berikan pesan yang jelas saat berkas belum tersalin."""
    root = RESULTS_DIR.resolve()
    rel = Path(relative_path)
    # Aplikasi hanya membuka CSV internal; tidak bergantung pada working directory.
    if rel.is_absolute() or rel.suffix.lower() != ".csv" or ".." in rel.parts:
        raise ValueError(f"Nama berkas hasil tidak valid: {relative_path}")
    path = (root / rel).resolve()
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"Berkas berada di luar data/results: {relative_path}") from exc
    if not path.is_file():
        raise FileNotFoundError(
            f"Berkas 'data/results/{rel.as_posix()}' tidak ditemukan. "
            "Ekstrak ZIP ini lengkap ke folder baru; jangan gabungkan dengan folder aplikasi lama."
        )
    return pd.read_csv(path, encoding="utf-8-sig")


def repeated_cv_summary():
    df = read_result("repeated_cv_summary.csv")
    required = {"Model", "Macro F1 (Mean)", "Macro F1 (Std)"}
    if not required.issubset(df.columns) or set(df["Model"]) != {"M0", "M1", "M2"} or len(df) != 3:
        raise ValueError("Ringkasan Repeated CV tidak sesuai dengan eksperimen final M0–M2.")
    metric = pd.to_numeric(df["Macro F1 (Mean)"], errors='raise')
    if metric.isna().any() or not metric.between(0, 100).all():
        raise ValueError("Rentang nilai macro F1 pada CSV tidak valid.")
    return df.set_index("Model").loc[["M0", "M1", "M2"]].reset_index()

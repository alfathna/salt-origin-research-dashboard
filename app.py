"""Salt Origin Research Dashboard — tahap A: lima halaman fungsional.

Jalankan: streamlit run app.py
"""
import streamlit as st
from views import overview, eksplorasi_data, boxcox, evaluasi, klasifikasi
from utils.styles import inject_style

st.set_page_config(
    page_title="Salt Origin Research Dashboard",
    page_icon="🧂",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_style()

MENU = {
    "Overview": overview.render,
    "Eksplorasi Data": eksplorasi_data.render,
    "Analisis Box-Cox": boxcox.render,
    "Evaluasi Model": evaluasi.render,
    "Hasil Klasifikasi": klasifikasi.render,
}

with st.sidebar:
    selected = st.radio("Navigasi dashboard", list(MENU), label_visibility="collapsed", key="navigation")

try:
    MENU[selected]()
except FileNotFoundError as exc:
    st.error("File data yang diperlukan belum ditemukan.")
    st.info(str(exc))
    st.caption("Jangan menyalin app.py/views saja ke proyek lama. Salin juga seluruh folder data dari paket ZIP terbaru.")
except (ValueError, KeyError) as exc:
    st.error("Format data hasil tidak sesuai dengan yang dibutuhkan dashboard.")
    with st.expander("Detail error"):
        st.code(f"{type(exc).__name__}: {exc}")

st.markdown('<div class="salt-footer">Salt Origin Research Dashboard · Data sekunder FAAS · Zanela Lima et al. (2025)</div>',unsafe_allow_html=True)

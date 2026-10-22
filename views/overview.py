"""Halaman 01 — data asli + angka ringkasan eksperimen final, tanpa model.fit()."""
import plotly.graph_objects as go
import streamlit as st
from utils.data import LABELS, read_dataset, repeated_cv_summary

MODEL_LABELS = {
    "M0": "M0 — Data asli",
    "M1": "M1 — Standardisasi",
    "M2": "M2 — Box-Cox + standardisasi",
}
MODEL_COLORS = {"M0": "#91a3b2", "M1": "#448a9b", "M2": "#0f877b"}


def _format_percentage(v: float) -> str:
    return f"{v:.2f}".replace('.', ',') + "%"


def render():
    df = read_dataset()
    summary = repeated_cv_summary()
    metrics = summary.set_index("Model")["Macro F1 (Mean)"]
    delta = float(metrics.loc["M2"] - metrics.loc["M1"])

    st.markdown('<div class="salt-eyebrow">Overview / Ringkasan Penelitian</div>', unsafe_allow_html=True)
    st.title("Klasifikasi Asal Geografis Garam")
    st.markdown("""<p class="salt-lead">Eksplorasi penelitian tentang pengaruh transformasi Box-Cox terhadap performa <b>Gaussian Naive Bayes (GNB)</b> dalam mengklasifikasikan negara asal garam berdasarkan delapan kandungan mineral hasil pengukuran FAAS.</p>""", unsafe_allow_html=True)

    a,b,c,d=st.columns(4)
    a.metric("Sampel garam",len(df))
    b.metric("Negara asal",df["Country"].nunique())
    c.metric("Fitur mineral",8)
    d.metric("Konfigurasi GNB",len(summary))

    st.write("")
    st.subheader("Hasil utama evaluasi model")
    st.caption("Rata-rata macro F1 pada Repeated Stratified 5-Fold Cross-Validation × 10 (50 evaluasi untuk setiap konfigurasi).")
    cards=st.columns(3)
    for c,model in zip(cards,["M0","M1","M2"]):
        with c:
            st.metric(MODEL_LABELS[model],_format_percentage(metrics.loc[model]))

    fig=go.Figure()
    for _,row in summary.iterrows():
        model=row["Model"]
        fig.add_trace(go.Bar(
            x=[MODEL_LABELS[model]],y=[row["Macro F1 (Mean)"]],
            marker_color=MODEL_COLORS[model],name=model,
            text=[_format_percentage(row["Macro F1 (Mean)"])],textposition="outside",
            customdata=[[row["Macro F1 (Std)"]]],
            hovertemplate=f"{model}: %{{y:.2f}}%<br>Standar deviasi: %{{customdata[0]:.2f}} poin<extra></extra>"
        ))
    fig.update_layout(
        showlegend=False, height=360, margin=dict(l=10,r=10,t=26,b=10),
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(title="Macro F1 (%)",range=[0,105],gridcolor="#F1F5F9",zeroline=False,linecolor="#E2E8F0"),
        xaxis=dict(title=None,tickfont=dict(size=12,color="#334155")),
        font=dict(family="'Plus Jakarta Sans', Inter, Arial, sans-serif",color="#334155"),
        hoverlabel=dict(bgcolor="#FFFFFF",bordercolor="#CBD5E1",font_family="'Plus Jakarta Sans', Inter, Arial, sans-serif",font_color="#0F172A")
    )
    st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
    st.markdown(f"""<div class="salt-note"><b>Temuan utama:</b> M2 mencapai rata-rata macro F1 <b>{_format_percentage(metrics.loc["M2"])}</b>, lebih tinggi <b>{str(f'{delta:.2f}').replace('.', ',')} poin persentase</b> dibanding M1. Ini adalah hasil pada dataset penelitian, bukan jaminan performa pada sampel garam baru.</div>""",unsafe_allow_html=True)

    left,right=st.columns([1,1],gap="large")
    with left:
        st.subheader("Komposisi sampel")
        counts=df["Country"].value_counts().reindex(LABELS)
        f=go.Figure(go.Bar(
            x=counts.values,y=counts.index,orientation='h',
            text=counts.values,textposition="auto",marker_color=["#248f83","#78b8b1","#5089a6","#b8cad2"],
            hovertemplate="%{y}: %{x} sampel<extra></extra>"
        ))
        f.update_layout(height=286,margin=dict(l=2,r=12,t=4,b=4),
            plot_bgcolor="rgba(0,0,0,0)",paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(title="Jumlah sampel",range=[0,18],gridcolor="#F1F5F9",linecolor="#E2E8F0"),
            yaxis=dict(title=None,autorange="reversed",tickfont=dict(size=12,color="#334155")),showlegend=False,
            font=dict(family="'Plus Jakarta Sans', Inter, Arial, sans-serif",color="#334155"),
            hoverlabel=dict(bgcolor="#FFFFFF",bordercolor="#CBD5E1",font_family="'Plus Jakarta Sans', Inter, Arial, sans-serif",font_color="#0F172A"))
        st.plotly_chart(f,use_container_width=True,config={"displayModeBar":False})
    with right:
        st.subheader("Tiga konfigurasi penelitian")
        st.markdown("""**M0 — Baseline:** delapan fitur mineral dalam satuan asli → GaussianNB.

**M1 — Standardisasi:** konversi Na dari mg/g ke µg/g → StandardScaler → GaussianNB.

**M2 — Transformasi Box-Cox:** konversi Na → Box-Cox dan standardisasi melalui PowerTransformer → GaussianNB.

Seluruh konfigurasi menggunakan `var_smoothing=1e-9` tanpa tuning hyperparameter.""")

    with st.expander("Metodologi dan sumber data",expanded=False):
        st.markdown("""**Dataset:** 59 sampel garam dari Brazil (11), Spain (16), France (16), dan Portugal (16), dengan 8 fitur: K, Na, Ca, Mg, Fe, Mn, Zn, Cu. Kolom `Sample` hanya sebagai identitas dan `Country` sebagai target.

**Sumber:** Zanela Lima *et al.* (2025), *Origin Identification of Table Salt Using Flame Atomic Absorption and Portable Near-Infrared Spectrometries*, *Chemosensors*, 13(7), 231. Dataset aplikasi berasal dari pengukuran **FAAS** pada tabel S2 supplementary material; aplikasi ini tidak menggunakan spektrum NIR. [DOI artikel sumber](https://doi.org/10.3390/chemosensors13070231).

**Rancangan evaluasi:** tiga stratified hold-out (80:20, 70:30, 60:40), Stratified 5-Fold CV, dan Repeated Stratified 5-Fold CV × 10; `random_state=42`. Halaman ini menampilkan hasil Repeated CV sebagai ringkasan utama.

**Batasan:** ukuran dataset kecil; model hanya membedakan empat negara yang tersedia. Evaluasi pada sampel baru di luar dataset sumber belum dilakukan.""")

    st.caption("Angka dan grafik Overview dibaca dari data/table_salt_origin.csv dan data/results/repeated_cv_summary.csv. Data tidak dilatih ulang dalam aplikasi.")

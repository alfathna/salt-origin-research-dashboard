"""Halaman 02 — eksplorasi data FAAS asli, tanpa perubahan data penelitian."""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from utils.data import read_dataset, LABELS, FEATURES, DISPLAY_MINERALS
from utils.visuals import COUNTRY_COLORS, fig_style, chart, download_csv, intro, fmt_num


def render():
    df = read_dataset()
    intro(st, "02 / Eksplorasi Data", "Karakteristik Mineral Garam",
          "Eksplorasi 59 sampel FAAS dari empat negara. Filter hanya mengubah tampilan dan statistik deskriptif, bukan data atau model penelitian.")

    left, right = st.columns([1.5, 1])
    with left:
        countries = st.multiselect("Negara asal", LABELS, default=LABELS, key="eda_countries")
    with right:
        mineral = st.selectbox("Mineral yang dianalisis", FEATURES, format_func=lambda x: DISPLAY_MINERALS[x], key="eda_mineral")
    if not countries:
        st.warning("Pilih setidaknya satu negara untuk menampilkan eksplorasi.")
        return
    subset = df[df["Country"].isin(countries)].copy()
    unit = "mg/g" if mineral == "Na_mg_g" else "µg/g"

    a, b, c = st.columns(3)
    a.metric("Sampel ditampilkan", len(subset))
    b.metric("Median", f"{fmt_num(subset[mineral].median())} {unit}")
    c.metric("Maksimum", f"{fmt_num(subset[mineral].max())} {unit}")

    st.subheader("Distribusi negara dan kandungan mineral")
    a, b = st.columns([0.95, 1.5], gap="large")
    with a:
        counts = subset["Country"].value_counts().reindex(countries)
        fig = go.Figure(go.Bar(
            x=counts.values, y=counts.index, orientation="h",
            marker_color=[COUNTRY_COLORS[c] for c in counts.index],
            text=counts.values, textposition="auto",
            hovertemplate="%{y}: %{x} sampel<extra></extra>",
        ))
        fig_style(fig, height=345, legend=False)
        fig.update_layout(xaxis_title="Jumlah sampel", yaxis_title=None)
        fig.update_yaxes(autorange="reversed")
        chart(st, fig)
    with b:
        hist = px.histogram(subset, x=mineral, color="Country", color_discrete_map=COUNTRY_COLORS,
                            category_orders={"Country": LABELS}, opacity=0.7, nbins=18, barmode="overlay")
        fig_style(hist, height=345)
        hist.update_layout(xaxis_title=f"{DISPLAY_MINERALS[mineral]} ({unit})", yaxis_title="Jumlah sampel")
        chart(st, hist)
    st.caption("Histogram menampilkan jumlah sampel pada interval nilai mineral; bin mengikuti rentang data yang sedang difilter.")

    a, b = st.columns([1.2, 1], gap="large")
    with a:
        st.markdown("#### Boxplot per negara")
        fig = px.box(subset, x="Country", y=mineral, color="Country",
                     category_orders={"Country": LABELS}, color_discrete_map=COUNTRY_COLORS,
                     points="all", hover_data=["Sample"])
        fig_style(fig, height=365, legend=False)
        fig.update_layout(xaxis_title=None, yaxis_title=f"{DISPLAY_MINERALS[mineral]} ({unit})")
        chart(st, fig)
    with b:
        st.markdown("#### Statistik deskriptif terfilter")
        desc = subset.groupby("Country", sort=False)[mineral].agg(["count", "mean", "median", "std", "min", "max"]).reset_index()
        desc.columns = ["Negara", "N", "Rata-rata", "Median", "Std", "Minimum", "Maksimum"]
        st.dataframe(desc.round(3), use_container_width=True, hide_index=True)
        st.caption("Standar deviasi sampel (ddof=1). Semua ringkasan mengikuti filter negara.")
        download_csv(st, desc, "statistik_eda_terfilter.csv", "eda_desc_csv")

    st.subheader("Hubungan antarfitur mineral")
    corr = subset[FEATURES].corr(method="spearman")
    labels = [DISPLAY_MINERALS[x] for x in FEATURES]
    heat = go.Figure(go.Heatmap(
        z=corr.values, x=labels, y=labels, zmin=-1, zmax=1, zmid=0,
        colorscale=[[0,"#47779D"],[0.5,"#F7FAFA"],[1,"#0B9484"]],
        text=corr.round(2).values, texttemplate="%{text:.2f}", textfont=dict(size=11),
        colorbar=dict(title="ρ"), hovertemplate="%{y} – %{x}<br>Spearman ρ = %{z:.3f}<extra></extra>"
    ))
    fig_style(heat, height=450, legend=False)
    heat.update_yaxes(autorange="reversed", scaleanchor="x")
    chart(st, heat)
    st.caption("Korelasi Spearman dihitung secara deskriptif pada baris yang dipilih. Korelasi global tidak membuktikan pelanggaran independensi kondisional GNB.")

    with st.expander("Skewness dan karakteristik nilai ekstrem", expanded=False):
        skew = subset[FEATURES].skew().rename_axis("Fitur").reset_index(name="Skewness")
        skew["Mineral"] = skew["Fitur"].map(DISPLAY_MINERALS)
        st.dataframe(skew[["Mineral", "Skewness"]], use_container_width=True, hide_index=True)
        if "SF11" in set(subset["Sample"]):
            k = float(subset.loc[subset["Sample"] == "SF11", "K_ug_g"].iloc[0])
            st.info(f"Sampel SF11 memiliki nilai K sebesar {fmt_num(k)} µg/g. Nilai ekstrem ini tercatat dalam sumber penelitian dan tidak dihapus.")
        st.caption("Skewness yang ditampilkan di sini dihitung dari data asli yang sedang difilter, bukan hasil transformasi Box-Cox pada data latih.")

    st.subheader("Tabel dataset")
    search = st.text_input("Cari kode sampel (opsional)", placeholder="Contoh: SF11", key="eda_search").strip()
    rows = subset[subset["Sample"].str.contains(search, case=False, regex=False)] if search else subset
    st.dataframe(rows, use_container_width=True, hide_index=True)
    download_csv(st, rows, "dataset_garam_terfilter.csv", "eda_data_csv")

    st.caption("Sumber: table_salt_origin.csv (FAAS, supplementary Table S2 Zanela Lima et al., 2025). Na dalam mg/g; tujuh mineral lain dalam µg/g.")

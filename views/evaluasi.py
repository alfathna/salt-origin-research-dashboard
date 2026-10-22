"""Halaman 04 — hasil hold-out/CV dari CSV final, tanpa training ulang."""
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from utils.data import read_result
from utils.visuals import (MODEL_ORDER, MODEL_NAMES, MODEL_COLORS, METRICS, SCHEMES,
                           fig_style, chart, download_csv, fmt_pct, fmt_num, intro)

SCHEMES_UI = ["Repeated 5-Fold × 10", "Stratified 5-Fold", "Hold-out 80:20", "Hold-out 70:30", "Hold-out 60:40"]


def _scheme_tables(choice):
    if choice.startswith("Hold-out"):
        split = choice.split(" ")[-1]
        return (read_result("holdout_metrics_all_models.csv").query("Skenario == @split"), None, "holdout")
    if choice == "Stratified 5-Fold":
        return read_result("cv5_summary.csv"), read_result("cv5_fold_metrics.csv"), "cv"
    return read_result("repeated_cv_summary.csv"), read_result("repeated_cv_50fold_metrics.csv"), "repeated"


def render():
    intro(st, "04 / Evaluasi Model", "Perbandingan Kinerja Gaussian Naive Bayes",
          "Bandingkan M0, M1, dan M2 pada satu skema evaluasi yang sama. Semua skor dibaca dari hasil final; tidak ada pelatihan ulang ataupun perubahan konfigurasi model.")
    a, b = st.columns([1.25, 1])
    with a:
        choice = st.selectbox("Skema evaluasi", SCHEMES_UI, key="ev_scheme")
    with b:
        metric = st.selectbox("Metrik evaluasi", METRICS, key="ev_metric")

    data, folds, kind = _scheme_tables(choice)
    data = data.set_index("Model").loc[MODEL_ORDER].reset_index()
    value_col = metric if kind == "holdout" else metric + " (Mean)"
    std_col = None if kind == "holdout" else metric + " (Std)"
    if value_col not in data.columns:
        st.error("Metrik tidak ditemukan pada ringkasan eksperimen.")
        return
    a, b, c = st.columns(3)
    for col, m in zip((a, b, c), MODEL_ORDER):
        r = data.set_index("Model").loc[m]
        with col:
            st.metric(MODEL_NAMES[m], fmt_pct(r[value_col]))
            if std_col:
                st.caption(f"Standar deviasi: {fmt_num(r[std_col])} poin persentase")

    v = data.set_index("Model")[value_col]
    delta = float(v["M2"] - v["M1"])
    st.info(f"Pada skema **{choice}**, nilai {metric} M2 − M1 = **{fmt_num(delta)} poin persentase**. "
            "Ini adalah selisih pada skema yang sama, bukan estimasi kausal bahwa semua peningkatan hanya disebabkan oleh satu faktor.")
    st.subheader("Grafik perbandingan model")
    fig = go.Figure()
    for _, r in data.iterrows():
        model = r["Model"]
        fig.add_trace(go.Bar(
            x=[model], y=[r[value_col]], name=MODEL_NAMES[model], marker_color=MODEL_COLORS[model],
            text=[fmt_pct(r[value_col])], textposition="outside",
            hovertemplate="%{x}: %{y:.2f}%<extra></extra>"
        ))
    fig_style(fig, height=360, legend=False)
    fig.update_layout(yaxis_title=metric + " (%)", xaxis_title="Konfigurasi", yaxis_range=[0, 108])
    chart(st, fig)
    st.caption("Pada hold-out, grafik menunjukkan satu hasil pada data uji. Pada CV, grafik menunjukkan rata-rata antar-fold (bukan skor satu hold-out).")

    st.subheader("Ringkasan hasil")
    main_metrics = ["Accuracy", "Macro F1", "Weighted F1"]
    if kind == "holdout":
        detail = data[["Model", "Jumlah Latih", "Jumlah Uji"] + main_metrics].copy()
    else:
        detail = data[["Model"] + [f"{m} (Mean)" for m in main_metrics]].copy()
    st.dataframe(detail.round(2), use_container_width=True, hide_index=True)
    with st.expander("Rincian semua metrik dan unduh CSV"):
        if kind == "holdout":
            full = data[["Model", "Jumlah Latih", "Jumlah Uji"] + METRICS].copy()
        else:
            full = data[["Model"] + [c for m in METRICS for c in (m + " (Mean)", m + " (Std)") if c in data.columns]].copy()
        st.dataframe(full.round(2), use_container_width=True, hide_index=True)
        download_csv(st, full, "evaluasi_" + choice.lower().replace(" ", "_").replace(":", "_").replace("×", "x") + ".csv", "ev_summary_csv")

    if folds is not None:
        st.subheader("Variasi skor antarfold")
        plot = go.Figure()
        for m in MODEL_ORDER:
            rows = folds[folds["Model"] == m]
            plot.add_trace(go.Box(y=rows[metric], name=m, marker_color=MODEL_COLORS[m],
                                  boxpoints="all", jitter=0.27, pointpos=0,
                                  hovertemplate=f"{m}<br>{metric}: %{{y:.2f}}%<extra></extra>"))
        fig_style(plot, height=380)
        plot.update_layout(yaxis_title=metric + " (%)", xaxis_title=None, showlegend=False,
                           yaxis_range=[0, 105])
        chart(st, plot)
        st.caption("Lima fold untuk Stratified 5-Fold; 50 fold untuk Repeated 5-Fold × 10. "
                   "Fold berulang berasal dari dataset yang sama, sehingga 50 skor bukan 50 pengujian eksternal independen.")
        with st.expander("Lihat hasil setiap fold"):
            rows = folds.sort_values(["Pengulangan", "Fold", "Model"])
            st.dataframe(rows, use_container_width=True, hide_index=True)
            download_csv(st, rows, "hasil_per_fold.csv", "ev_folds_csv")
        if kind == "repeated":
            with st.expander("Analisis selisih macro F1 antar-model (50 fold)"):
                _paired_analysis()
    with st.expander("Cara membaca dan batas evaluasi"):
        st.markdown("""**Metrik utama adalah macro F1**, yaitu rerata F1 dari empat negara tanpa pembobotan jumlah sampel. Metrik pendukung: accuracy, precision, recall, dan weighted F1.

**M0** memakai mineral asli; **M1** konversi Na dan standardisasi; **M2** konversi Na, Box-Cox, dan standardisasi. Seluruhnya menggunakan GNB dengan `var_smoothing=1e-9` tanpa tuning.

**M0 ke M1** tidak boleh dibaca sebagai pengaruh standardisasi murni karena perbedaan skala dapat memengaruhi `epsilon_` pada implementasi GaussianNB. **M1 ke M2** lebih tepat untuk mengamati tambahan pengaruh transformasi Box-Cox di atas pengendalian skala.

Evaluasi didasarkan pada 59 sampel dari empat negara dan belum merupakan pengujian independen pada sampel baru. Hasil ini tidak membuktikan keunggulan universal suatu metode.""")

def _paired_analysis():
    pairs = read_result("paired_macro_f1_differences.csv")
    diff = go.Figure()
    for col, color in [("M1 - M0", MODEL_COLORS["M1"]), ("M2 - M1", MODEL_COLORS["M2"]), ("M2 - M0", "#A08BC4")]:
        diff.add_trace(go.Box(y=pairs[col], name=col, boxpoints="outliers", marker_color=color))
    fig_style(diff, height=340)
    diff.update_layout(yaxis_title="Selisih macro F1 (poin persentase)", xaxis_title=None,
                       showlegend=False)
    diff.add_hline(y=0, line_dash="dash", line_color="#748493")
    chart(st, diff)
    st.caption("Selisih dihitung berpasangan pada fold yang sama. Standar deviasi fold bukan confidence interval dan grafik ini bukan uji signifikansi statistik.")
    with st.expander("Lihat tabel 50 pasangan fold"):
        st.dataframe(pairs, use_container_width=True, hide_index=True)
        download_csv(st, pairs, "paired_macro_f1_differences.csv", "ev_paired_csv")


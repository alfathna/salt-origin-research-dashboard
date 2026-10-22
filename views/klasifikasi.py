"""Halaman 05 — confusion matrix dan audit prediksi pada data uji hold-out."""
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from utils.data import read_result, read_dataset, LABELS, FEATURES, DISPLAY_MINERALS
from utils.visuals import (MODEL_ORDER, MODEL_NAMES, MODEL_COLORS, SCHEMES,
                           fig_style, chart, download_csv, fmt_pct, intro)


def matrix_from_predictions(rows):
    """Baris = kelas aktual; kolom = hasil prediksi; urutan label tetap."""
    return pd.crosstab(pd.Categorical(rows["Country"], categories=LABELS),
                       pd.Categorical(rows["Prediksi"], categories=LABELS),
                       dropna=False).reindex(index=LABELS, columns=LABELS, fill_value=0)


def render():
    intro(st, "05 / Hasil Klasifikasi", "Analisis Prediksi Benar dan Salah",
          "Pelajari kesalahan klasifikasi dari prediksi yang tersimpan pada data uji hold-out. "
          "Confusion matrix tidak dihitung dari skor agregat dan tidak dibuat untuk CV karena prediksi individual CV tidak disimpan.")
    a, b = st.columns(2)
    with a:
        scheme = st.selectbox("Rasio latih:uji", SCHEMES, index=1, key="cl_scheme")
    with b:
        model = st.selectbox("Konfigurasi GNB", MODEL_ORDER, index=2, format_func=lambda x: MODEL_NAMES[x], key="cl_model")
    all_preds = read_result("holdout_predictions.csv")
    rows = all_preds[(all_preds["Skenario"] == scheme) & (all_preds["Model"] == model)].copy()
    rows["Status"] = np.where(rows["Country"] == rows["Prediksi"], "Benar", "Salah")
    cm = matrix_from_predictions(rows)
    n = len(rows)
    correct = int((rows["Status"] == "Benar").sum())
    errors = n - correct
    metrics = read_result("holdout_metrics_all_models.csv")
    expected = metrics[(metrics["Skenario"] == scheme) & (metrics["Model"] == model)].iloc[0]
    if n != int(expected["Jumlah Uji"]) or not np.isclose(100 * correct / n, float(expected["Accuracy"]), atol=1e-8):
        st.error("Hasil confusion matrix tidak cocok dengan ringkasan hold-out. Periksa sumber data.")
        st.stop()

    a, b, c, d = st.columns(4)
    a.metric("Jumlah data uji", n)
    b.metric("Prediksi benar", correct)
    c.metric("Prediksi salah", errors)
    d.metric("Accuracy", fmt_pct(expected["Accuracy"]))

    a, b = st.columns([1.1, 1], gap="large")
    with a:
        st.subheader("Confusion matrix")
        fig = go.Figure(go.Heatmap(
            z=cm.values, x=LABELS, y=LABELS, zmin=0,
            colorscale=[[0, "#F1F8F7"], [1, "#0D8079"]],
            showscale=True, colorbar=dict(title="Sampel"),
            text=cm.values, texttemplate="%{text}", textfont=dict(size=15),
            hovertemplate="Aktual: %{y}<br>Prediksi: %{x}<br>Jumlah: %{z}<extra></extra>"
        ))
        fig_style(fig, height=420, legend=False)
        fig.update_layout(xaxis_title="Negara prediksi", yaxis_title="Negara aktual")
        fig.update_yaxes(autorange="reversed")
        chart(st, fig)
        st.caption("Diagonal: prediksi benar. Di luar diagonal: salah klasifikasi. Label selalu Brazil, Spain, France, Portugal.")
    with b:
        st.subheader("Classification report per negara")
        reports = read_result("holdout_classification_reports.csv")
        per_class = reports[(reports["Skenario"] == scheme) & (reports["Model"] == model) &
                            (reports["Kelas"].isin(LABELS))].copy()
        per_class = per_class.set_index("Kelas").reindex(LABELS).reset_index()
        st.caption("Precision, recall, F1 dalam skala 0–1; support adalah jumlah sampel aktual per negara.")
        st.dataframe(per_class, use_container_width=True, hide_index=True,
                     column_config={"Precision": st.column_config.NumberColumn(format="%.3f"),
                                    "Recall": st.column_config.NumberColumn(format="%.3f"),
                                    "F1": st.column_config.NumberColumn(format="%.3f")})
        download_csv(st, per_class, f"classification_report_{scheme.replace(':','_')}_{model}.csv", "cl_report_csv")
        st.markdown("#### Pola kesalahan")
        wrong = rows[rows["Status"] == "Salah"]
        if wrong.empty:
            st.success("Tidak ada prediksi salah pada skenario/model yang dipilih.")
        else:
            patterns = wrong.groupby(["Country", "Prediksi"]).size().reset_index(name="Jumlah")
            patterns.columns = ["Aktual", "Diprediksi sebagai", "Jumlah"]
            st.dataframe(patterns.sort_values("Jumlah", ascending=False), use_container_width=True, hide_index=True)

    st.subheader("Eksplorasi prediksi per sampel")
    a, b = st.columns(2)
    with a:
        status = st.selectbox("Status hasil", ["Semua", "Benar", "Salah"], key="cl_status")
    with b:
        selected_country = st.selectbox("Negara aktual", ["Semua"] + LABELS, key="cl_country")
    filtered = rows.copy()
    if status != "Semua":
        filtered = filtered[filtered["Status"] == status]
    if selected_country != "Semua":
        filtered = filtered[filtered["Country"] == selected_country]
    st.dataframe(filtered[["Sample", "Country", "Prediksi", "Status"]], use_container_width=True, hide_index=True)
    download_csv(st, filtered, f"prediksi_{model}_{scheme.replace(':','_')}.csv", "cl_pred_csv")

    with st.expander("Lihat kandungan mineral pada satu sampel data uji", expanded=False):
        sample = st.selectbox("Kode sampel dalam data uji", sorted(rows["Sample"].tolist()), key="cl_sample")
        record = read_dataset().set_index("Sample").loc[sample]
        pred = rows.set_index("Sample").loc[sample]
        st.write(f"**{sample}** · Negara aktual: **{pred['Country']}** · Prediksi {model}: **{pred['Prediksi']}** · Status: **{pred['Status']}**")
        rec = pd.DataFrame({"Mineral": [DISPLAY_MINERALS[x] for x in FEATURES],
                            "Nilai sumber": [record[x] for x in FEATURES],
                            "Satuan": ["mg/g" if x == "Na_mg_g" else "µg/g" for x in FEATURES]})
        st.dataframe(rec, use_container_width=True, hide_index=True)
        st.caption("Nilai mineral merupakan data asli sebelum preprocessing. Hasil prediksi di atas adalah hasil uji historis yang tersimpan.")

    st.subheader("Perubahan prediksi antar-konfigurasi")
    changes = read_result("audit_bab3/perubahan_prediksi_holdout.csv")
    changes = changes[changes["Skenario"] == scheme].copy()
    comparison = st.selectbox("Bandingkan prediksi", ["M1→M2", "M0→M1", "M0→M2"], key="cl_pair")
    counts = changes[f"Perubahan {comparison}"].value_counts()
    categories = ["Salah→Benar", "Benar→Salah", "Benar→Benar", "Salah→Salah"]
    count_df = pd.DataFrame({"Kategori": categories, "Jumlah": [int(counts.get(x, 0)) for x in categories]})
    l, r = st.columns([1, 1.4], gap="large")
    with l:
        plot = go.Figure(go.Bar(x=count_df["Kategori"], y=count_df["Jumlah"],
                                marker_color=["#0B9484", "#C87070", "#5D91AB", "#AAB6C3"],
                                text=count_df["Jumlah"], textposition="outside"))
        fig_style(plot, height=345, legend=False)
        plot.update_layout(xaxis_title=None, yaxis_title="Jumlah sampel")
        plot.update_xaxes(tickangle=-24)
        chart(st, plot)
    with r:
        st.dataframe(changes[["Sample", "Country", "Prediksi " + comparison[:2],
                                    "Prediksi " + comparison[-2:], "Perubahan " + comparison]],
                     use_container_width=True, hide_index=True)
        download_csv(st, changes, f"perubahan_prediksi_{scheme.replace(':','_')}.csv", "cl_change_csv")
    st.caption("Perubahan dibandingkan pada sampel uji yang sama untuk rasio terpilih. M2 tidak selalu mengubah seluruh kesalahan menjadi benar.")

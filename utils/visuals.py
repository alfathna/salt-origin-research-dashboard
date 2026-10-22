"""Komponen visual yang konsisten di seluruh dashboard (tanpa pemodelan ML)."""
from io import BytesIO
import pandas as pd
import plotly.graph_objects as go

MODEL_ORDER = ["M0", "M1", "M2"]
MODEL_NAMES = {
    "M0": "M0 · Data asli",
    "M1": "M1 · Standardisasi",
    "M2": "M2 · Box-Cox + standardisasi",
}
MODEL_COLORS = {"M0": "#8B9FB0", "M1": "#3985A1", "M2": "#0B9484"}
COUNTRY_COLORS = {
    "Brazil": "#0B9484", "Spain": "#E4A55A", "France": "#547FA7", "Portugal": "#9E80B9"
}
SCHEMES = ["80:20", "70:30", "60:40"]
METRICS = ["Macro F1", "Accuracy", "Weighted F1", "Macro Precision", "Macro Recall", "Weighted Precision", "Weighted Recall"]


def fmt_pct(value, digits=2):
    return f"{float(value):.{digits}f}".replace(".", ",") + "%"


def fmt_num(value, digits=2):
    return f"{float(value):,.{digits}f}".replace(",", "§").replace(".", ",").replace("§", ".")


def fig_style(fig: go.Figure, height=390, legend=True):
    fig.update_layout(
        height=height, margin=dict(l=16, r=16, t=28, b=22),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="'Plus Jakarta Sans', Inter, Arial, sans-serif", size=12, color="#334155"),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.03, xanchor="left", x=0,
            font=dict(size=12, color="#475569")
        ),
        showlegend=legend,
        hoverlabel=dict(
            bgcolor="#FFFFFF",
            bordercolor="#CBD5E1",
            font_size=12,
            font_family="'Plus Jakarta Sans', Inter, Arial, sans-serif",
            font_color="#0F172A"
        ),
    )
    fig.update_yaxes(gridcolor="#F1F5F9", zeroline=False, linecolor="#E2E8F0")
    fig.update_xaxes(gridcolor="#F8FAFC", zeroline=False, linecolor="#E2E8F0")
    return fig


def chart(st, fig):
    st.plotly_chart(fig, use_container_width=True, config={"displaylogo": False, "responsive": True})


def download_csv(st, df: pd.DataFrame, filename: str, key: str):
    st.download_button(
        "⬇️ Unduh tabel (CSV)",
        data=df.to_csv(index=False).encode("utf-8-sig"),
        file_name=filename, mime="text/csv", key=key, use_container_width=False,
    )


def intro(st, eyebrow, title, text):
    st.markdown(f'<div class="salt-eyebrow">{eyebrow}</div>', unsafe_allow_html=True)
    st.title(title)
    st.markdown(f'<p class="salt-lead">{text}</p>', unsafe_allow_html=True)

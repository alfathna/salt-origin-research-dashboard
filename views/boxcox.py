"""Analisis Box-Cox dari keluaran final dan profil diagnostik training tersimpan."""
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
from utils.data import read_result
from utils.visuals import SCHEMES, fmt_num, fig_style, chart, download_csv, intro

DETAIL = 'audit_bab3/diagnostik_lintas_rasio/'


def render():
    intro(st, '03 / Analisis Box-Cox', 'Pengaruh Transformasi terhadap Distribusi Mineral',
          'Perubahan distribusi mineral pada data latih, sebelum dan sesudah Box-Cox. Seluruh diagnostik mengikuti rasio dan mineral yang dipilih.')
    all_data = read_result(DETAIL + 'skewness_boxcox_training_3rasio_rinci.csv')
    summary = read_result(DETAIL + 'ringkasan_skewness_boxcox_training_3rasio.csv')
    profiles = read_result(DETAIL + 'profil_boxcox_training_3rasio.csv')
    by_country = read_result(DETAIL + 'skewness_per_negara_training_3rasio.csv')

    a, b = st.columns(2)
    with a:
        scheme = st.selectbox('Rasio latih:uji', SCHEMES, index=1, key='bc_scheme')
    dataset = all_data.loc[all_data['Skenario']==scheme].copy()
    with b:
        mineral = st.selectbox('Mineral terpilih', dataset['Mineral'].tolist(),
                               format_func=lambda x: x.split('_')[0], key='bc_mineral')
    row = summary.loc[summary['Skenario']==scheme].iloc[0]
    focus = dataset.loc[dataset['Mineral']==mineral].iloc[0]
    name = mineral.split('_')[0]

    st.subheader('Ringkasan delapan mineral')
    a,b,c,d=st.columns(4)
    a.metric('Data latih',int(row['N training']))
    b.metric('Rerata |skewness| sebelum',fmt_num(row['Rata-rata abs skewness sebelum'],3))
    c.metric('Rerata |skewness| sesudah',fmt_num(row['Rata-rata abs skewness sesudah'],3))
    d.metric('Mineral dengan |skewness| turun',f"{int(row['Jumlah mineral berkurang'])}/{int(row['Jumlah mineral'])}")

    st.markdown('#### Perubahan skewness delapan mineral')
    fig=go.Figure()
    labels=dataset['Mineral'].str.split('_').str[0].tolist()
    for label,col,color in [
        ('Sebelum Box-Cox','Abs skewness sebelum','#8B9FB0'),
        ('Sesudah Box-Cox','Abs skewness sesudah','#0B9484')
    ]:
        fig.add_trace(go.Bar(x=labels,y=dataset[col],name=label,marker_color=color,
                             hovertemplate='%{x}: %{y:.4f}<extra>'+label+'</extra>'))
    fig_style(fig,height=345)
    fig.update_layout(barmode='group',xaxis_title='Mineral',yaxis_title='|Skewness|')
    chart(st,fig)
    st.caption('Grafik dan empat indikator di atas merangkum seluruh mineral pada data latih rasio terpilih.')

    st.subheader(f'Detail mineral {name}')
    a,b,c=st.columns(3)
    a.metric('Skewness sebelum',fmt_num(focus['Skewness sebelum'],3))
    b.metric('Skewness sesudah',fmt_num(focus['Skewness sesudah'],3))
    c.metric('Lambda Box-Cox (λ)',fmt_num(focus['Lambda Box-Cox (fit training)'],4))

    details = profiles[(profiles['Skenario']==scheme)&(profiles['Mineral']==mineral)].copy()
    if len(details)!=int(row['N training']):
        st.error('Jumlah profil diagnostik tidak cocok dengan jumlah data latih.')
        st.stop()
    st.markdown('#### Distribusi sebelum dan sesudah')
    f=make_subplots(rows=1,cols=2,subplot_titles=('Sebelum Box-Cox','Sesudah Box-Cox + standardisasi'),
                    horizontal_spacing=.12)
    f.add_trace(go.Histogram(x=details['Sebelum (µg/g)'],name='Sebelum',marker_color='#8B9FB0',
                             hovertemplate='Konsentrasi: %{x:.4g} µg/g<br>Sampel: %{y}<extra></extra>'),row=1,col=1)
    f.add_trace(go.Histogram(x=details['Sesudah (standar)'],name='Sesudah',marker_color='#0B9484',
                             hovertemplate='Nilai: %{x:.3f}<br>Sampel: %{y}<extra></extra>'),row=1,col=2)
    fig_style(f,height=310,legend=False)
    f.update_xaxes(title_text='Konsentrasi (µg/g)',row=1,col=1)
    f.update_xaxes(title_text='Nilai tertransformasi (tanpa satuan)',row=1,col=2)
    f.update_yaxes(title_text='Jumlah sampel',row=1,col=1)
    chart(st,f)
    st.caption('Histogram data training saja. Nilai ekstrem tetap dipertahankan; sumbu kiri dan kanan memiliki satuan berbeda. Parameter Box-Cox diambil dari eksperimen yang cocok dengan keluaran final.')

    with st.expander('Lihat skewness per negara dan tabel lengkap'):
        subset = by_country[(by_country['Skenario']==scheme)&(by_country['Mineral']==mineral)].copy()
        st.markdown(f'**Skewness {name} menurut negara — training {scheme}**')
        st.dataframe(subset[['Negara','N training','Skewness sebelum','Skewness sesudah','Penurunan abs skewness']],
                     use_container_width=True,hide_index=True)
        st.caption('Skewness gabungan yang membaik tidak berarti setiap negara mengalami perbaikan serupa.')
        st.markdown('**Rincian delapan mineral**')
        columns=['Mineral','Skewness sebelum','Skewness sesudah','Lambda Box-Cox (fit training)']
        st.dataframe(dataset[columns],use_container_width=True,hide_index=True)
        download_csv(st,dataset,f'boxcox_training_{scheme.replace(":","_")}.csv','bc_csv')

    st.caption('Skewness mendekati nol tidak otomatis membuktikan asumsi Gaussian per kelas atau menjamin peningkatan hasil klasifikasi.')

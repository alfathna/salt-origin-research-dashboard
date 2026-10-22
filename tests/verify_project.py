"""Verifikasi sumber data dan hasil (tanpa perlu instal Streamlit)."""
from pathlib import Path
import sys
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / 'data' / 'results'
sys.path.insert(0, str(ROOT))


def verify():
    ds = pd.read_csv(ROOT / 'data/table_salt_origin.csv', encoding='utf-8-sig')
    assert ds.shape == (59, 10), ds.shape
    assert ds['Country'].value_counts().to_dict() == {'Brazil':11,'Spain':16,'France':16,'Portugal':16}
    assert ds['Sample'].is_unique and ds.isna().sum().sum() == 0

    rep = pd.read_csv(RESULTS/'repeated_cv_summary.csv')
    assert rep.Model.tolist() == ['M0','M1','M2']
    assert np.allclose(rep['Macro F1 (Mean)'].values, [60.259199,68.218362,86.415079], atol=5e-5)
    assert np.isclose(rep.loc[2,'Macro F1 (Mean)']-rep.loc[1,'Macro F1 (Mean)'],18.196717,atol=5e-5)

    cv5 = pd.read_csv(RESULTS/'cv5_fold_metrics.csv')
    repeats = pd.read_csv(RESULTS/'repeated_cv_50fold_metrics.csv')
    assert len(cv5)==15 and len(repeats)==150
    # Setiap model menggunakan indeks fold yang sama pada CV dan Repeated CV.
    assert repeats.groupby(['Pengulangan','Fold'])['Model'].nunique().eq(3).all()
    assert repeats.groupby(['Pengulangan','Fold'])['Kode Sampel Uji'].nunique().eq(1).all()
    core = cv5.sort_values(['Model','Fold']).reset_index(drop=True)
    first = repeats.query('Pengulangan == 1').sort_values(['Model','Fold']).reset_index(drop=True)
    assert np.allclose(core['Macro F1'],first['Macro F1'])
    for m, group in repeats.groupby('Model'):
        expected = rep.set_index('Model').loc[m,'Macro F1 (Mean)']
        assert np.isclose(group['Macro F1'].mean(), expected, atol=1e-7)

    holdout = pd.read_csv(RESULTS/'holdout_metrics_all_models.csv')
    preds = pd.read_csv(RESULTS/'holdout_predictions.csv')
    reports = pd.read_csv(RESULTS/'holdout_classification_reports.csv')
    changes = pd.read_csv(RESULTS/'audit_bab3/perubahan_prediksi_holdout.csv')
    ring = pd.read_csv(RESULTS/'audit_bab3/ringkasan_perubahan_prediksi_holdout.csv')
    assert len(holdout) == 9 and len(preds)==162 and len(changes)==54
    labels = ['Brazil','Spain','France','Portugal']
    for (scheme,model), part in preds.groupby(['Skenario','Model']):
        row=holdout.query('Skenario == @scheme and Model == @model').iloc[0]
        n=len(part)
        assert n == row['Jumlah Uji']
        assert np.isclose(100*(part['Country']==part['Prediksi']).mean(),row['Accuracy'],atol=1e-7)
        r=reports.query('Skenario == @scheme and Model == @model and Kelas in @labels')
        assert len(r) == 4 and int(r['Support'].sum()) == n
        assert set(part['Country']).issubset(labels)
        audit=changes.query('Skenario == @scheme')
        merged=part.merge(audit, on=['Skenario','Sample','Country'])
        assert len(merged)==n
        assert (merged['Prediksi']==merged['Prediksi '+model]).all()
    for _,row in ring.iterrows():
        subset=changes[changes['Skenario']==row['Skenario']]
        counted=subset['Perubahan '+row['Perbandingan']].value_counts()
        for status in ['Salah→Benar','Benar→Salah','Benar→Benar','Salah→Salah']:
            assert int(row[status])==int(counted.get(status,0))
    bc = pd.read_csv(RESULTS/'audit_bab3/diagnostik_lintas_rasio/skewness_boxcox_training_3rasio_rinci.csv')
    assert len(bc)==24 and bc.groupby('Skenario').size().to_dict()=={'80:20':8,'70:30':8,'60:40':8}
    assert (bc['N training']==bc['Skenario'].map({'80:20':47,'70:30':41,'60:40':35})).all()
    assert (bc['Abs skewness sebelum'].round(8)>=0).all()
    assert (bc['Abs skewness sesudah'].round(8)>=0).all()
    assert (bc['Abs skewness berkurang']).all()
    # Periksa precision, recall, F1 per negara terhadap prediksi uji asli.
    for (scheme, model), part in preds.groupby(['Skenario','Model']):
        report = reports.query('Skenario == @scheme and Model == @model and Kelas in @labels')
        for country in labels:
            row = report[report['Kelas'] == country].iloc[0]
            tp = int(((part['Country'] == country) & (part['Prediksi'] == country)).sum())
            actual = int((part['Country'] == country).sum())
            predicted = int((part['Prediksi'] == country).sum())
            precision = tp/predicted if predicted else 0.0
            recall = tp/actual if actual else 0.0
            f1 = 2*precision*recall/(precision+recall) if precision+recall else 0.0
            assert np.allclose([precision, recall, f1, actual],
                               [row['Precision'], row['Recall'], row['F1'], row['Support']])
    # Diagnostik tambahan: profil 3 rasio mengikuti semua train index.
    ext = RESULTS/'audit_bab3/diagnostik_lintas_rasio'
    profiles = pd.read_csv(ext/'profil_boxcox_training_3rasio.csv')
    perclass = pd.read_csv(ext/'skewness_per_negara_training_3rasio.csv')
    assert len(profiles) == 8*(47+41+35) and len(perclass)==3*4*8
    assert profiles.groupby(['Skenario','Mineral']).size().eq(
        profiles['Skenario'].map({'80:20':47,'70:30':41,'60:40':35})
        .groupby([profiles['Skenario'],profiles['Mineral']]).first()
    ).all()
    assert profiles.groupby(['Skenario','Sample']).Mineral.nunique().eq(8).all()
    assert set(profiles.Mineral)==set(['K_ug_g','Na_ug_g','Ca_ug_g','Mg_ug_g','Fe_ug_g','Mn_ug_g','Zn_ug_g','Cu_ug_g'])
    for _, r in bc.iterrows():
        p = profiles[(profiles.Skenario == r['Skenario']) & (profiles.Mineral == r['Mineral'])]
        assert np.allclose([p['Sebelum (µg/g)'].skew(), p['Sesudah (standar)'].skew()],
                           [r['Skewness sebelum'], r['Skewness sesudah']], atol=1e-6)
    original70 = pd.read_csv(RESULTS/'audit_bab3/skewness_per_negara_training70.csv')
    new70 = perclass.query('Skenario == "70:30"').drop(columns='Skenario')
    join = new70.merge(original70,on=['Negara','Mineral'],suffixes=('_new','_old'))
    assert len(join)==32
    for field in ['Skewness sebelum','Skewness sesudah']:
        assert np.allclose(join[field+'_new'],join[field+'_old'],atol=1e-6)
    assert len(list(RESULTS.rglob('*.csv')))==26
    assert len(list(RESULTS.rglob('*.png')))==16
    print('PASS: dataset dan semua skema/model sesuai; 3 rasio x 8 mineral profil cocok; diagnostik 70:30 per negara identik; 26 CSV, 16 PNG.')

if __name__ == '__main__':
    verify()

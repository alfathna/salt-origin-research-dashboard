"""Ekspor diagnostik deskriptif lintas rasio untuk dashboard.

Jalankan secara offline, BUKAN dari Streamlit. Ini mengulangi fit Box-Cox
pada training tiap rasio untuk memverifikasi lambda/skewness terhadap file
final notebook; TIDAK melatih atau mengubah classifier GNB.
"""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PowerTransformer

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT/'data'/'table_salt_origin.csv'
OUT = ROOT/'data'/'results'/'audit_bab3'/'diagnostik_lintas_rasio'
ORIGINAL = OUT/'skewness_boxcox_training_3rasio_rinci.csv'
EXPECTED = pd.read_csv(ORIGINAL)
df = pd.read_csv(DATA, encoding='utf-8-sig')
raw = df.drop(columns=['Sample','Country'])
X = raw.copy()
X['Na_mg_g'] = X['Na_mg_g']*1000
X = X.rename(columns={'Na_mg_g':'Na_ug_g'})
y = df['Country']

profiles = []
country_rows = []
ratios = {'80:20': .2, '70:30': .3, '60:40': .4}
for ratio, test_size in ratios.items():
    train_idx, _ = train_test_split(
        np.arange(len(X)), test_size=test_size, random_state=42, stratify=y
    )
    before = X.iloc[train_idx]
    transformer = PowerTransformer(method='box-cox',standardize=True)
    array_after = transformer.fit_transform(before)
    after = pd.DataFrame(array_after, index=before.index, columns=before.columns)

    for mineral, lam in zip(before.columns, transformer.lambdas_):
        check = EXPECTED.query('Skenario == @ratio and Mineral == @mineral').iloc[0]
        values = [float(before[mineral].skew()),float(after[mineral].skew()),float(lam)]
        checkvals = [float(check['Skewness sebelum']), float(check['Skewness sesudah']),float(check['Lambda Box-Cox (fit training)'])]
        if not np.allclose(values, checkvals, rtol=1e-5, atol=1e-5):
            raise AssertionError(f'Diagnostik {ratio}/{mineral} tidak cocok! {values} vs {checkvals}')

    for idx in before.index:
        for mineral in before.columns:
            profiles.append({
                'Skenario':ratio, 'Sample':df.loc[idx,'Sample'],
                'Negara':df.loc[idx,'Country'], 'Mineral':mineral,
                'Sebelum (µg/g)':float(before.loc[idx,mineral]),
                'Sesudah (standar)':float(after.loc[idx,mineral]),
            })

    for nation, indexes in y.loc[before.index].groupby(y.loc[before.index]).groups.items():
        for mineral in before.columns:
            skew_b = float(before.loc[indexes,mineral].skew())
            skew_a = float(after.loc[indexes,mineral].skew())
            country_rows.append({
                'Skenario':ratio,'Negara':nation,'Mineral':mineral,
                'N training':len(indexes),
                'Skewness sebelum':skew_b,'Skewness sesudah':skew_a,
                'Abs skewness sebelum':abs(skew_b),'Abs skewness sesudah':abs(skew_a),
                'Penurunan abs skewness': bool(abs(skew_a) < abs(skew_b)-1e-12),
            })

per_class = pd.DataFrame(country_rows)
per70 = pd.read_csv(ROOT/'data'/'results'/'audit_bab3'/'skewness_per_negara_training70.csv')
compare = per_class[per_class['Skenario']=='70:30'].drop(columns='Skenario')
keys = ['Negara','Mineral']
joined = compare.merge(per70, on=keys, suffixes=('_new','_old'), validate='one_to_one')
for c in ['Skewness sebelum','Skewness sesudah','Abs skewness sebelum','Abs skewness sesudah']:
    if not np.allclose(joined[c+'_new'], joined[c+'_old'], atol=1e-6):
        raise AssertionError(f'Diagnostik per negara rasio 70:30 tidak sesuai: {c}')

OUT.mkdir(exist_ok=True, parents=True)
pd.DataFrame(profiles).to_csv(OUT/'profil_boxcox_training_3rasio.csv',index=False,encoding='utf-8-sig')
per_class.to_csv(OUT/'skewness_per_negara_training_3rasio.csv',index=False,encoding='utf-8-sig')
print('PASS: 24 fit parameter cocok, 70:30 per-negara cocok; profil',len(profiles),'baris; per negara',len(per_class),'baris.')

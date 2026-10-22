"""Uji portable readers tanpa perlu server/browser Streamlit."""
from pathlib import Path
import os, sys, types
ROOT = Path(__file__).resolve().parents[1]
# Streamlit cache decorator mocked ONLY for standalone data-reader tests.
st = types.ModuleType("streamlit")
st.cache_data = lambda *args, **kw: (lambda fn: fn)
sys.modules['streamlit'] = st
sys.path.insert(0, str(ROOT))
from utils.data import read_dataset, read_result

os.chdir(ROOT.parent)
assert len(read_dataset()) == 59
for path in (
    'repeated_cv_summary.csv',
    'holdout_predictions.csv',
    'audit_bab3/diagnostik_lintas_rasio/profil_boxcox_training_3rasio.csv',
    'audit_bab3/diagnostik_lintas_rasio/skewness_per_negara_training_3rasio.csv',
):
    assert not read_result(path).empty, path
for path in ('../table_salt_origin.csv', '/tmp/forbidden.csv', 'audit_bab3/../../../anything.csv'):
    try:
        read_result(path)
    except ValueError:
        pass
    else:
        raise AssertionError(f'Unsafe path allowed: {path}')
try:
    read_result('audit_bab3/diagnostik_lintas_rasio/missing_example.csv')
except FileNotFoundError as e:
    assert 'missing_example.csv' in str(e)
else:
    raise AssertionError('Expected FileNotFoundError for missing CSV')
print('PASS: pembacaan data dari folder kerja berbeda, jalur bertingkat, dan penanganan berkas hilang.')

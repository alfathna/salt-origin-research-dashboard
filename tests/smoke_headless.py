"""Headless code-path smoke tests (mock Streamlit controls; NOT browser QA)."""
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

class FakeStreamlit(types.ModuleType):
    def __init__(self):
        super().__init__('streamlit')
        self.choices = {}
        self.figures = 0
        self.dataframes = 0
        self.column_config = types.SimpleNamespace(NumberColumn=lambda **kwargs: None)
    def __enter__(self): return self
    def __exit__(self, exc_type, exc, tb): return False
    def cache_data(self, *args, **kwargs):
        return lambda fn: fn
    def columns(self, specs, **kwargs):
        n = specs if isinstance(specs, int) else len(specs)
        return [self] * n
    def selectbox(self, label, options, **kwargs):
        key=kwargs.get('key')
        return self.choices.get(key, options[kwargs.get('index',0)])
    def multiselect(self, label, options, **kwargs): return self.choices.get(kwargs.get('key'), kwargs.get('default',[]))
    def text_input(self, *a, **kw): return self.choices.get(kw.get('key'), '')
    def expander(self, *a, **kw): return self
    def plotly_chart(self, fig, **kwargs):
        assert len(fig.data)>0
        fig.to_json()
        self.figures+=1
    def dataframe(self, data, **kwargs):
        assert data is not None
        self.dataframes+=1
    def image(self, file, **kwargs): assert Path(file).is_file()
    def stop(self): raise AssertionError('Streamlit st.stop() reached')
    def __getattr__(self, k):
        if k.startswith('__'): raise AttributeError(k)
        return lambda *args,**kwargs: None

st = FakeStreamlit()
sys.modules['streamlit'] = st

from views import overview, eksplorasi_data, boxcox, evaluasi, klasifikasi

def main():
    pages = [overview.render, eksplorasi_data.render, boxcox.render, evaluasi.render, klasifikasi.render]
    for fn in pages: fn()
    n = 5
    # Filter EDA termasuk negara tunggal dan mineral Na dengan satuan khusus.
    st.choices.update(eda_countries=['Spain'],eda_mineral='Na_mg_g',eda_search='SE')
    eksplorasi_data.render(); n+=1
    st.choices.clear()
    for scheme in ['80:20','70:30','60:40']:
        st.choices['bc_scheme'] = scheme
        for mineral in ['K_ug_g','Na_ug_g','Ca_ug_g','Mg_ug_g','Fe_ug_g','Mn_ug_g','Zn_ug_g','Cu_ug_g']:
            st.choices['bc_mineral'] = mineral
            boxcox.render(); n+=1
        st.choices['cl_scheme'] = scheme
        for model in ['M0','M1','M2']:
            for pair in ['M1→M2','M0→M1','M0→M2']:
                st.choices.update(cl_model=model,cl_status='Salah',cl_country='France',cl_pair=pair)
                klasifikasi.render(); n+=1
    st.choices.clear()
    for scheme in evaluasi.SCHEMES_UI:
        for metric in evaluasi.METRICS:
            st.choices.update(ev_scheme=scheme, ev_metric=metric)
            evaluasi.render(); n+=1
    print(f'PASS: {n} halaman/varian dieksekusi tanpa error pada stub Streamlit, {st.figures} plotly figures, {st.dataframes} dataframes.')
    print('NOTE: Pengujian ini tidak menggantikan tes Streamlit sungguhan di browser (Tahap B).')

if __name__ == '__main__': main()

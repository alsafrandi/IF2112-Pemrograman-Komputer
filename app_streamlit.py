import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go


st.set_page_config(layout="wide")

def load_data():
    dataMinyak = pd.read_csv('produksi_minyak_mentah.csv')
    country = pd.read_json('kode_negara_lengkap.json')
    mergeResult = pd.merge(left=country, right=dataMinyak, left_on='alpha-3', right_on='kode_negara')
    data = dataHasil=mergeResult[['name','tahun','produksi','alpha-3','country-code','iso_3166-2','region','sub-region','intermediate-region','region-code','sub-region-code']]
    data2 = data.rename({'name': 'Negara','produksi':'Produksi' ,'tahun': 'Tahun','alpha-3':'Kode Negara','region':'Region','sub-region':'Sub Region'}, axis='columns')
    return data2
def get_total_dataframe(dataset):
    total_dataframe = dataset[['Negara','Tahun','Kode Negara','Region','Sub Region','Produksi']]
    return total_dataframe
st.header("++++++++++++ANALISA DATA PRODUKSI MINYAK DI SELURUH NEGARA++++++++++++")
st.header("")
dataset=load_data()
dataset_bersih = dataset[dataset['Produksi'] != 0]
dataset_tidak_produksi = dataset[dataset['Produksi'] == 0]

st.subheader("GRAFIK PENDAPATAN MINYAK BERDASARKAN NEGARA")
data_select_negara = dataset_bersih.groupby('Negara',as_index=False).mean()
select = st.selectbox('Pilih negara',data_select_negara['Negara'])
negara_data = dataset[dataset['Negara'] == select]
if select:
    state_total = get_total_dataframe(negara_data)
    st.subheader("Grafik pendapatan minyak negara "+select)
    

    state_total_graph = px.bar(state_total, x='Tahun',y='Produksi',labels={'Negara produsen minyak = %s' % (select)})
    st.plotly_chart(state_total_graph,use_container_width=True)


st.subheader("NEGARA DENGAN NILAI KUMULATIF PRODUKSI TERTINGGI")
nilai_input = int(st.number_input("Banyak Negara", min_value=1,max_value=100))
Data = dataset[['Negara','Kode Negara','Tahun','Produksi','Region','Sub Region']]
Data['Produksi Kumulatif'] = Data['Produksi'].cumsum()
total = Data.sort_values(by=['Produksi Kumulatif'],ascending=False)
urut = total.groupby('Negara',as_index=False).sum()
dataMax = urut.sort_values(by=['Produksi'],ascending=False).head(nilai_input)
fig = px.pie(dataMax, values='Produksi', names='Negara')
st.plotly_chart(fig, use_container_width=True)


st.subheader("GRAFIK PENDAPATAN MINYAK BERDASARKAN TAHUN")
select_year = st.selectbox("Lihat Tahun",dataset['Tahun'])
if select_year:
        
    state_year = dataset[dataset['Tahun'] == select_year]
    state_total = get_total_dataframe(state_year)

    st.subheader("Grafik pendapatan minyak pada tahun "+str(select_year))
    state_total_graph = px.bar(state_total, x='Produksi',y='Negara',labels={'Negara produsen minyak = %s' % (select)})
    st.plotly_chart(state_total_graph,use_container_width=True)
        
    st.subheader("Tampilan Negara tertinggi Penghasil Minyak pada tahun "+str(select_year))
    nilai = int(st.number_input("Banyak Negara Tahun", min_value=1,max_value=100))
    dataMax = state_total.sort_values(by=['Produksi'],ascending=False).head(nilai)
    fig = px.pie(dataMax, values='Produksi', names='Negara')
    st.plotly_chart(fig, use_container_width=True)
col1, col2 = st.columns((3,3))
with col1:
    st.subheader("Negara Produksi tertinggi pada tahun "+str(select_year))
    data_tahun =dataset_bersih[dataset_bersih["Tahun"] == select_year]
    data_tahun=data_tahun[data_tahun['Produksi']==data_tahun['Produksi'].max()]
    st.subheader("Total produksi : "+data_tahun['Produksi'].to_string(index=False))
    st.markdown("Negara      : "+data_tahun['Negara'].to_string(index=False))
    st.markdown("Kode Negara : "+data_tahun['Kode Negara'].to_string(index=False))
    st.markdown("Tahun       : "+data_tahun['Tahun'].to_string(index=False))
    st.markdown("Region      : "+data_tahun['Region'].to_string(index=False))
    st.markdown("Sub Region  : "+data_tahun['Sub Region'].to_string(index=False))

with col2:
    st.subheader("Negara Produksi terendah pada tahun "+str(select_year))
    data_tahun =dataset_bersih[dataset_bersih["Tahun"] == select_year]
    data_tahun=data_tahun[data_tahun['Produksi']==data_tahun['Produksi'].min()]
    data_tahun = data_tahun.head(5)
    st.subheader("Total produksi : "+data_tahun['Produksi'].to_string(index=False))
    st.markdown("Negara      : "+data_tahun['Negara'].to_string(index=False))
    st.markdown("Kode Negara : "+data_tahun['Kode Negara'].to_string(index=False))
    st.markdown("Tahun       : "+data_tahun['Tahun'].to_string(index=False))
    st.markdown("Region      : "+data_tahun['Region'].to_string(index=False))
    st.markdown("Sub Region  : "+data_tahun['Sub Region'].to_string(index=False))

st.subheader("Negara tidak berproduksi pada tahun "+str(select_year))
data_tahun =dataset_tidak_produksi[dataset_tidak_produksi["Tahun"] == select_year]
st.dataframe(data_tahun[["Negara",'Kode Negara',"Tahun","Produksi",'Region','Sub Region']])
pos1, pos2 ,pos3= st.columns((3,3,3))
with pos1:
    st.subheader("Negara dengan produksi tertinggi sepanjang tahun ")
    data_tahun_tertinggi = dataset_bersih
    data_tertinggi = data_tahun_tertinggi.sort_values(by=['Produksi'],ascending=False).head(1)
    st.subheader("Total produksi : "+data_tertinggi['Produksi'].to_string(index=False))
    st.markdown("Negara      : "+data_tertinggi['Negara'].to_string(index=False))
    st.markdown("Kode Negara : "+data_tertinggi['Kode Negara'].to_string(index=False))
    st.markdown("Tahun       : "+data_tertinggi['Tahun'].to_string(index=False))
    st.markdown("Region      : "+data_tertinggi['Region'].to_string(index=False))
    st.markdown("Sub Region  : "+data_tertinggi['Sub Region'].to_string(index=False))
    
with pos2:
    st.subheader("Negara dengan produksi terendah sepanjang tahun ")
    data_terkecil = dataset_bersih
    data_terkecil = data_tahun_tertinggi.sort_values(by=['Produksi'],ascending=True).head(1)
    st.subheader("Total produksi : "+data_terkecil['Produksi'].to_string(index=False))
    st.markdown("Negara      : "+data_terkecil['Negara'].to_string(index=False))
    st.markdown("Kode Negara : "+data_terkecil['Kode Negara'].to_string(index=False))
    st.markdown("Tahun       : "+data_terkecil['Tahun'].to_string(index=False))
    st.markdown("Region      : "+data_terkecil['Region'].to_string(index=False))
    st.markdown("Sub Region  : "+data_terkecil['Sub Region'].to_string(index=False))

st.subheader("Negara tidak produksi di sepanjang tahun")
st.dataframe(dataset_tidak_produksi[['Negara','Kode Negara','Tahun','Produksi','Region','Sub Region']])
    

st.markdown(" <style>footer {visibility: hidden;}</style> ", unsafe_allow_html=True)

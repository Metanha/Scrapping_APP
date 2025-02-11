import streamlit as st
import pandas as pd
import glob
import os


st.markdown("<h1 style='text-align: center; color: black;'>MY DATA APP</h1>", unsafe_allow_html=True)

st.markdown("""
This app allows you to download scraped data on motocycles from expat-dakar 
* **Python libraries:** base64, pandas, streamlit
* **Data source:** [Expat-Dakar](https://www.expat-dakar.com/).
""")

def load_(dataframe, title, key):
    st.markdown("""
    <style>
    div.stButton {text-align:center}
    </style>""", unsafe_allow_html=True)

    if st.button(title, key):
        st.subheader('Display data dimension')
        st.write('Data dimension: ' + str(dataframe.shape[0]) + ' rows and ' + str(dataframe.shape[1]) + ' columns.')
        st.dataframe(dataframe)


st.markdown('''<style> .stButton>button {
    font-size: 12px;
    height: 3em;
    width: 25em;
}</style>''', unsafe_allow_html=True)


load_(pd.read_excel('data/P1_Ordinateurs.xlsx'), 'Ordinateurs', '1')
load_(pd.read_excel('data/P1_Telephones.xlsx'), 'Téléphones', '2')
load_(pd.read_excel('data/P1_cinema.xlsx'), 'Télévision', '3')


#range(len(glob.glob("data/*.xlsx"))),
for i,f in enumerate(glob.glob("data/*.xlsx")):
    df =pd.read_excel(f)
    filename = os.path.basename(f).replace(".xlsx", "")  # Extraire le nom du fichier sans extension
    load_(df, filename, str(i+1))

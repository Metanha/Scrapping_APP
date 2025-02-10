import streamlit as st
import pandas as pd
import os
from io import BytesIO
import requests
from requests import get
from bs4 import BeautifulSoup as bs
import glob

def load_(dataframe, title, key):
    st.markdown("""
    <style>
    div.stButton {text-align:center}
    </style>""", unsafe_allow_html=True)

    if st.button(title, key):
        st.subheader('Display data dimension')
        st.write('Data dimension: ' + str(dataframe.shape[0]) + ' rows and ' + str(dataframe.shape[1]) + ' columns.')
        st.dataframe(dataframe)


load_(pd.read_excel('data/P1_Ordinateurs.xlsx'), 'Ordinateurs', '1')
load_(pd.read_excel('data/P1_Telephones.xlsx'), 'Téléphones', '2')
load_(pd.read_excel('data/P1_cinema.xlsx'), 'Télévision', '3')


def download_dataframe(df):
    """Permet de télécharger un DataFrame en CSV."""
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Télécharger les données",
        data=csv,
        file_name="donnees_scrapees.csv",
        mime="text/csv"
    )

url="https://www.expat-dakar.com/ordinateurs?page=1"
def scrape_data(url):
    """Scrape les données d'une page Expat-Dakar."""
    
    res=get(url) # récupère le code HTML de la page
    soup=bs(res.text,"html.parser") #stocker le code html dans un objet beautifulSoup ,

    contenairs=soup.find_all("div",class_="listing-card__content 1")

    data=pd.DataFrame(columns=["Details","Etat","Marque","Addresse","Prix","Lien_image"])
    
    for content in contenairs:
        try:
            details=content.find("div",class_="listing-card__header__title").text.replace("\n","").replace("  ","")
            Etat=content.find("div",class_="listing-card__header__tags").find_all("span")[0].text
            Marque=content.find("div",class_="listing-card__header__tags").find_all("span")[1].text
            Addresse=content.find("div",class_="listing-card__header__location").text.replace("\n","").replace("  ","")
            Prix=content.find("div",class_="listing-card__info-bar__price").find("span",class_="listing-card__price__value 1").text.replace("\n","").replace("F Cfa","").replace("\u202f","").replace(" ","")
            Lien_image=content.find_all("img", class_="listing-card__image__resource vh-img") #["src"]
    
            d=pd.DataFrame({"Details":[details],"Etat":[Etat],"Marque":[Marque],"Addresse":[Addresse],"Prix":[Prix],"Lien_image":[Lien_image]})
            
            data=pd.concat([data,d],ignore_index=True)
            return data
        except Exception as e:
            print(f"Erreur lors de l'extraction d'un contenu : {e}")
            return None

download_dataframe(scrape_data(url))


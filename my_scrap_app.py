import streamlit as st
import pandas as pd
import os
from io import BytesIO
import requests
from requests import get
from bs4 import BeautifulSoup as bs
import glob
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
#--------------------------------------------------------------------------
#Charger les donnéés
def load_(dataframe, title):
    st.markdown("""
    <style>
    div.stButton {text-align:center}
    </style>""", unsafe_allow_html=True)

    #if st.button(title, key):
    st.subheader('Display data dimension')
    st.write('Data dimension: ' + str(dataframe.shape[0]) + ' lignes et ' + str(dataframe.shape[1]) + ' colonnes.')
    st.dataframe(dataframe)

############## CODE SCRAPING DES ORDINATEURS
def scrape_data_ordin(url):
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
        except Exception as e:
            print(f"Erreur lors de l'extraction d'un contenu : {e}")
    return data

###########SCRAPPER LES TELEPHONES
def scrape_data_telep(url):
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
    
        except Exception as e:
            print(f"Erreur lors de l'extraction d'un contenu : {e}")
    return data

########## SCRAPER LES TELEVISION
def scrape_data_tele(url):
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
    
        except Exception as e:
            print(f"Erreur lors de l'extraction d'un contenu : {e}{page}")
    return data

# Configuration de la page 
st.set_page_config(page_title="Web Scraping App")

# Barre latérale pour la navigation
menu = st.sidebar.radio(
    "Navigation",
    ["📊 Scraper des données", "📈 Dashboard des données", "📝 Formulaire d'évaluation"]
)

# 1️⃣ **Scraper des données en temps réel**
if menu == "📊 Scraper des données":
    #le nombre de pages a scrapper
    page=st.sidebar.selectbox("Choisissez le nombre de page à scrapper: ",[i for i in range(1,275)])
    
    st.title("Scraper des données")
    categorie=st.radio("Choisissez les données à scrapper ",["Ordinateurs","Téléphones","Télévision"])
    #url = st.text_input("Entrez l'URL de la page à scraper :", "")
    #Creation de deux colonnes pour aligner les boutons sur la même ligne  
    col1,col2=st.columns(2)
    with col1:
        lance_scrap=st.button("Lancer le scraping")
    with col2:
            telecharger_donne=st.button("📥 Télécharger les données")
    if lance_scrap:         
        if categorie=="Ordinateurs":
            url="https://www.expat-dakar.com/ordinateurs?page=1"
            df=scrape_data_ordin(url)
            load_(df,"Ordinateurs")
        elif categorie=="Téléphones":
            url="https://www.expat-dakar.com/telephones?page=1"
            df=scrape_data_telep(url)
            load_(df,"Téléphones")
        elif categorie=="Télévision":
            url="https://www.expat-dakar.com/tv-home-cinema?page=1"
            df=scrape_data_tele(url)
            load_(df,"Télévision")
    
     #Telecharger les données scrappées  
    if telecharger_donne:
        csv = df.to_csv(path_or_buf="data/donnees_scrapes.csv",index=False).encode('utf-8')


#chargement des données
df_ordinateurs=pd.read_excel('data/P1_Ordinateurs.xlsx')
df_telephones=pd.read_excel('data/P1_Telephones.xlsx')
df_television=pd.read_excel('data/P1_cinema.xlsx')

#Ajout dune liste déroulante dans la barre lateralle
categorie=st.sidebar.selectbox("Télécharger les données déjà scrapper: choisissez une catégorie ",["Ordinateurs","Téléphones","Télévision"])

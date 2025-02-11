import streamlit as st
import pandas as pd
import time
import matplotlib.pyplot as plt
import plotly.express as px
from bs4 import BeautifulSoup


# Configuration de la page 
st.set_page_config(page_title="Web Scraping App", layout="wide")

# Barre latérale pour la navigation
menu = st.sidebar.radio("Navigation", ["📊 Scraper des données", "📈 Dashboard des données", "📝 Formulaire d'évaluation"])

# 📊 **Scraper des données**
if menu == "📊 Scraper des données":
    st.title("Scraper des données")
    
    categorie=st.radio("Choisissez les données à scrapper ",["Ordinateurs","Téléphones","Télévision"])
    #url = st.text_input("Entrez l'URL de la page à scraper :", "")
    #Creation de deux colonnes pour aligner les boutons sur la même ligne  
    col1,col2=st.columns(2)
    with col1:
        lance_scrap=st.button("Lancer le scraping")
    with col2:
            telecharger_donne=st.button("📥 Télécharger les données")     
       # Sélection du nombre de pages
    url=""
    if categorie=="Ordinateurs":
        url="https://www.expat-dakar.com/ordinateurs?page=1"
        num_pages = st.sidebar.slider("Nombre de pages à scraper :", 1, 10, 1)
    elif categorie=="Téléphones":
        url="https://www.expat-dakar.com/telephones?page=1"
        num_pages = st.sidebar.slider("Nombre de pages à scraper :", 1, 11, 1)
    elif categorie=="Télévision":
        url="https://www.expat-dakar.com/tv-home-cinema?page=1"
        num_pages = st.sidebar.slider("Nombre de pages à scraper :", 1, 12, 1)
    
    if lance_scrap:         
        if categorie=="Ordinateurs":
            df=scrape_dynamic_site(url)
            load_(df,"Ordinateurs")
        elif categorie=="Téléphones":
            df=scrape_dynamic_site(url)
            load_(df,"Téléphones")
        elif categorie=="Télévision":
            df=scrape_dynamic_site(url)
            load_(df,"Télévision")
    
     #Telecharger les données scrappées  
    if telecharger_donne:
        csv = df.to_csv(path_or_buf="data/donnees_scrapes.csv",index=False).encode('utf-8')

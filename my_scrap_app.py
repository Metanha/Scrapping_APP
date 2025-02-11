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


# 📈 **Dashboard des Données Scrapées**
elif menu == "📈 Dashboard des données":
    st.title("📊 Dashboard des Données Scrapées")

    if "scraped_data" in st.session_state and not st.session_state["scraped_data"].empty:
        df = st.session_state["scraped_data"]

        # **Histogramme des Prix**
        st.subheader("📈 Distribution des Prix")
        fig, ax = plt.subplots()
        ax.hist(df["Prix"], bins=20, color="blue", alpha=0.7)
        ax.set_xlabel("Prix (F CFA)")
        ax.set_ylabel("Nombre de produits")
        ax.set_title("Distribution des prix")
        st.pyplot(fig)

        # **Répartition des Marques**
        st.subheader("🎯 Répartition des Marques")
        fig_pie = px.pie(df, names="Marque", title="Répartition des Marques", hole=0.4)
        st.plotly_chart(fig_pie)

        # **Comparaison des prix par marque**
        st.subheader("💰 Comparaison des Prix par Marque")
        fig_bar = px.bar(df, x="Marque", y="Prix", title="Prix moyen par marque", color="Marque", barmode="group")
        st.plotly_chart(fig_bar)

        # **Tableau interactif avec filtres**
        st.subheader("📜 Table des Données Filtrables")
        marque_filter = st.multiselect("Filtrer par Marque :", df["Marque"].unique())
        if marque_filter:
            df = df[df["Marque"].isin(marque_filter)]
        st.dataframe(df)
    else:
        st.warning("Aucune donnée disponible. Faites d'abord un scraping.")

# 📝 Formulaire d'évaluation**
elif menu == "📝 Formulaire d'évaluation":
    st.title("📝 Formulaire d'évaluation")
    
    kobo_link = "<iframe src=https://ee.kobotoolbox.org/i/TOv0huae width="800" height="600"></iframe>"
    st.markdown(f'<iframe src="{kobo_link}" width="700" height="800"></iframe>', unsafe_allow_html=True)



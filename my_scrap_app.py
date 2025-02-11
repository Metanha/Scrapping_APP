import streamlit as st
import pandas as pd
import time
import matplotlib.pyplot as plt
import plotly.express as px
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


#Configuration de Selenium
def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Exécuter en mode sans interface graphique
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver
    
# Fonction de scraping dynamique
def scrape_dynamic_site(url):
    driver = get_driver()
    driver.get(url)

    # Attendre le chargement complet
    time.sleep(3)

    # Récupération du HTML après exécution de JavaScript
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Fermer le navigateur après récupération des données
    driver.quit()

    # Extraction des éléments
    contenairs = soup.find_all("div", class_="listing-card__content 1")
    data = pd.DataFrame(columns=["Details", "Etat", "Marque", "Adresse", "Prix", "Lien_image"])
    
    for content in contenairs:
        try:
            details = content.find("div", class_="listing-card__header__title").text.strip()
            Etat = content.find("div", class_="listing-card__header__tags").find_all("span")[0].text
            Marque = content.find("div", class_="listing-card__header__tags").find_all("span")[1].text
            Adresse = content.find("div", class_="listing-card__header__location").text.strip().replace(",\n","").replace("   ","")
            Prix = content.find("div", class_="listing-card__info-bar__price").find("span", class_="listing-card__price__value 1").text.strip().replace("F Cfa", "").replace("\u202f", "").replace(" ", "")
            Lien_image = content.find("img", class_="listing-card__image__resource vh-img")["src"] if content.find("img", class_="listing-card__image__resource vh-img") else ""

            d = pd.DataFrame({"Details": [details], "Etat": [Etat], "Marque": [Marque], "Adresse": [Adresse], "Prix": [Prix], "Lien_image": [Lien_image]})
            data = pd.concat([data, d], ignore_index=True)
        except Exception as e:
            print(f"Erreur lors de l'extraction d'un contenu : {e}")

    return data



# 📌 Configuration de la page 
st.set_page_config(page_title="Web Scraping App", layout="wide")

# 📌 Barre latérale pour la navigation
menu = st.sidebar.radio("Navigation", ["📊 Scraper des données", "📈 Dashboard des données"], "📝 Formulaire d'évaluation")

# 📊 **Scraper des données**
if menu == "📊 Scraper des données":
    st.title("Scraper des données")
    
    # Sélection du nombre de pages
    
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
            num_pages = st.sidebar.slider("Nombre de pages à scraper :", 1, 10, 1)
            df=scrape_dynamic_site(url)
            load_(df,"Ordinateurs")
        elif categorie=="Téléphones":
            url="https://www.expat-dakar.com/telephones?page=1"
            num_pages = st.sidebar.slider("Nombre de pages à scraper :", 1, 11, 1)
            df=scrape_dynamic_site(url)
            load_(df,"Téléphones")
        elif categorie=="Télévision":
            url="https://www.expat-dakar.com/tv-home-cinema?page=1"
            num_pages = st.sidebar.slider("Nombre de pages à scraper :", 1, 12, 1)
            df=scrape_dynamic_site(url)
            load_(df,"Télévision")
    
     #Telecharger les données scrappées  
    if telecharger_donne:
        csv = df.to_csv(path_or_buf="data/donnees_scrapes.csv",index=False).encode('utf-8')

    # Boutons
    col1, col2 = st.columns(2)
    with col1:
        lancer_scraping = st.button("Lancer le scraping")
    with col2:
        telecharger_donnees = st.button("📥 Télécharger les données")

    if lancer_scraping:
        base_url = urls[categorie]
        df = scrape_dynamic_site(base_url, num_pages)
        st.session_state["scraped_data"] = df  # Stocker les données en mémoire
        st.write(f"📊 **{len(df)} produits trouvés sur {num_pages} pages**")
        st.dataframe(df)

    if telecharger_donnees:
        if "scraped_data" in st.session_state and not st.session_state["scraped_data"].empty:
            df = st.session_state["scraped_data"]
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Télécharger en CSV", csv, "donnees_scrapees.csv", "text/csv")
        else:
            st.warning("Aucune donnée disponible. Lancez d'abord un scraping.")

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

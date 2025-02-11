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

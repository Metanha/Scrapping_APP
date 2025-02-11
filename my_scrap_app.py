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
page=st.sidebar.selectbox("Choisissez le nombre de page à scrapper: ",[i for i in range(1,275)])

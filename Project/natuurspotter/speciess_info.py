import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
from tabulate import tabulate
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.styles import getSampleStyleSheet
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()
DATA_DIR = BASE_DIR / "dataoutputs"
IMAGES_DIR = DATA_DIR / "images"

IMAGES_DIR.mkdir(parents=True, exist_ok=True)

def species_info(species):
    headers = {"User-Agent":""}
    url="https://waarnemingen.be/species/search/"
    wiki_url=f"https://en.wikipedia.org/wiki/{species}"
    search_parameters={"q":species,"species_group":16}
    response = requests.get(url,params=search_parameters)
    rarity_soup = BeautifulSoup(response.text,"html.parser")
    rarity_status_dutch = rarity_soup.find("span",class_="hidden-sm").get_text(strip=True)
    translation_api = "https://api.mymemory.translated.net/get"
    params = {
        "q": rarity_status_dutch,
        "langpair": "nl|en"
    }
    r = requests.get(translation_api, params=params, timeout=10)
    data = r.json()
    rarity_status_english = data["responseData"]["translatedText"]
    soup = BeautifulSoup(response.text,"html.parser")
    new_url = soup.find("a",href=re.compile(r"^/species/\d+/$"))
    if new_url is None:
        return "This species doesnot belong to Coleoptera,Thank you"
    species_url="https://waarnemingen.be"+new_url["href"]
    response2=requests.get(species_url)
    soup2=BeautifulSoup(response2.text,"html.parser")
    description_in_dutch = soup2.find("div",class_="app-content-section js-user-content").get_text(strip=True)
    response3=requests.get(wiki_url,headers=headers)
    soup3=BeautifulSoup(response3.text,"html.parser")
    div_container=soup3.find("div",class_="mw-content-ltr mw-parser-output")
    para=""
    for i in div_container.find_all("p"):
        if i.get_text(strip=True):
            para=i
            break
    for j in para.find_all("sup"):
        j.decompose()
    for k in para.find_all("style"):
        k.decompose()
    description_in_english=para.get_text()

    namur_url="https://waarnemingen.be"+new_url["href"]+"observations/?date_after=2024-12-25&date_before=2025-12-25&country_division=24&search=&user=&location=&sex=&month=&life_stage=&activity=&method="
    response4=requests.get(namur_url)
    soup4=BeautifulSoup(response4.text,"html.parser")
    table = soup4.find("table",class_="table table-bordered table-striped")
    lines = table.find("tbody").find_all("tr")
    data = []
    for i in lines:
        obs=i.find_all("td")
        if len(obs)<3:
            continue
        date = obs[0].get_text(strip=True)
        rawnumber = obs[1].get_text(" ", strip=True)
        match = re.search(r"\d+", rawnumber)
        number = match.group()
        location = obs[2].get_text(strip=True)
        data.append([date,number,location])
        if len(data)==10:
            break
        
    species_img = None
    img_tags = soup2.find_all("img")
    img_url = None
    for i in img_tags:
        src=i.get("src")
        if src.startswith("/media/photo/"):
            img_url="https://waarnemingen.be"+src
            break

    if img_url:
        response_img=requests.get(img_url)
        if response_img.status_code==200:
            species_img = IMAGES_DIR / f"{species}_img.jpg"
            with open(species_img,"wb") as f:
                for pic in response_img.iter_content(1024):
                    f.write(pic)
    
    full_species_informations = {
        "Name":species,
        "Latin Name":species,
        "Rarity Status(Dutch)":rarity_status_dutch,
        "Rarity Status(english)":rarity_status_english,
        "Description(Dutch)":description_in_dutch,
        "Description(English)":description_in_english,
        "Observation of the species in Namur": data,
        "image_path": str(species_img)
        
    }

    return full_species_informations
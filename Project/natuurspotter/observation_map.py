from bs4 import BeautifulSoup
import requests
import re
import folium
import time
import datetime
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from folium.plugins import MarkerCluster
import random
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()
DATA_DIR = BASE_DIR / "dataoutputs"
MAP_DIR = DATA_DIR / "maps"
MAP_DIR.mkdir(parents=True, exist_ok=True)

def observations_map(day=None):
    if day is None:
        day = datetime.datetime.now().strftime("%Y-%m-%d")
    url = f"https://waarnemingen.be/fieldwork/observations/daylist/?date={day}&species_group=16&country_division=24&rarity=&search="
    response = requests.get(url)
    soup=BeautifulSoup(response.text,"html.parser")
    data_table = soup.find("table",class_="table table-bordered table-striped")
    if not data_table:
        print("opps..No observation found",file=sys.stderr)
        return
    data_rows = data_table.find("tbody").find_all("tr")
    locator = Nominatim(user_agent="sadman")
    geocode = RateLimiter(locator.geocode)
    X = folium.Map(location=[50.4674,4.8718],zoom_start=9)
    cluster = MarkerCluster().add_to(X)
    color_for_species = {}

    for i in data_rows:
        data_col=i.find_all("td")
        if len(data_col)<5:
            continue
        species_namess=data_col[3]
        Common_name = species_namess.find("span", class_="species-common-name")
        scientific_name=species_namess.find("i",class_="species-scientific-name")
        if Common_name:
            name=Common_name.get_text(strip=True)
        elif scientific_name:
            name=scientific_name.get_text(strip=True)
        else:
            continue

        location = data_col[4]
        location_name=location.find_all("a")
        for i in location_name:
            raw_location=i.get_text(strip=True)
            clean_location=raw_location.split("(")[0].split(",")[0].strip()
            if name not in color_for_species:
                color_for_species[name] = "#{:06x}".format(random.randint(0, 0xFFFFFF))
            realLocation=geocode(clean_location+ ",Namur,Belgium")
            if not realLocation:
                continue
            folium.Marker(location=[realLocation.latitude,realLocation.longitude],popup=f"<b>{name}</b><br>{raw_location}</br>{day}",icon=folium.Icon(color=color_for_species[name],icon="smile",prefix="fa")).add_to(cluster)

    legend_html = """
        <div style="
            position: fixed;
            bottom: 50px;
            left: 50px;
            z-index: 9999;
            background-color: white;
            padding: 10px;
            border: 2px solid grey;
            font-size: 14px;
        ">
        <b>Species names</b><br>
        """

    for species, color in color_for_species.items():
            legend_html += f"""
            <i style="color:{color}">●</i> {species}<br>
            """

    legend_html += "</div>"
    X.get_root().html.add_child(folium.Element(legend_html))
    mapfilename = MAP_DIR / f"observation_map.html"
    X.save(mapfilename)
    return {
    "date": day,
    "map_file": str(mapfilename),
    "species_count": len(color_for_species),
    "species_colors": color_for_species
    }
import requests
from bs4 import BeautifulSoup
import re
import json
import datetime
import calendar
import plotly.express as px
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()
DATA_DIR = BASE_DIR / "dataoutputs"
PLOT_DIR = DATA_DIR / "plots"
PLOT_DIR.mkdir(parents=True, exist_ok=True)

def seasonal_analysis(species,year):
    headers = {"User-Agent":""}
    url="https://waarnemingen.be/species/search/"
    search_parameters={"q":species,"species_group":16}
    response = requests.get(url,params=search_parameters)
    soup = BeautifulSoup(response.text,"html.parser")
    new_url = soup.find("a",href=re.compile(r"^/species/\d+/$"))
    if not new_url:
        print("No species found")
        return
    species_url="https://waarnemingen.be"+new_url["href"]
    observation_url=f"{species_url}observations/?"
    date_parameters = {"date_after": f"{year}-01-01","date_before":f"{year}-12-31","country_division":24}
    new_response = requests.get(observation_url,params=date_parameters)
    soup1=BeautifulSoup(new_response.text,"html.parser")
    data_table = soup1.find("table",class_="table table-bordered table-striped")
    if "Geen resultaten" in data_table.get_text():
        print(f"No observations done in {year} for {species} in Namur",file=sys.stderr)
        return
    data_rows = data_table.find_all("tr")
    M_counts={i:0 for i in range(1,13)}
    seasons_with_months = {"Winter": [12, 1, 2],"Spring": [3, 4, 5],"Summer": [6, 7, 8],"Autumn": [9, 10, 11]}
    s_counts = {"Winter": 0,"Spring": 0,"Summer": 0,"Autumn": 0}

    for i in data_rows:
        data_cols=i.find_all("td")
        if not data_cols:
            continue
        date=data_cols[0].get_text(strip=True)[:10]
        realdate = datetime.datetime.strptime(date,"%Y-%m-%d")
        M_counts[realdate.month] += 1
    for i, j in seasons_with_months.items():
        for k in j:
            s_counts[i] += M_counts[k]
    
    months = list(M_counts.keys())
    count = list(M_counts.values())
    names_m=[]
    for i in months:
        names_m.append(calendar.month_abbr[i])
    
    fig_month = px.pie(
    names=names_m,
    values=count,
    title=f"Monthly observations of {species} ({year})"
    )
    fig_season = px.bar(
    x=list(s_counts.keys()),
    y=list(s_counts.values()),
    labels={"x": "Season", "y": "Observations"},
    title=f"Seasonal observations of {species} ({year})"
    )

    monthly_file = PLOT_DIR / f"Graph_seasonal.html"
    seasonal_file = PLOT_DIR / f"Graph_seasonal_bar.html"
    fig_month.write_html(monthly_file)
    fig_season.write_html(seasonal_file)

    low_season = min(s_counts,key=s_counts.get)
    explanations = explanation(species,low_season,year)
    return {
        "species": species,
        "year": int(year),
        "monthly_counts": M_counts,
        "seasonal_counts": s_counts,
        "lowest_season": low_season,
        "llm_explanation": explanations,
        "monthly_file": str(monthly_file),
        "seasonal_file": str(seasonal_file)
    }

#i am using ollama..a platform where i can install any llm locally..so that i dont have to pay for llm access cuz i mostly used the free trails before...i can use it ofr llm api
def explanation(species,low_season,year):
    text = f"Why {species} is less observed in the year of {year} during {low_season}.Explain it purely"
    url = "http://localhost:11434/api/generate"

    payload = {
    "model": "gemma3:1b",
    "prompt": text,
    "stream": False
    }
    r = requests.post(url, json=payload)
    data = r.json()
    explaination_data = data.get("response")
    return explaination_data
    
import requests
from bs4 import BeautifulSoup
import datetime
import csv
import calendar
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()
DATA_DIR = BASE_DIR / "dataoutputs"
CSV_DIR = DATA_DIR / "csv"
CSV_DIR.mkdir(parents=True, exist_ok=True)

def biodiversity_analysis(month=None, year=None):
    todays_date = datetime.date.today()
    if month is None:
        month = todays_date.month
    if year is None:
        year = todays_date.year
    
    MONTH_TO_NUMBER = {"january": 1,"february": 2,"march": 3,"april": 4,"may": 5,"june": 6,"july": 7,"august": 8,"september": 9,"october": 10,"november": 11,"december": 12}
    month_number = MONTH_TO_NUMBER[month.lower()]
    total_day_month = calendar.monthrange(int(year),month_number)[1]
    url = "https://waarnemingen.be/fieldwork/observations/daylist/"
    translation_cache = {}
    csv_rows = []
    total = 0
    species_counts = {} 
    for i in range(1,total_day_month+1):
        date = f"{year}-{month_number:02d}-{i:02d}"
        parameters = {"species_group":16,"country_division":24,"date":date}
        response = requests.get(url,params=parameters)
        soup = BeautifulSoup(response.text,"html.parser")
        data_table = soup.find("table",class_="table table-bordered table-striped")
        if "Geen resultaten" in data_table.get_text():
            continue
        data_row = data_table.find("tbody").find_all("tr")
        for i in data_row:
            data_cols = i.find_all("td")
            raw_name = data_cols[3].get_text()
            common_dutch = None
            scientific_name = None
            if " - " in raw_name:
                common_dutch, scientific_name = raw_name.split(" - ", 1)
            else:
                scientific_name = raw_name
            location = data_cols[4].get_text(strip=True)
            common_english = None
            if common_dutch:
                common_english = translation(common_dutch,translation_cache)
            if not common_english:
                common_english = scientific_name
            X = f"{common_english} ({scientific_name})"
            total += 1
            species_counts[X] = species_counts.get(X,0)+1
            csv_rows.append([
                date,
                common_dutch or "",
                common_english,
                scientific_name,
                location
            ])
    csv_file = CSV_DIR / f"biodiversity_analysis.csv"
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Date",
            "Common name (Dutch)",
            "Common name (English)",
            "Scientific name",
            "Location"
        ])
        writer.writerows(csv_rows)
    print(f"Species: {len(species_counts)} unique species",file=sys.stderr)
    print(f"Total observations: {total}",file=sys.stderr)
    print(f"CSV saved as: {csv_file}",file=sys.stderr)

    return {
    "month": month,
    "year": int(year),
    "total_observations": total,
    "unique_species_count": len(species_counts),
    "species_counts": species_counts,
    "csv_file": str(csv_file)
    }

    
def translation(english_name,cache):
    if not english_name:
        return None
    if english_name in cache:
        return cache[english_name]
    url = "https://api.mymemory.translated.net/get"
    params = {"q": english_name,"langpair": "nl|en"}
    e_response = requests.get(url,params=params) 
    data = e_response.json()["responseData"]["translatedText"]
    cache[english_name] = data
    return data

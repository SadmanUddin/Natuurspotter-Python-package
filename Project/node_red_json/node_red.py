import sys
import json
from natuurspotter.speciess_info import species_info
from natuurspotter.biodiversityy_analysis import biodiversity_analysis
from natuurspotter.observation_map import observations_map
from natuurspotter.seasonall_analysis import seasonal_analysis
from natuurspotter.pdf_generation import species_report

def main():
    raw = sys.stdin.read().strip()
    if not raw:
        print(json.dumps({"error": "No input received"}))
        return

    data = json.loads(raw)

    species = data.get("species")
    year = data.get("year")
    month = data.get("month")
    day = data.get("day")

    if not all([species, year, month, day]):
        print(json.dumps({"error": "Missing arguments"}))
        return

    result = {
        "species_info": species_info(species),
        "pdf": species_report(species),
        "seasonal_analysis": seasonal_analysis(species, year),
        "observation_map": observations_map(day),
        "biodiversity_analysis": biodiversity_analysis(month, year)
    }

    print(json.dumps(result))

if __name__ == "__main__":
    main()
# NatuurSpotter

NatuurSpotter is a Python-based biodiversity analysis package designed to analyze **Coleoptera (beetle) observations in Namur Province, Belgium**.
The system automatically collects biodiversity observation data, performs exploratory data analysis, generates visualizations and reports, and displays results through a **Node-RED dashboard**.
The project integrates **data scraping, biodiversity analytics, geospatial visualization, automated reporting, and LLM-based explanations**.

---

# Project Overview

NatuurSpotter functions as an automated biodiversity analysis pipeline:

1. Collect biodiversity observation data  
2. Analyze species observations and biodiversity metrics  
3. Generate CSV files, visualizations, maps, and PDF reports  
4. Display results through a Node-RED dashboard  

All generated outputs are stored inside the:

```
dataoutputs/
```

The Node-RED dashboard reads directly from this folder and updates automatically when the Python scripts are executed.

---

# Features

## Biodiversity Analysis

Computes biodiversity metrics such as:

- Total number of observations
- Number of unique species
- Rare species counts

Results are exported to CSV files and visualized in the dashboard.

---

## Seasonal Observation Analysis

Analyzes seasonal and monthly patterns of species observations.

Visualizations include:

- Plotly bar charts
- Monthly distribution graphs
- Seasonal observation patterns

---

## Species Information Extraction

The system gathers species information including:

- Dutch description
- English description
- Rarity status
- Observation history

Sources include public biodiversity and encyclopedia resources.

---

## Automatic Species Report Generation

Species reports are automatically generated as **PDF files** containing:

- Species descriptions
- Rarity status
- Observation statistics
- Images
- Observation history

---

## LLM-based Ecological Explanation

When observation counts are low during specific seasons, the system generates possible ecological explanations using a **local LLM model running with Ollama**.

The model is accessed through an API and provides contextual explanations.

---

## Observation Mapping

Observation locations are visualized using **Folium interactive maps**.

Maps are exported as HTML files and embedded in the dashboard.

---

# Node-RED Dashboard

The Node-RED dashboard visualizes the generated outputs.

Dashboard components include:

- Biodiversity statistics table
- Rare species table
- Species richness charts
- Observation maps
- Embedded PDF species reports

The dashboard automatically reads files from the `dataoutputs/` folder.

---

# Implemented Functions

The core functionality of the package is implemented through the following methods:

```
species_info(species)

observations_map(day=None)

seasonal_analysis(species, year)

biodiversity_analysis(month=None, year=None)

generate_species_pdf(
    species,
    latin_name,
    rarity_status_dutch,
    rarity_status_english,
    description_dutch,
    description_english,
    observations,
    image_path
)

species_report(species)

explanation(species, low_season, year)

translation(english_name, cache)
```

---

# Example Usage

Example usage from `run.py`:

```python
from natuurspotter.biodiversity_analysis import biodiversity_analysis
from natuurspotter.pdf_info import generate_species_pdf
from natuurspotter.observation_map import observations_map
from natuurspotter.seasonall_analysis import seasonal_analysis
from natuurspotter.speciess_info import species_info
from natuurspotter.pdf_generation import species_report

X = seasonal_analysis("Galerucella nymphaeae", "2021")

print(X["llm_explanation"])

species_report("Harmonia quadripunctata")

observations_map("2019-4-13")

biodiversity_analysis("april", "2019")
```

Running the script will:

1. Analyze seasonal observations for a species
2. Generate a species report
3. Produce an observation map
4. Perform biodiversity analysis for a selected period

All outputs are saved to the `dataoutputs/` directory.

---

# Input Requirements

## Species Input

Species names must always be provided using **Latin names**.

Example:

```
Galerucella nymphaeae
```

---

## Date Format

Dates must follow this format:

```
YYYY-M-D
```

Example:

```
2019-4-13
```

---

# Project Structure

```
NatuurSpotter
│
├── natuurspotter/
│   ├── biodiversity_analysis.py
│   ├── seasonal_analysis.py
│   ├── observation_map.py
│   ├── species_info.py
│   ├── pdf_generation.py
│
├── dataoutputs/
│   ├── csv/
│   ├── plots/
│   ├── maps/
│   └── pdf/
│
├── dashboard/
│   └── node-red-flow.json
│
├── run.py
└── README.md
```

---

# Data Sources

The project uses publicly available biodiversity data and species information from:

- Waarnemingen.be
- Wikipedia

Additional services include:

- Translation APIs
- Ollama local LLM for ecological explanations

---

# Technologies Used

Python libraries:

- pandas
- plotly
- folium
- requests

Other tools:

- Node-RED
- Ollama (local LLM)

---

# Purpose

The goal of this project is to explore biodiversity patterns in **Coleoptera species** and provide a reproducible system for biodiversity analysis and visualization.

The project demonstrates:

- biodiversity data analysis
- automated data pipelines
- geospatial visualization
- dashboard integration
- AI-assisted interpretation

---
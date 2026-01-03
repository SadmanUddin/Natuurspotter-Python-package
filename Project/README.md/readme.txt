NatuurSpotter is a Python-based biodiversity analysis package combined with a Node-RED dashboard to visualize Coleoptera observations in Namur Province, Belgium.

what the project automatically does:
-Collects biodiversity observation data
-Generates CSV files, maps, plots, and PDFs
-Visualizes results in a user-friendly Node-RED dashboard

properties of this package==
1.Species information scraping with Dutch and English descriptions with a pdf generation
2.analyze biodiversity with total observation ,unique species and counts rare species
3.analyze the seasons and months for species observation and visualizes them using ploty graphs and bar charts
4.Gives an llm based ans of why the species is less observed in specific season(I used local llm model using ollam and calling the llm through an api)
5.Folium observation map

Node-RED Dashboard:
-Biodiversity table (CSV-based)
-Rare species table
-Bar & pie charts (species richness)
-Embedded observation map
-Embedded PDF species report
-Fully automatic (reads from generated files in dataoutputs folder)

methods implemented:
-species_info(species)
-observations_map(day=None)
-seasonal_analysis(species,year)
-biodiversity_analysis(month=None, year=None)
-generate_species_pdf(species,latin_name,rarity_status_dutch,rarity_status_english,description_dutch,description_english,observations,image_path)
-species_report(species)
-explanation(species,low_season,year)
-translation(english_name,cache)

inputs:
1.species name always in latin name
2.date format in day input always in ("YYYY-M-D") format

The dashboard automatically reads files from dataoutputs/...No manual input is required...Visualizations update whenever Python is re-run.
--dataoutputs folder is the main folder from where i feed the dashboard

sources:
1.official belgium website (waarnemingen.be) and wikipedia
2.Api s for translation,names, llm explanations etc
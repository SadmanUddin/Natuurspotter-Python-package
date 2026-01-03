from natuurspotter.biodiversityy_analysis import biodiversity_analysis
from natuurspotter.pdf_info import generate_species_pdf
from natuurspotter.observation_map import observations_map
from natuurspotter.seasonall_analysis import seasonal_analysis
from natuurspotter.speciess_info import species_info
from natuurspotter.pdf_generation import species_report

X=seasonal_analysis("Galerucella nymphaeae","2021")
print(X["llm_explanation"])
species_report("Harmonia quadripunctata")
observations_map("2019-4-13")
biodiversity_analysis("april","2019")
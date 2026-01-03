from natuurspotter.speciess_info import species_info
from natuurspotter.pdf_info import generate_species_pdf

def species_report(species):

    info = species_info(species)

    pdf_result = generate_species_pdf(
        species=info["Name"],
        latin_name=info["Latin Name"],
        rarity_status_dutch=info["Rarity Status(Dutch)"],
        rarity_status_english=info["Rarity Status(english)"],
        description_dutch=info["Description(Dutch)"],
        description_english=info["Description(English)"],
        observations=info["Observation of the species in Namur"],
        image_path=info["image_path"]
    )

    return {
        "species_info": info,
        "pdf": pdf_result
    }
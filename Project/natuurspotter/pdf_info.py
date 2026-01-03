from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.styles import getSampleStyleSheet
import os
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()
DATA_DIR = BASE_DIR / "dataoutputs"
PDF_DIR = DATA_DIR / "pdf"
PDF_DIR.mkdir(parents=True, exist_ok=True)

def draw_page_border(c, width, height, margin=1.5*cm):
    c.setLineWidth(1)
    c.rect(
        margin,
        margin,
        width - 2*margin,
        height - 2*margin
    )

def generate_species_pdf(
    species,
    latin_name,
    rarity_status_dutch,
    rarity_status_english,
    description_dutch,
    description_english,
    observations,
    image_path
):
    pdf_file = PDF_DIR / f"Species_report.pdf"
    c = canvas.Canvas(str(pdf_file), pagesize=A4)
    width, height = A4

    margin = 1.5 * cm
    c.setLineWidth(1)
    c.rect(
        margin,
        margin,
        width - 2 * margin,
        height - 2 * margin
    )

    styles = getSampleStyleSheet()
    normal = styles["Normal"]
    heading = styles["Heading2"]
    header_top = height - margin - 0.5 * cm
    text_x = margin + 0.5 * cm

    c.setFont("Helvetica-Bold", 16)
    c.drawString(text_x, header_top, species)

    c.setFont("Helvetica", 11)
    c.drawString(text_x, header_top - 1.0 * cm, f"Latin name: {latin_name}")
    c.drawString(
        text_x,
        header_top - 1.7 * cm,
        f"Rarity (NL): {rarity_status_dutch}"
    )
    c.drawString(
        text_x,
        header_top - 2.4 * cm,
        f"Rarity (EN): {rarity_status_english}"
    )
    image_box = 4.5 * cm
    if image_path and os.path.exists(image_path):
        try:
            img = ImageReader(image_path)
            c.drawImage(
                img,
                width - margin - image_box,
                header_top - image_box,
                width=image_box,
                height=image_box,
                preserveAspectRatio=True,
                mask="auto"
            )
        except Exception:
            pass

    header_height = 5.5 * cm 
    frame = Frame(
        margin + 0.5 * cm,
        margin + 0.5 * cm,
        width - 2 * margin - 1 * cm,
        height - header_height - margin,
        showBoundary=0
    )

    story = []

    story.append(Paragraph("<b>Description (English)</b>", heading))
    story.append(Paragraph(description_english, normal))
    story.append(Paragraph("<br/>", normal))

    story.append(Paragraph("<b>Description (Dutch)</b>", heading))
    story.append(Paragraph(description_dutch, normal))
    story.append(Paragraph("<br/>", normal))

    story.append(Paragraph("<b>Recent observations in Namur</b>", heading))

    if observations:
        for date, number, location in observations:
            story.append(
                Paragraph(
                    f"<b>{date}</b> — {number} observed at {location}",
                    normal
                )
            )
    else:
        story.append(Paragraph("No observations available.", normal))

    frame.addFromList(story, c)

    c.save()
    print(f"PDF generated: {pdf_file}",file=sys.stderr)
    return {
    "pdf_file": str(pdf_file),
    "species": species,
    "image_used": image_path,
    "observations_count": len(observations) if observations else 0
    }
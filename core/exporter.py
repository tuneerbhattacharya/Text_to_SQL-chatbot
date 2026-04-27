from io import BytesIO
import pandas as pd
from reportlab.lib.pagesizes import landscape, letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


def export_csv(df: pd.DataFrame):
    return df.to_csv(index=False).encode("utf-8")


def export_pdf(df: pd.DataFrame, title="Analytics Report"):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
    styles = getSampleStyleSheet()
    elements = [Paragraph(title, styles["Title"]), Spacer(1, 12)]

    if df.empty:
        elements.append(Paragraph("No rows returned.", styles["Normal"]))
    else:
        preview = df.copy().head(50)
        data = [preview.columns.tolist()] + preview.astype(str).values.tolist()

        table = Table(data, repeatRows=1)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 7),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]))
        elements.append(table)

    doc.build(elements)
    buffer.seek(0)
    return buffer

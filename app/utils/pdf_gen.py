import io
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas


def generate_certificate_pdf(
    student_name: str, title: str, issued_at: str, cert_id: int
) -> bytes:
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=landscape(A4))
    w, h = landscape(A4)
    c.setFillColorRGB(0.039, 0.086, 0.157)
    c.rect(0, 0, w, h, fill=1, stroke=0)
    c.setStrokeColorRGB(0.788, 0.635, 0.294)
    c.setLineWidth(3)
    c.rect(1 * cm, 1 * cm, w - 2 * cm, h - 2 * cm, fill=0, stroke=1)
    c.setStrokeColorRGB(0.788, 0.635, 0.294)
    c.setLineWidth(1)
    c.rect(1.5 * cm, 1.5 * cm, w - 3 * cm, h - 3 * cm, fill=0, stroke=1)
    c.setFillColorRGB(0.788, 0.635, 0.294)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(w / 2, h - 3 * cm, "R O A N   A C A D E M Y")
    c.setFont("Helvetica-Bold", 40)
    c.setFillColorRGB(0.961, 0.937, 0.878)
    c.drawCentredString(w / 2, h - 5.5 * cm, "Certificate of Completion")
    c.setFont("Helvetica", 14)
    c.drawCentredString(w / 2, h - 7.5 * cm, "This is proudly presented to")
    c.setFont("Helvetica-BoldOblique", 32)
    c.setFillColorRGB(0.788, 0.635, 0.294)
    c.drawCentredString(w / 2, h - 9.5 * cm, student_name)
    c.setFont("Helvetica", 14)
    c.setFillColorRGB(0.961, 0.937, 0.878)
    c.drawCentredString(w / 2, h - 11 * cm, "for successfully completing")
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(w / 2, h - 12.5 * cm, title)
    c.setFont("Helvetica", 11)
    c.drawCentredString(
        w / 2,
        3 * cm,
        f"Issued on {issued_at}  ·  Certificate ID: ROAN-{cert_id:05d}",
    )
    c.setFont("Helvetica-Oblique", 10)
    c.drawCentredString(
        w / 2, 2.2 * cm, "Registrar, ROAN University of Applied Arts"
    )
    c.showPage()
    c.save()
    return buf.getvalue()


def generate_admit_card_pdf(
    student_name: str,
    student_email: str,
    exam_title: str,
    exam_date: str,
    venue: str,
    mode: str,
    student_id: int,
    exam_id: int,
) -> bytes:
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    w, h = A4
    c.setFillColorRGB(0.039, 0.086, 0.157)
    c.rect(0, 0, w, h, fill=1, stroke=0)
    c.setStrokeColorRGB(0.788, 0.635, 0.294)
    c.setLineWidth(2)
    c.rect(1 * cm, 1 * cm, w - 2 * cm, h - 2 * cm, fill=0, stroke=1)
    c.setFillColorRGB(0.788, 0.635, 0.294)
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(w / 2, h - 3 * cm, "ROAN — ADMIT CARD")
    c.setFillColorRGB(0.961, 0.937, 0.878)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(w / 2, h - 4.2 * cm, exam_title)

    y = h - 6 * cm
    line_h = 0.9 * cm

    def row(label: str, value: str, y: float) -> float:
        c.setFillColorRGB(0.788, 0.635, 0.294)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(2.5 * cm, y, label)
        c.setFillColorRGB(0.961, 0.937, 0.878)
        c.setFont("Helvetica", 12)
        c.drawString(6.5 * cm, y, value)
        return y - line_h

    y = row("Candidate:", student_name, y)
    y = row("Email:", student_email, y)
    y = row("Roll No:", f"ROAN-S-{student_id:05d}", y)
    y = row("Exam ID:", f"ROAN-E-{exam_id:05d}", y)
    y = row("Date:", exam_date, y)
    y = row("Mode:", mode, y)
    y = row("Venue:", venue, y)

    c.setStrokeColorRGB(0.788, 0.635, 0.294)
    c.line(2 * cm, y - 0.5 * cm, w - 2 * cm, y - 0.5 * cm)

    c.setFillColorRGB(0.961, 0.937, 0.878)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(2.5 * cm, y - 1.6 * cm, "Instructions:")
    c.setFont("Helvetica", 10)
    instructions = [
        "1. Report at the exam venue 30 minutes before the scheduled time.",
        "2. Carry a valid government-issued photo ID along with this admit card.",
        "3. Electronic devices are not allowed inside the examination hall.",
        "4. Follow examiner instructions at all times.",
        "5. This admit card is issued digitally and does not require a signature.",
    ]
    yy = y - 2.4 * cm
    for line in instructions:
        c.drawString(2.5 * cm, yy, line)
        yy -= 0.6 * cm

    c.setFont("Helvetica-Oblique", 9)
    c.setFillColorRGB(0.788, 0.635, 0.294)
    c.drawCentredString(
        w / 2,
        1.5 * cm,
        "Issued by ROAN Examinations · This is a computer-generated document.",
    )
    c.showPage()
    c.save()
    return buf.getvalue()

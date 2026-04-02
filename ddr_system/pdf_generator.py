from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
import datetime

# Color palette
NAVY = colors.HexColor("#1F4E79")
BLUE = colors.HexColor("#2E75B6")
LIGHT_BLUE = colors.HexColor("#D6E4F0")
RED = colors.HexColor("#C00000")
ORANGE = colors.HexColor("#E36C09")
GREEN = colors.HexColor("#375623")
GRAY = colors.HexColor("#888888")
LIGHT_GRAY = colors.HexColor("#F5F5F5")
WHITE = colors.white
BLACK = colors.black

SEV_COLORS = {
    "high": (RED, WHITE),
    "medium": (ORANGE, WHITE),
    "low": (GREEN, WHITE),
}

PRI_COLORS = {
    "immediate": RED,
    "short-term": ORANGE,
    "general maintenance": GREEN,
}


def get_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        "DDRTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=22,
        textColor=NAVY,
        alignment=TA_CENTER,
        spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        "DDRSub",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=9,
        textColor=GRAY,
        alignment=TA_CENTER,
        spaceAfter=16,
    ))
    styles.add(ParagraphStyle(
        "DDRHeading1",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=13,
        textColor=NAVY,
        spaceBefore=12,
        spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        "DDRHeading2",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        textColor=BLUE,
        spaceBefore=8,
        spaceAfter=3,
    ))
    styles.add(ParagraphStyle(
        "DDRBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        textColor=BLACK,
        spaceAfter=3,
        leading=15,
    ))
    styles.add(ParagraphStyle(
        "DDRBullet",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        textColor=BLACK,
        spaceAfter=2,
        leading=14,
        leftIndent=14,
        bulletIndent=4,
        bulletText="\u2022",
    ))
    styles.add(ParagraphStyle(
        "DDRImageNote",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=9,
        textColor=GRAY,
        alignment=TA_CENTER,
        spaceAfter=8,
        spaceBefore=4,
    ))
    styles.add(ParagraphStyle(
        "DDRTableHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        textColor=WHITE,
    ))
    styles.add(ParagraphStyle(
        "DDRTableCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        textColor=BLACK,
        leading=13,
    ))
    styles.add(ParagraphStyle(
        "DDRTableCellItalic",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=9.5,
        textColor=GRAY,
        leading=13,
    ))
    styles.add(ParagraphStyle(
        "DDRPriority",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        spaceAfter=3,
        spaceBefore=6,
    ))
    return styles


def divider():
    return HRFlowable(width="100%", thickness=1.5, color=BLUE, spaceAfter=6, spaceBefore=6)


def generate_pdf(report, output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=2.5 * cm,
        leftMargin=2.5 * cm,
        topMargin=2.5 * cm,
        bottomMargin=2.5 * cm,
    )

    S = get_styles()
    story = []

    # ── Title ──
    story.append(Paragraph("MAIN DETAILED DIAGNOSTIC REPORT", S["DDRTitle"]))
    story.append(Paragraph("Prepared by AI-Powered DDR Workflow System", S["DDRSub"]))

    # ── Property Info Table ──
    pi = report.get("property_info", {})
    info_data = [
        [Paragraph("<b>Property Address</b>", S["DDRTableCell"]), Paragraph(pi.get("address", "Not Available"), S["DDRTableCell"])],
        [Paragraph("<b>Inspection Date</b>", S["DDRTableCell"]), Paragraph(pi.get("inspection_date", "Not Available"), S["DDRTableCell"])],
        [Paragraph("<b>Report Date</b>", S["DDRTableCell"]), Paragraph(pi.get("report_date", datetime.date.today().strftime("%d %B %Y")), S["DDRTableCell"])],
        [Paragraph("<b>Property Type</b>", S["DDRTableCell"]), Paragraph(pi.get("property_type", "Not Available"), S["DDRTableCell"])],
        [Paragraph("<b>Inspector</b>", S["DDRTableCell"]), Paragraph(pi.get("inspector", "Not Available"), S["DDRTableCell"])],
        [Paragraph("<b>Client</b>", S["DDRTableCell"]), Paragraph(pi.get("client", "Not Available"), S["DDRTableCell"])],
    ]
    info_tbl = Table(info_data, colWidths=[5 * cm, 11.5 * cm])
    info_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), LIGHT_BLUE),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(info_tbl)
    story.append(Spacer(1, 10))
    story.append(divider())

    # ── 1. Property Issue Summary ──
    story.append(Paragraph("1. Property Issue Summary", S["DDRHeading1"]))
    story.append(Paragraph(report.get("property_issue_summary", "Not Available"), S["DDRBody"]))
    story.append(divider())

    # ── 2. Area-wise Observations ──
    story.append(Paragraph("2. Area-wise Observations", S["DDRHeading1"]))
    for area in report.get("area_wise_observations", []):
        area_items = []
        area_items.append(Paragraph(area.get("area", "Area"), S["DDRHeading2"]))
        for obs in area.get("observations", []):
            area_items.append(Paragraph(f"\u2022 {obs}", S["DDRBullet"]))
        thermal = area.get("thermal_findings", [])
        if thermal:
            area_items.append(Paragraph("<b>Thermal Findings:</b>", S["DDRBody"]))
            for t in thermal:
                area_items.append(Paragraph(f"\u2022 {t}", S["DDRBullet"]))
        for img in area.get("images", []):
            na = not img or "not available" in str(img).lower()
            area_items.append(Paragraph(
                "[ Image Not Available ]" if na else f"[ Image: {img} ]",
                S["DDRImageNote"]
            ))
        story.append(KeepTogether(area_items))
    story.append(divider())

    # ── 3. Probable Root Causes ──
    story.append(Paragraph("3. Probable Root Causes", S["DDRHeading1"]))
    for cause in report.get("probable_root_causes", ["Not Available"]):
        story.append(Paragraph(f"\u2022 {cause}", S["DDRBullet"]))
    story.append(divider())

    # ── 4. Severity Assessment ──
    story.append(Paragraph("4. Severity Assessment", S["DDRHeading1"]))
    sev_data = report.get("severity_assessment", [])
    if sev_data:
        header = [
            Paragraph("Area / Issue", S["DDRTableHeader"]),
            Paragraph("Severity", S["DDRTableHeader"]),
            Paragraph("Reasoning", S["DDRTableHeader"]),
        ]
        rows = [header]
        styles_cmd = [
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9.5),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 7),
            ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ]
        for i, s in enumerate(sev_data):
            lvl = s.get("severity", "Low").lower()
            bg, fg = SEV_COLORS.get(lvl, (GREEN, WHITE))
            rows.append([
                Paragraph(f"{s.get('issue','')} ({s.get('area','')})", S["DDRTableCell"]),
                Paragraph(f"<b>{s.get('severity','Low')}</b>", ParagraphStyle(
                    "sev", parent=S["DDRTableCell"], textColor=WHITE, fontName="Helvetica-Bold", alignment=TA_CENTER
                )),
                Paragraph(s.get("reasoning", ""), S["DDRTableCell"]),
            ])
            styles_cmd.append(("BACKGROUND", (1, i + 1), (1, i + 1), bg))
        tbl = Table(rows, colWidths=[4.5 * cm, 2.2 * cm, 9.8 * cm])
        tbl.setStyle(TableStyle(styles_cmd))
        story.append(tbl)
    story.append(divider())

    # ── 5. Recommended Actions ──
    story.append(Paragraph("5. Recommended Actions", S["DDRHeading1"]))
    groups = {}
    for a in report.get("recommended_actions", []):
        grp = a.get("priority", "General Maintenance")
        groups.setdefault(grp, []).append(a.get("action", ""))
    counter = 1
    for grp in ["Immediate", "Short-term", "General Maintenance"]:
        items = groups.get(grp, [])
        if not items:
            continue
        col = PRI_COLORS.get(grp.lower(), BLACK)
        p = Paragraph(grp.upper(), ParagraphStyle(
            "pri", parent=S["DDRPriority"], textColor=col
        ))
        story.append(p)
        for item in items:
            story.append(Paragraph(f"{counter}. {item}", S["DDRBullet"]))
            counter += 1
    story.append(divider())

    # ── 6. Additional Notes ──
    story.append(Paragraph("6. Additional Notes", S["DDRHeading1"]))
    for note in report.get("additional_notes", ["Not Available"]):
        story.append(Paragraph(f"\u2022 {note}", S["DDRBullet"]))
    conflicts = report.get("conflicts", [])
    if conflicts:
        story.append(Paragraph("<b>Conflicts Between Documents:</b>",
                               ParagraphStyle("conf", parent=S["DDRBody"], textColor=ORANGE)))
        for c in conflicts:
            story.append(Paragraph(f"\u2022 {c}", S["DDRBullet"]))
    story.append(divider())

    # ── 7. Missing or Unclear Information ──
    story.append(Paragraph("7. Missing or Unclear Information", S["DDRHeading1"]))
    missing = report.get("missing_or_unclear_information", [])
    if missing:
        header = [
            Paragraph("Item", S["DDRTableHeader"]),
            Paragraph("Status", S["DDRTableHeader"]),
        ]
        rows = [header]
        for m in missing:
            rows.append([
                Paragraph(m.get("item", ""), S["DDRTableCell"]),
                Paragraph(m.get("status", "Not Available"), S["DDRTableCellItalic"]),
            ])
        tbl3 = Table(rows, colWidths=[6 * cm, 10.5 * cm])
        tbl3.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("FONTSIZE", (0, 0), (-1, -1), 9.5),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 7),
            ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ]))
        story.append(tbl3)
    else:
        story.append(Paragraph("None identified.", S["DDRBody"]))

    story.append(Spacer(1, 20))
    story.append(Paragraph("— END OF REPORT —", ParagraphStyle(
        "end", parent=S["DDRBody"], textColor=GRAY, alignment=TA_CENTER, fontName="Helvetica-Bold"
    )))

    doc.build(story)

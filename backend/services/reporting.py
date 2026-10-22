import os
import csv
import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

REPORTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

def generate_pdf_report(investigation: dict) -> str:
    inv_id = investigation["id"]
    inv_type = investigation["inv_type"]
    target = investigation["target"]
    timestamp = investigation["timestamp"]
    data = investigation.get("data", {})
    
    filename = f"TRACE_Report_{inv_type}_{target}_{inv_id}.pdf"
    file_path = os.path.join(REPORTS_DIR, filename)
    
    doc = SimpleDocTemplate(
        file_path,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    
    usable_width = 595.27 - 72
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#0f172a')
    )
    
    sub_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=14,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#0284c7')
    )

    section_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=colors.HexColor('#1e40af'),
        spaceBefore=10,
        spaceAfter=5
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#334155')
    )

    table_header = ParagraphStyle(
        'TH',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=10.5,
        textColor=colors.white,
        alignment=TA_CENTER
    )
    
    table_cell = ParagraphStyle(
        'TC',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#1e293b')
    )
    
    table_cell_bold = ParagraphStyle(
        'TCB',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#0f172a')
    )

    story = []
    
    # 1. Header Banner
    story.append(Paragraph("TRACE — OSINT DIGITAL FOOTPRINT ANALYZER", title_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Formal Academic Investigation &amp; Technical Findings Report", sub_style))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0284c7"), spaceAfter=14))
    
    # 2. Academic Project Metadata Box
    meta_data = [
        [Paragraph("<b>Student Name:</b>", table_cell_bold), Paragraph("Fardeen Akmal (Roll No: 2)", table_cell)],
        [Paragraph("<b>Branch:</b>", table_cell_bold), Paragraph("Computer Science &amp; Engineering (IoT, Cyber Security and Blockchain Technology)", table_cell)],
        [Paragraph("<b>Project Guide:</b>", table_cell_bold), Paragraph("Prof. Akanksha Thakare", table_cell)],
        [Paragraph("<b>Institute:</b>", table_cell_bold), Paragraph("G.V. Acharya Institute of Engineering and Technology, University of Mumbai", table_cell)],
        [Paragraph("<b>Target Investigated:</b>", table_cell_bold), Paragraph(f"<b>{target}</b> (Type: {inv_type.upper()})", table_cell)],
        [Paragraph("<b>Investigation Date:</b>", table_cell_bold), Paragraph(timestamp, table_cell)],
    ]
    meta_table = Table(meta_data, colWidths=[130, usable_width - 130])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8fafc')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 12))
    
    # 3. Investigation Findings
    if inv_type == "username":
        story.append(Paragraph("Username Reconnaissance Findings:", section_style))
        findings = data.get("findings", [])
        
        headers = ["Source Platform", "Category", "Profile URL", "Status", "Response / Detail"]
        rows = [[Paragraph(h, table_header) for h in headers]]
        
        for f in findings:
            status_col = "#15803d" if f["status"] == "FOUND" else ("#b91c1c" if f["status"] == "NOT_FOUND" else "#b45309")
            rows.append([
                Paragraph(f["source"], table_cell_bold),
                Paragraph(f["category"], table_cell),
                Paragraph(f["url"], table_cell),
                Paragraph(f"<font color='{status_col}'><b>{f['status']}</b></font>", table_cell),
                Paragraph(f["detail"], table_cell)
            ])
            
        t = Table(rows, colWidths=[75, 80, 150, 75, 143.27])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#94a3b8')),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ]))
        story.append(t)
        
    elif inv_type == "domain":
        story.append(Paragraph("Domain Intelligence &amp; Infrastructure Findings:", section_style))
        dns_recs = data.get("dns_records", {})
        reg = data.get("registration", {})
        geo = data.get("geolocation", {})
        
        domain_rows = [
            [Paragraph("Target Domain", table_cell_bold), Paragraph(target, table_cell)],
            [Paragraph("Primary IPv4 Address", table_cell_bold), Paragraph(data.get("primary_ip", "N/A"), table_cell)],
            [Paragraph("Registrar", table_cell_bold), Paragraph(reg.get("registrar", "N/A"), table_cell)],
            [Paragraph("Creation Date", table_cell_bold), Paragraph(reg.get("creation_date", "N/A"), table_cell)],
            [Paragraph("Expiration Date", table_cell_bold), Paragraph(reg.get("expiration_date", "N/A"), table_cell)],
            [Paragraph("Server Geolocation", table_cell_bold), Paragraph(f"{geo.get('city', 'N/A')}, {geo.get('country', 'N/A')} (ISP: {geo.get('isp', 'N/A')})", table_cell)],
            [Paragraph("Autonomous System (ASN)", table_cell_bold), Paragraph(geo.get("asn", "N/A"), table_cell)],
            [Paragraph("Authoritative Nameservers", table_cell_bold), Paragraph(", ".join(dns_recs.get("NS", [])[:3]) or "None", table_cell)],
            [Paragraph("Mail Servers (MX)", table_cell_bold), Paragraph(", ".join(dns_recs.get("MX", [])[:3]) or "None", table_cell)],
            [Paragraph("SPF TXT Records", table_cell_bold), Paragraph("Configured (v=spf1)" if any("v=spf1" in x for x in dns_recs.get("TXT", [])) else "Not found", table_cell)],
        ]
        dt = Table(domain_rows, colWidths=[150, usable_width - 150])
        dt.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#ffffff')),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(dt)
        
    story.append(Spacer(1, 14))
    
    # 4. Limitations & Ethical Notice
    story.append(Paragraph("Investigation Limitations &amp; Ethical Statement:", section_style))
    story.append(Paragraph(
        "<b>Notice:</b> This investigation was conducted using passive, public OSINT techniques strictly within authorized educational and ethical parameters. "
        "No active scanning, intrusion, or unauthorized access was attempted. Rate limiting, WAF challenges, or private profiles may result in inconclusive findings. "
        "Information is provided 'as observed' at the collection timestamp without modification.",
        body_style
    ))
    
    doc.build(story)
    return file_path

def generate_csv_report(investigation: dict) -> str:
    inv_id = investigation["id"]
    inv_type = investigation["inv_type"]
    target = investigation["target"]
    data = investigation.get("data", {})
    
    filename = f"TRACE_Report_{inv_type}_{target}_{inv_id}.csv"
    file_path = os.path.join(REPORTS_DIR, filename)
    
    with open(file_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["TRACE OSINT INVESTIGATION REPORT"])
        writer.writerow(["Student", "Fardeen Akmal (Roll No: 2)"])
        writer.writerow(["Guide", "Akanksha Thakare"])
        writer.writerow(["Institute", "G.V. Acharya Institute of Engineering and Technology, University of Mumbai"])
        writer.writerow(["Target", target])
        writer.writerow(["Type", inv_type])
        writer.writerow(["Timestamp", investigation["timestamp"]])
        writer.writerow([])
        
        if inv_type == "username":
            writer.writerow(["Source", "Category", "URL", "Status", "Verified", "Response Time (ms)", "Detail"])
            for item in data.get("findings", []):
                writer.writerow([
                    item.get("source"),
                    item.get("category"),
                    item.get("url"),
                    item.get("status"),
                    item.get("verified"),
                    item.get("response_time_ms"),
                    item.get("detail")
                ])
        elif inv_type == "domain":
            writer.writerow(["Attribute", "Value"])
            writer.writerow(["Primary IP", data.get("primary_ip")])
            reg = data.get("registration", {})
            writer.writerow(["Registrar", reg.get("registrar")])
            writer.writerow(["Creation Date", reg.get("creation_date")])
            writer.writerow(["Expiration Date", reg.get("expiration_date")])
            geo = data.get("geolocation", {})
            writer.writerow(["Location", f"{geo.get('city')}, {geo.get('country')}"])
            writer.writerow(["ISP / ASN", f"{geo.get('isp')} / {geo.get('asn')}"])
            dns_recs = data.get("dns_records", {})
            for rtype, vals in dns_recs.items():
                writer.writerow([f"DNS_{rtype}", "; ".join(vals)])
                
    return file_path

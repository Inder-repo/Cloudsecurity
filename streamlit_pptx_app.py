# Streamlit app to generate and download a PDF presentation for Cloud Security Transformation with CCSP
# Prerequisites: Install dependencies (pip install -r requirements.txt)
# Usage: Save as streamlit_pdf_app.py, run with `streamlit run streamlit_pdf_app.py`, open http://localhost:8501,
# click "Generate and Download PDF" to create and download cloud_security_ccsp.pdf

import streamlit as st
import io
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.lib.colors import HexColor

try:
    from reportlab.lib import colors
except ImportError:
    st.error("The 'reportlab' library is not installed. Install it by running: `pip install reportlab==4.2.2`")
    st.error("If using Python 3, try: `pip3 install reportlab==4.2.2`")
    st.error("For virtual environments, activate the environment first.")
    st.error("For permission issues, try: `pip install reportlab==4.2.2 --user`")
    st.stop()

# Define colors to match HTML
PRIMARY_BLUE = HexColor("#667eea")
ACCENT_RED = HexColor("#f5576c")
GREEN = HexColor("#28a745")
PURPLE = HexColor("#764ba2")
GRAY = HexColor("#f8f9fa")
DARK_GRAY = HexColor("#2c3e50")
WHITE = colors.white

# Styles
styles = getSampleStyleSheet()
title_style = ParagraphStyle('Title', parent=styles['Title'], fontSize=24, textColor=PRIMARY_BLUE, spaceAfter=12, alignment=1)
subtitle_style = ParagraphStyle('Subtitle', parent=styles['Normal'], fontSize=12, textColor=WHITE, spaceAfter=12, alignment=1)
body_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=10, textColor=DARK_GRAY, spaceAfter=8, leading=12)
mono_style = ParagraphStyle('Mono', parent=styles['Code'], fontSize=8, textColor=DARK_GRAY, fontName='Courier', spaceAfter=8, alignment=1)

# Helper function to create a slide
def create_slide(doc, title, content, graphics=None, subtitle=None):
    elements = []
    elements.append(Paragraph(title, title_style))
    if subtitle:
        table = Table([[Paragraph(subtitle, subtitle_style)]], colWidths=[6*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), ACCENT_RED),
            ('BOX', (0,0), (-1,-1), 1, PRIMARY_BLUE),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph(content, body_style))
    if graphics:
        elements.extend(graphics)
    elements.append(Spacer(1, 0.3*inch))
    doc.build(elements)

# Function to create the bar chart for Slide 7
def create_bar_chart():
    drawing = Drawing(4*inch, 2*inch)
    data = [
        (100, 90, 95, 100),  # Compliance
        (0, 90, 80, 90),     # Attack Surface Reduction
        (0, 0, 80, 80),      # MTTD Reduction
        (0, 0, 75, 75)       # MTTR Improvement
    ]
    bc = VerticalBarChart()
    bc.x = 0
    bc.y = 0
    bc.height = 1.8*inch
    bc.width = 3.8*inch
    bc.data = data
    bc.categoryAxis.categoryNames = ['Planning', 'Implementation', 'Optimization', 'Overall']
    bc.categoryAxis.labels.fontSize = 8
    bc.valueAxis.valueMin = 0
    bc.valueAxis.valueMax = 100
    bc.valueAxis.labels.fontSize = 8
    bc.bars[0].fillColor = PRIMARY_BLUE
    bc.bars[1].fillColor = ACCENT_RED
    bc.bars[2].fillColor = GREEN
    bc.bars[3].fillColor = PURPLE
    drawing.add(bc)
    return drawing

# Function to create stats grid for Slide 1
def create_stats_grid():
    stats = [
        ("High", "Cost of breaches"),
        ("Critical", "Multi-cloud governance"),
        ("Strategic", "CCSP-driven resilience")
    ]
    data = [[Paragraph(f"{num}<br/>{desc}", ParagraphStyle('Stats', fontSize=10, textColor=WHITE, alignment=1))
             for num, desc in stats]]
    table = Table(data, colWidths=[1.5*inch]*3)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), PURPLE),
        ('BOX', (0,0), (-1,-1), 1, PRIMARY_BLUE),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('INNERGRID', (0,0), (-1,-1), 0.5, PRIMARY_BLUE),
    ]))
    return table

# Function to generate the PDF
def generate_pdf():
    pdf_file = "cloud_security_ccsp.pdf"
    doc = SimpleDocTemplate(pdf_file, pagesize=letter)

    # Slide 1: Welcome & Introduction
    story = []
    story.append(Paragraph("Cloud Security Transformation with CCSP", title_style))
    story.append(Table([[Paragraph("Securing the Cloud Journey<br/><br/>Cloud adoption fuels innovation, but security risks like misconfigurations, API vulnerabilities, and compliance gaps threaten enterprises. CCSP equips all levels—beginners to advanced professionals—to build resilient, compliant multi-cloud systems.", subtitle_style)]], colWidths=[6*inch], rowHeights=[1.5*inch], style=TableStyle([('BACKGROUND', (0,0), (-1,-1), ACCENT_RED), ('BOX', (0,0), (-1,-1), 1, PRIMARY_BLUE), ('ALIGN', (0,0), (-1,-1), 'CENTER')])))
    story.append(Spacer(1, 0.2*inch))
    story.append(create_stats_grid())
    doc.build(story)
    story = []

    # Slide 2: Cloud vs. On-Premises Risks
    story.append(Paragraph("Cloud vs. On-Premises Risks", title_style))
    story.append(Paragraph("Basic and Advanced Risk Analysis<br/>"
                          "<b>Cloud-Specific Risks:</b><br/>"
                          "• Basic: Shared responsibility confusion (e.g., AWS S3 settings); multi-tenancy risks.<br/>"
                          "• Advanced: Inconsistent multi-cloud governance; API vulnerabilities (e.g., Lambda).<br/>"
                          "• Examples: 2018 S3 leak (basic); 2020 Twilio API breach (advanced).<br/>"
                          "• Implications: Beginners—Learn roles. Intermediate—Use CSPM. Advanced—Standardize (Domain 1).<br/><br/>"
                          "<b>On-Premises Risks:</b><br/>"
                          "• Basic: Physical vulnerabilities; unpatched legacy systems.<br/>"
                          "• Advanced: Limited DR redundancy; manual governance.<br/>"
                          "• Examples: Equifax 2017 (basic); outdated servers (advanced).<br/>"
                          "• Implications: Beginners—Patch. Intermediate—Automate backups. Advanced—Hybrid monitoring (Domain 5).<br/><br/>"
                          "<b>Shared Risks:</b><br/>"
                          "• Basic: Data breaches; insider threats.<br/>"
                          "• Advanced: APTs; global compliance (GDPR, CCPA).<br/>"
                          "• Examples: Target 2013 (basic); 2021 SolarWinds (advanced).<br/>"
                          "• Implications: Beginners—Basic controls. Intermediate—SIEM. Advanced—Hybrid (Domains 1, 5).", body_style))
    story.append(Table([[Paragraph("[Cloud Risks]         [Shared Risks]         [On-Prem Risks]<br/>"
                                  " | S3 Misconfig |----| Breaches, APTs |----| Legacy Systems |<br/>"
                                  " | APIs, Shadow IT|----| Insider, Compliance|----| Physical, Manual |<br/>"
                                  " | Domain 1, 4   |----| Domain 1, 5    |----| Domain 5        |", mono_style)]],
                       colWidths=[6*inch], style=TableStyle([('BACKGROUND', (0,0), (-1,-1), GRAY), ('BOX', (0,0), (-1,-1), 1, PRIMARY_BLUE), ('ALIGN', (0,0), (-1,-1), 'CENTER')])))
    doc.build(story)
    story = []

    # Slide 3: Interactive Poll (Static)
    story.append(Paragraph("Your Biggest Cloud Security Concern", title_style))
    story.append(Paragraph("Prioritize Challenges for All Levels<br/><br/>"
                          "<b>Misconfigured Services (Domain 1):</b><br/>"
                          "• Impact: Exposed data due to improper settings.<br/>"
                          "• Example: 2018 S3 bucket leak.<br/>"
                          "• Implications: Beginners—Check defaults. Intermediate—AWS Config. Advanced—Automate audits.<br/><br/>"
                          "<b>Lack of Visibility (Domain 5):</b><br/>"
                          "• Impact: Delayed threat detection.<br/>"
                          "• Example: Target 2013 breach.<br/>"
                          "• Implications: Beginners—Learn monitoring. Intermediate—Splunk. Advanced—UEBA (Sentinel).<br/><br/>"
                          "<b>Multi-Cloud Governance (Domain 1):</b><br/>"
                          "• Impact: Inconsistent policies.<br/>"
                          "• Example: 2019 Capital One IAM.<br/>"
                          "• Implications: Beginners—Learn governance. Intermediate—AWS Organizations. Advanced—Standardize.<br/><br/>"
                          "<b>API and Serverless Security (Domain 4):</b><br/>"
                          "• Impact: Exposed endpoints.<br/>"
                          "• Example: 2020 Twilio API breach.<br/>"
                          "• Implications: Beginners—API basics. Intermediate—OAuth. Advanced—API Gateway.", body_style))
    doc.build(story)
    story = []

    # Slide 4: Key Security Challenges
    story.append(Paragraph("Key Security Challenges in Cloud", title_style))
    story.append(Paragraph("Basic and Advanced CCSP Mitigations<br/><br/>"
                          "1. <b>Shared Responsibility Confusion:</b><br/>"
                          "• Issue: Misunderstanding roles. Example: 2018 S3 leak.<br/>"
                          "• Domains: 1 (Responsibility), 5 (Configuration).<br/>"
                          "• Mitigation: Basic—Domain 1 matrix. Intermediate—AWS Config. Advanced—Azure Policy.<br/><br/>"
                          "2. <b>Multi-Cloud Governance:</b><br/>"
                          "• Issue: Inconsistent policies. Example: Capital One 2019.<br/>"
                          "• Domains: 1, 5.<br/>"
                          "• Mitigation: Basic—Learn governance. Intermediate—AWS Organizations. Advanced—ServiceNow GRC.<br/><br/>"
                          "3. <b>Data Loss and Leakage:</b><br/>"
                          "• Issue: Exposed data. Example: 2018 voter leak.<br/>"
                          "• Domains: 2 (Encryption), 3 (Storage).<br/>"
                          "• Mitigation: Basic—Encrypt. Intermediate—AWS Macie. Advanced—Vault.<br/><br/>"
                          "4. <b>API and Serverless Security:</b><br/>"
                          "• Issue: Exposed endpoints. Example: 2020 Twilio.<br/>"
                          "• Domains: 2, 4.<br/>"
                          "• Mitigation: Basic—OAuth. Intermediate—API Gateway. Advanced—Snyk.<br/><br/>"
                          "5. <b>Visibility and Threat Detection:</b><br/>"
                          "• Issue: Delayed detection. Example: 2021 SolarWinds.<br/>"
                          "• Domains: 3, 5.<br/>"
                          "• Mitigation: Basic—Monitoring. Intermediate—Splunk. Advanced—Cortex XSOAR.", body_style))
    doc.build(story)
    story = []

    # Slide 5: CCSP Domains Overview
    story.append(Paragraph("CCSP Domains for Transformation", title_style))
    story.append(Paragraph("Six Pillars for All Levels<br/><br/>"
                          "1. <b>Cloud Concepts, Architecture & Design:</b><br/>"
                          "• Principle: Align models with business needs.<br/>"
                          "• Example: Netflix hybrid (advanced); IaaS/PaaS (basic).<br/>"
                          "• Tools: Beginner—AWS Config. Advanced—AWS Organizations, Azure Policy.<br/><br/>"
                          "2. <b>Cloud Data Security:</b><br/>"
                          "• Principle: Protect data with encryption, DLP.<br/>"
                          "• Example: Dropbox AES-256 (basic); Vault (advanced).<br/>"
                          "• Tools: AWS KMS, Vault.<br/><br/>"
                          "3. <b>Cloud Platform & Infrastructure Security:</b><br/>"
                          "• Principle: Secure networks, containers.<br/>"
                          "• Example: VPC (basic); Kubernetes with Istio (advanced).<br/>"
                          "• Tools: AWS VPC, Istio.<br/><br/>"
                          "4. <b>Cloud Application Security:</b><br/>"
                          "• Principle: Embed security in apps.<br/>"
                          "• Example: Secure coding (basic); Snyk with GitHub Actions (advanced).<br/>"
                          "• Tools: Code reviews, Snyk.<br/><br/>"
                          "5. <b>Cloud Security Operations:</b><br/>"
                          "• Principle: Automate monitoring, response.<br/>"
                          "• Example: Splunk (basic); Cortex XSOAR (advanced).<br/>"
                          "• Tools: Splunk, XSOAR.<br/><br/>"
                          "6. <b>Legal, Risk & Compliance:</b><br/>"
                          "• Principle: Ensure compliance.<br/>"
                          "• Example: GDPR checks (basic); OneTrust (advanced).<br/>"
                          "• Tools: Manual audits, OneTrust.", body_style))
    doc.build(story)
    story = []

    # Slide 6: Best Practices
    story.append(Paragraph("Best Practices for Secure Cloud Adoption", title_style))
    story.append(Paragraph("Phased Approach for All Levels<br/><br/>"
                          "<b>Phase 1: Assessment (Domain 1, 6):</b><br/>"
                          "• Action: Inventory assets; establish multi-cloud governance.<br/>"
                          "• Tools: Beginner—AWS Config. Advanced—ServiceNow GRC, AWS Organizations.<br/>"
                          "• Example: Retailer used Config; bank standardized policies.<br/><br/>"
                          "<b>Phase 2: Implementation (Domain 2, 3, 4):</b><br/>"
                          "• Action: Deploy encryption, RBAC, DevSecOps.<br/>"
                          "• Tools: Beginner—AWS KMS, Okta. Advanced—Vault, Istio, Snyk.<br/>"
                          "• Example: Tech firm used Okta; fintech secured serverless.<br/><br/>"
                          "<b>Phase 3: Operations (Domain 5):</b><br/>"
                          "• Action: Automate monitoring, incident response.<br/>"
                          "• Tools: Beginner—Splunk. Advanced—Cortex XSOAR, Sentinel.<br/>"
                          "• Example: Healthcare used Splunk; enterprise reduced MTTD by 80%.", body_style))
    story.append(Table([[Paragraph("Key Tools: CASB, CSPM, SOAR, GRC<br/>Goal: Compliant, Secure Operations", ParagraphStyle('Goal', fontSize=10, textColor=WHITE, alignment=1))]],
                       colWidths=[6*inch], style=TableStyle([('BACKGROUND', (0,0), (-1,-1), GREEN), ('BOX', (0,0), (-1,-1), 1, PRIMARY_BLUE), ('ALIGN', (0,0), (-1,-1), 'CENTER')])))
    doc.build(story)
    story = []

    # Slide 7: Detailed Case Study with Chart
    story.append(Paragraph("Case Study: Multi-Cloud Financial Transformation", title_style))
    story.append(Paragraph("Securing 300+ Apps Across AWS, Azure, GCP<br/><br/>"
                          "<b>Context:</b> Global financial firm migrated 300+ apps to multi-cloud under SOX, PCI DSS, GDPR, CCPA.<br/><br/>"
                          "<b>Stage 1: Planning (Domains 1, 6):</b><br/>"
                          "• Requirements: 1M+ transactions; 100% visibility.<br/>"
                          "• Risks: Basic—Shared responsibility (e.g., 2018 S3). Advanced—Governance (e.g., 2019 Capital One).<br/>"
                          "• Security: Basic—Domain 1 matrix. Intermediate—AWS Config. Advanced—AWS Organizations, ServiceNow GRC.<br/>"
                          "• Outcome: <b>100% visibility</b>; GDPR readiness.<br/>"
                          "• Tools: AWS Config, Organizations, ServiceNow GRC.<br/><br/>"
                          "<b>Stage 2: Implementation (Domains 2, 3, 4):</b><br/>"
                          "• Requirements: Secure 1PB+ data, 200+ serverless apps; zero-trust.<br/>"
                          "• Risks: Basic—S3 misconfigs (e.g., 2018 voter). Advanced—API gaps (e.g., 2020 Twilio).<br/>"
                          "• Security: Basic—KMS, VPCs. Intermediate—Macie, API Gateway. Advanced—Vault, Istio, Snyk.<br/>"
                          "• Outcome: <b>90% attack surface reduction</b>; zero-trust apps.<br/>"
                          "• Tools: KMS, Macie, API Gateway, Vault, Istio, Snyk.<br/><br/>"
                          "<b>Stage 3: Optimization (Domain 5):</b><br/>"
                          "• Requirements: MTTD <24h, MTTR <12h; automate compliance.<br/>"
                          "• Risks: Basic—Visibility (e.g., Target 2013). Advanced—APTs (e.g., 2021 SolarWinds).<br/>"
                          "• Security: Basic—Splunk. Intermediate—Sentinel. Advanced—XSOAR.<br/>"
                          "• Outcome: <b>MTTD <24h</b>; <b>75% MTTR improvement</b>.<br/>"
                          "• Tools: Splunk, Sentinel, XSOAR.<br/><br/>"
                          "<b>Results (All Domains):</b><br/>"
                          "• Impact: Resilient, compliant multi-cloud architecture.", body_style))
    story.append(Spacer(1, 0.2*inch))
    story.append(create_bar_chart())
    story.append(Table([[Paragraph("[Multi-Cloud Architecture]<br/>"
                                  " | AWS (Config, KMS) |----| Azure (Sentinel, Policy) |----| GCP (RBAC, GRC) |<br/>"
                                  " | Stage 1: Governance|----| Stage 2: Zero-Trust |----| Stage 3: SOAR     |<br/>"
                                  " | Vault, Istio, Snyk |----| XSOAR, Compliance   |----| API Gateway       |<br/>"
                                  " | Domain 1,2,3,4,5,6 |", mono_style)]],
                       colWidths=[6*inch], style=TableStyle([('BACKGROUND', (0,0), (-1,-1), GRAY), ('BOX', (0,0), (-1,-1), 1, PRIMARY_BLUE), ('ALIGN', (0,0), (-1,-1), 'CENTER')])))
    doc.build(story)
    story = []

    # Slide 8: Interactive Quiz (Static)
    story.append(Paragraph("Test Your CCSP Knowledge", title_style))
    story.append(Paragraph("<b>Question 1: Who secures data in AWS S3? (Domain 1)</b><br/>"
                          "• Options: AWS Only, Customer, Both Equally<br/>"
                          "• Correct: <b>Customer</b>. The customer secures S3 data.<br/><br/>"
                          "<b>Question 2: Which tool supports Domain 5’s incident response?</b><br/>"
                          "• Options: Palo Alto Cortex XSOAR, AWS KMS, OneTrust<br/>"
                          "• Correct: <b>Cortex XSOAR</b> aligns with Domain 5 for automation.", body_style))
    doc.build(story)
    story = []

    # Slide 9: Actionable Steps
    story.append(Paragraph("Actionable Steps for Cloud Security", title_style))
    story.append(Paragraph("Implement CCSP-Driven Security Today<br/><br/>"
                          "<b>Beginner: Enable MFA (Domain 3):</b><br/>"
                          "• Activate MFA on AWS IAM or Azure AD.<br/>"
                          "• Action: Enable MFA for admin accounts.<br/>"
                          "• Tool: AWS IAM, Okta.<br/><br/>"
                          "<b>Beginner: Secure S3 Buckets (Domain 2):</b><br/>"
                          "• Restrict public access to prevent leaks.<br/>"
                          "• Action: Review S3 permissions.<br/>"
                          "• Tool: AWS S3 Console.<br/><br/>"
                          "<b>Intermediate: Deploy CSPM (Domain 5):</b><br/>"
                          "• Monitor and fix misconfigurations.<br/>"
                          "• Action: Set up AWS Config or Azure Security Center.<br/>"
                          "• Tool: AWS Config, Azure Security Center.<br/><br/>"
                          "<b>Intermediate: Monitor with SIEM (Domain 5):</b><br/>"
                          "• Real-time threat detection.<br/>"
                          "• Action: Configure Splunk for logs and alerts.<br/>"
                          "• Tool: Splunk, Azure Sentinel.<br/><br/>"
                          "<b>Advanced: Standardize Governance (Domain 1):</b><br/>"
                          "• Consistent policies across clouds.<br/>"
                          "• Action: Use AWS Organizations, ServiceNow GRC.<br/>"
                          "• Tool: AWS Organizations, ServiceNow GRC.<br/><br/>"
                          "<b>Advanced: Automate Incident Response (Domain 5):</b><br/>"
                          "• Deploy SOAR for threat response.<br/>"
                          "• Action: Integrate Cortex XSOAR with Sentinel.<br/>"
                          "• Tool: Cortex XSOAR, Palo Alto Sentinel.", body_style))
    doc.build(story)
    story = []

    # Slide 10: Engage and Learn More
    story.append(Paragraph("Strategize and Scale with CCSP", title_style))
    story.append(Paragraph("Next Steps for Cloud Security<br/><br/>"
                          "<b>Domain 1:</b><br/>"
                          "• Assess cloud models and governance (AWS Organizations).<br/><br/>"
                          "<b>Domain 2–4:</b><br/>"
                          "• Implement encryption (KMS, Vault), RBAC (Istio), DevSecOps (Snyk).<br/><br/>"
                          "<b>Domain 5–6:</b><br/>"
                          "• Automate monitoring (XSOAR, Splunk) and compliance (OneTrust).<br/><br/>"
                          "<b>Action:</b><br/>"
                          "• Enroll in CCSP training at <a href='http://www.isc2.org'>www.isc2.org</a>.<br/><br/>"
                          "<b>Enhanced:</b> Resilience with CCSP<br/>"
                          "<b>Unified:</b> Multi-cloud strategy", body_style))
    story.append(Table([[Paragraph("Enhanced: Resilience with CCSP<br/>Unified: Multi-cloud strategy", ParagraphStyle('Conclusion', fontSize=10, textColor=WHITE, alignment=1))]],
                       colWidths=[6*inch], style=TableStyle([('BACKGROUND', (0,0), (-1,-1), PURPLE), ('BOX', (0,0), (-1,-1), 1, PRIMARY_BLUE), ('ALIGN', (0,0), (-1,-1), 'CENTER')])))
    doc.build(story)

    return pdf_file

# Streamlit app
st.title("Cloud Security CCSP Presentation Generator")
st.write("Click the button below to generate and download a PDF presentation on Cloud Security Transformation with CCSP.")

if st.button("Generate and Download PDF"):
    with st.spinner("Generating PDF file..."):
        pdf_file = generate_pdf()
        with open(pdf_file, "rb") as f:
            pdf_bytes = f.read()
        st.download_button(
            label="Download cloud_security_ccsp.pdf",
            data=pdf_bytes,
            file_name="cloud_security_ccsp.pdf",
            mime="application/pdf"
        )
        st.success("Presentation generated! Click the download button above.")
        # Clean up temporary file
        if os.path.exists(pdf_file):
            os.remove(pdf_file)

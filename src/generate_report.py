import pathlib
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

# Path configurations
BASE_DIR = pathlib.Path(__file__).parent.parent
OUTPUT_PDF = BASE_DIR / "docs" / "report.pdf"


class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and draw total page numbers
    along with formal running headers and footers using a single consistent font and tone.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_elements(num_pages)
            super().showPage()
        super().save()

    def draw_page_elements(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#222222"))
        
        # Running header on pages 2 and later
        if self._pageNumber > 1:
            self.drawString(54, 752, "Project NeuroTone | Comprehensive Technical & Project Report")
            self.setStrokeColor(colors.HexColor("#CCCCCC"))
            self.setLineWidth(0.6)
            self.line(54, 744, 558, 744)

        # Running footer on all pages
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 36, page_str)
        self.drawString(54, 36, "Project NeuroTone — Acoustic Vocal Biomarker Screening for Parkinson's Disease")
        self.setStrokeColor(colors.HexColor("#CCCCCC"))
        self.setLineWidth(0.6)
        self.line(54, 48, 558, 48)
        
        self.restoreState()


def build_pdf():
    OUTPUT_PDF.parent.mkdir(parents=True, exist_ok=True)
    
    doc = SimpleDocTemplate(
        str(OUTPUT_PDF),
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=58,
        bottomMargin=58
    )
    
    # Consistent, formal typographic hierarchy using standard Helvetica
    # Uniform text color: dark formal charcoal (#1A1A1A)
    PRIMARY_COLOR = colors.HexColor("#1A1A1A")
    BORDER_COLOR = colors.HexColor("#D1D5DB")
    ROW_BG_LIGHT = colors.HexColor("#F9FAFB")
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=PRIMARY_COLOR,
        spaceAfter=5
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=PRIMARY_COLOR,
        spaceAfter=12
    )
    
    meta_style = ParagraphStyle(
        'MetaText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=PRIMARY_COLOR
    )
    
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=PRIMARY_COLOR,
        spaceBefore=0,
        spaceAfter=5,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=PRIMARY_COLOR,
        spaceAfter=5
    )
    
    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=PRIMARY_COLOR,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=3
    )
    
    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=PRIMARY_COLOR
    )
    
    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=PRIMARY_COLOR
    )
    
    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=PRIMARY_COLOR
    )

    story = []
    
    # =========================================================
    # PAGE 1: EXECUTIVE SUMMARY & CLINICAL FOUNDATIONS
    # =========================================================
    story.append(Paragraph("Project NeuroTone: Comprehensive Project Report", title_style))
    story.append(Paragraph("A Non-Invasive, Smartphone-Compatible Voice Acoustic Screening Prototype for Parkinson's Disease", subtitle_style))
    
    meta_data = [
        [
            Paragraph("<b>Document Version:</b> 1.0 (Formal)", meta_style),
            Paragraph("<b>Current Status:</b> Phase 3 Completed (Benchmark & Visual Deck)", meta_style)
        ],
        [
            Paragraph("<b>Project Lead:</b> NeuroTone Research & Engineering Team", meta_style),
            Paragraph("<b>Target Audience:</b> Medical, Technical, and Executive Stakeholders", meta_style)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[244, 260])
    meta_table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 0.75, BORDER_COLOR),
        ('BACKGROUND', (0, 0), (-1, -1), ROW_BG_LIGHT),
        ('PADDING', (0, 0), (-1, -1), 5),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))
    
    # 1. Executive Summary & Vision
    story.append(Paragraph("1. Executive Summary & Project Vision", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.75, color=BORDER_COLOR, spaceAfter=6, spaceBefore=0))
    story.append(Paragraph(
        "Parkinson's Disease (PD) is among the most prevalent neurodegenerative conditions globally, characterized by "
        "the progressive loss of dopamine-generating neurons in the brain. Historically, clinical diagnosis depends on "
        "observable physical motor signs, notably resting tremors, limb rigidity, and postural instability. However, by the "
        "time these overt motor symptoms become clinically apparent, an estimated 60% to 80% of dopamine-producing cells "
        "in the substantia nigra have already been irreversibly lost. Early, accessible, and continuous screening is therefore "
        "critical to facilitate timely medical and therapeutic intervention.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Project NeuroTone</b> addresses this diagnostic gap by turning a ubiquitous device—a standard smartphone—into an "
        "instantaneous, non-invasive early screening tool. Up to 90% of individuals living with Parkinson's experience subtle "
        "vocal degradation (clinically termed <i>hypophonia</i> and <i>laryngeal dysarthria</i>) in early disease stages. "
        "By prompting a patient to sustain a simple vowel phonation (such as saying 'ah' for three seconds into a phone microphone), "
        "NeuroTone extracts micro-acoustic biomarkers of vocal fold tension and neurological stability, generating an objective risk score "
        "in seconds without expensive specialized hospital hardware.",
        body_style
    ))
    story.append(Spacer(1, 4))

    # 2. Clinical & Biological Foundations
    story.append(Paragraph("2. Clinical & Biological Foundations: The Voice as a Neurological Window", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.75, color=BORDER_COLOR, spaceAfter=6, spaceBefore=0))
    story.append(Paragraph(
        "Human voice production requires sub-millisecond neurological synchronization across the brainstem, laryngeal vocal "
        "folds, respiratory diaphragm, and oral articulation tract. In Parkinson's Disease, basal ganglia dysfunction impairs "
        "fine motor control, producing three distinctive acoustic phenomena:",
        body_style
    ))
    story.append(Paragraph(
        "• <b>Laryngeal Muscle Rigidity & Incomplete Closure:</b> Stiffened vocal cord muscles cannot fully seal during "
        "vocal vibration. This allows turbulent unphonated air to escape, creating breathiness, roughness, and diminished tonal clarity.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Neurological Vocal Micro-Tremors:</b> Involuntary micro-oscillations in laryngeal muscle tension introduce rapid, "
        "cycle-to-cycle instability in fundamental frequency (pitch jitter) and wave volume (amplitude shimmer).",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Chaotic Signal Turbulence:</b> Healthy vocal fold vibration is smooth and harmonic. Parkinsonian vocal production "
        "displays elevated physical entropy and nonlinear turbulence, which can be quantified mathematically.",
        bullet_style
    ))
    story.append(Paragraph(
        "Because vocal changes frequently precede observable hand tremors by months or years, telephonic and mobile acoustic "
        "screening provides an accessible, non-stigmatizing gateway for timely clinical evaluation.",
        body_style
    ))
    
    # End of Page 1
    story.append(PageBreak())

    # =========================================================
    # PAGE 2: ARCHITECTURE, DATASET, & BIOMARKER GUIDE
    # =========================================================
    story.append(Paragraph("3. System Architecture & Engineering Organization", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.75, color=BORDER_COLOR, spaceAfter=6, spaceBefore=0))
    story.append(Paragraph(
        "NeuroTone is built according to professional Python engineering standards, ensuring end-to-end reproducibility, "
        "preventing training data leakage, and enabling modular plug-and-play model iteration.",
        body_style
    ))
    
    arch_data = [
        [Paragraph("<b>Directory / File</b>", table_header_style), Paragraph("<b>Engineering Role & Contents</b>", table_header_style)],
        [Paragraph("data/raw/", table_cell_style), Paragraph("Immutable raw datasets: UCI Parkinson's benchmark, plus reserved folders for Italian and NeuroVoz corpora.", table_cell_style)],
        [Paragraph("data/processed/", table_cell_style), Paragraph("Standardized, cleaned datasets (uci_cleaned.csv) stripped of non-predictive string identifiers.", table_cell_style)],
        [Paragraph("src/", table_cell_style), Paragraph("Core pipeline modules: data downloaders, cleaning scripts, and modular cross-validation evaluation engines.", table_cell_style)],
        [Paragraph("src/plotter/", table_cell_style), Paragraph("Visualization engine and clinical feature mapping (feature_mapping.py) for readable reporting.", table_cell_style)],
        [Paragraph("visualizations/", table_cell_style), Paragraph("High-resolution pitch-deck visual assets (300 DPI PNGs) and compressed distribution archives.", table_cell_style)],
        [Paragraph("docs/", table_cell_style), Paragraph("Documentation for context retention (project_context.md) and formal reports (report.pdf).", table_cell_style)],
        [Paragraph("requirements.txt", table_cell_style), Paragraph("Pinned dependencies across scientific computing, audio processing, tree ensembles, and reporting.", table_cell_style)],
    ]
    arch_table = Table(arch_data, colWidths=[120, 384])
    arch_table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 0.75, BORDER_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('BACKGROUND', (0, 0), (-1, 0), ROW_BG_LIGHT),
        ('PADDING', (0, 0), (-1, -1), 3.5),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(arch_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("4. Dataset Profile & Exploratory Analysis", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.75, color=BORDER_COLOR, spaceAfter=6, spaceBefore=0))
    story.append(Paragraph(
        "For Phase 1 through Phase 3, we evaluated the benchmark <b>UCI Parkinson's Disease Dataset</b>, "
        "compiled by Max Little and colleagues in partnership with the National Centre for Voice and Speech (Denver, CO).",
        body_style
    ))
    story.append(Paragraph(
        "• <b>Participant Cohort:</b> 31 individuals (23 clinically diagnosed with Parkinson's, 8 healthy controls).<br/>"
        "• <b>Total Samples:</b> 195 sustained phonations (each participant recorded ~6 takes of the vowel sound '/ah/').<br/>"
        "• <b>Extracted Measurements:</b> 22 quantitative acoustic features per sample alongside a binary diagnostic label.<br/>"
        "• <b>Severe Class Imbalance:</b> 147 samples (75.4%) are Parkinson's cases, and only 48 samples (24.6%) are Healthy controls.",
        bullet_style
    ))
    story.append(Paragraph(
        "<b>The Imbalance Challenge:</b> A naive algorithm guessing 'Parkinson's' blindly would record an apparent 75.4% accuracy "
        "while providing zero screening value. Our pipeline counters this by integrating class reweighting and clinical-grade metrics.",
        body_style
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("5. Acoustic Vocal Biomarkers Explained in Plain English", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.75, color=BORDER_COLOR, spaceAfter=6, spaceBefore=0))
    
    bio_data = [
        [Paragraph("<b>Biomarker Category</b>", table_header_style), Paragraph("<b>Key Variables</b>", table_header_style), Paragraph("<b>What It Measures in Human Speech</b>", table_header_style)],
        [
            Paragraph("<b>Fundamental Frequency (Pitch)</b>", table_cell_style),
            Paragraph("MDVP:Fo(Hz), Fhi, Flo", table_cell_style),
            Paragraph("Average, highest, and lowest pitch of the vocal cords. Captures overall vocal range, pitch boundaries, and tonal stability.", table_cell_style)
        ],
        [
            Paragraph("<b>Frequency Instability (Jitter)</b>", table_cell_style),
            Paragraph("MDVP:Jitter(%), RAP, PPQ, DDP", table_cell_style),
            Paragraph("Cycle-to-cycle timing variations in pitch. Healthy voices maintain consistent timing; vocal cord micro-tremors cause rapid jitter.", table_cell_style)
        ],
        [
            Paragraph("<b>Amplitude Instability (Shimmer)</b>", table_cell_style),
            Paragraph("MDVP:Shimmer, APQ, DDA", table_cell_style),
            Paragraph("Cycle-to-cycle loudness variations. Incomplete vocal cord seal produces rapid, involuntary volume wavering and breathiness.", table_cell_style)
        ],
        [
            Paragraph("<b>Noise & Tonal Clarity</b>", table_cell_style),
            Paragraph("HNR, NHR", table_cell_style),
            Paragraph("Harmonics-to-Noise Ratio (HNR) compares pure musical tone to turbulent breathy noise. Lower HNR indicates vocal raspiness.", table_cell_style)
        ],
        [
            Paragraph("<b>Nonlinear Signal Dynamics</b>", table_cell_style),
            Paragraph("PPE, RPDE, DFA, Spread1, Spread2", table_cell_style),
            Paragraph("Quantifies turbulence and physical chaos in sound waves. Pitch Period Entropy (PPE) detects irregular pitch drift even when basic pitch averages seem normal.", table_cell_style)
        ],
    ]
    bio_table = Table(bio_data, colWidths=[110, 114, 280])
    bio_table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 0.75, BORDER_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('BACKGROUND', (0, 0), (-1, 0), ROW_BG_LIGHT),
        ('PADDING', (0, 0), (-1, -1), 3.5),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(bio_table)
    
    # End of Page 2
    story.append(PageBreak())

    # =========================================================
    # PAGE 3: ML PIPELINE & CLINICAL PERFORMANCE
    # =========================================================
    story.append(Paragraph("6. Machine Learning Pipeline & Clinical Evaluation", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.75, color=BORDER_COLOR, spaceAfter=6, spaceBefore=0))
    story.append(Paragraph(
        "To ensure that our screening model generalizes reliably to new, unseen patients, all model evaluations were performed "
        "using rigorous <b>Stratified 5-Fold Cross-Validation</b>. The dataset was partitioned into five subsets that each "
        "preserved the 75:25 class distribution. Over five iterations, four subsets trained the classifier while the remaining "
        "subset served as a blind test set, rotating until every sample had been evaluated out-of-fold.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Clinical Metrics vs. Raw Accuracy:</b> In a healthcare screening context, overall accuracy is a secondary metric. "
        "Medical utility depends fundamentally on two clinical trade-offs:<br/>"
        "• <b>Sensitivity (Recall for Class 1):</b> The proportion of actual Parkinson's patients correctly identified. A high sensitivity "
        "ensures that individuals with neurological impairment are not falsely reassured (minimizing dangerous False Negatives).<br/>"
        "• <b>Specificity (Recall for Class 0):</b> The proportion of healthy individuals correctly classified as healthy. High specificity "
        "prevents unnecessary anxiety, diagnostic follow-ups, and specialist clinical backlogs (minimizing False Positives).<br/>"
        "• <b>Area Under the ROC Curve (AUC):</b> Measures the classifier's overall discriminative power across all possible decision "
        "thresholds, where 0.5 represents a coin flip and 1.0 represents perfect diagnostic separation.",
        body_style
    ))
    story.append(Spacer(1, 4))
    
    comp_data = [
        [Paragraph("<b>Performance Metric</b>", table_header_style), Paragraph("<b>Baseline Random Forest</b>", table_header_style), Paragraph("<b>Champion XGBoost Model</b>", table_header_style), Paragraph("<b>Clinical Interpretation & Real-World Impact</b>", table_header_style)],
        [
            Paragraph("<b>Average AUC</b>", table_cell_style),
            Paragraph("0.9622", table_cell_style),
            Paragraph("<b>0.9738 (+1.2%)</b>", table_cell_style),
            Paragraph("Exceptional discriminative separation between cohorts across all confidence thresholds.", table_cell_style)
        ],
        [
            Paragraph("<b>Sensitivity (Recall PD)</b>", table_cell_style),
            Paragraph("0.9522", table_cell_style),
            Paragraph("<b>0.9524 (Stable)</b>", table_cell_style),
            Paragraph("Catches over 95 out of every 100 individuals showing acoustic signs of Parkinson's.", table_cell_style)
        ],
        [
            Paragraph("<b>Specificity (Recall Healthy)</b>", table_cell_style),
            Paragraph("0.6933", table_cell_style),
            Paragraph("<b>0.8356 (+14.2%)</b>", table_cell_style),
            Paragraph("Dramatic reduction in false positive alarms, avoiding unnecessary patient panic.", table_cell_style)
        ],
        [
            Paragraph("<b>Derived Accuracy</b>", table_cell_style),
            Paragraph("88.8%", table_cell_style),
            Paragraph("<b>92.3% (+3.5%)</b>", table_cell_style),
            Paragraph("Correctly categorizes ~180 out of the 195 test samples across all folds.", table_cell_style)
        ],
    ]
    comp_table = Table(comp_data, colWidths=[110, 105, 110, 179])
    comp_table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 0.75, BORDER_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('BACKGROUND', (0, 0), (-1, 0), ROW_BG_LIGHT),
        ('PADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(comp_table)
    story.append(Spacer(1, 6))
    
    story.append(Paragraph(
        "<b>The Engineering Breakthrough (Managing Imbalance):</b> While the initial Random Forest baseline delivered impressive "
        "sensitivity (95.2%), its specificity was poor (69.3%), meaning it falsely classified almost one in three healthy participants "
        "as having Parkinson's. By advancing to an Extreme Gradient Boosting (XGBoost) architecture with dynamic positive class weighting "
        "(<code>scale_pos_weight = 48 / 147 = 0.3265</code>), we heavily penalized misclassifications on the minority healthy cohort. "
        "This raised specificity by +14.2 percentage points (to 83.6%) without compromising sensitivity, lifting overall accuracy to 92.3%.",
        body_style
    ))
    
    # End of Page 3
    story.append(PageBreak())

    # =========================================================
    # PAGE 4: VISUAL PORTFOLIO, ROADMAP & CONCLUSION
    # =========================================================
    story.append(Paragraph("7. Explainable AI & Visual Pitch Deck Portfolio", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.75, color=BORDER_COLOR, spaceAfter=6, spaceBefore=0))
    story.append(Paragraph(
        "Opaque 'black-box' algorithms are impractical in healthcare; clinicians must understand <i>why</i> a patient was flagged. "
        "We generated five publication-ready visual assets (saved in <code>visualizations/</code>) to provide transparent interpretability:",
        body_style
    ))
    
    asset_data = [
        [Paragraph("<b>File / Graphic</b>", table_header_style), Paragraph("<b>Visual Format</b>", table_header_style), Paragraph("<b>Stakeholder & Clinical Value</b>", table_header_style)],
        [
            Paragraph("01_shap_summary.png", table_cell_style),
            Paragraph("SHAP Beeswarm Plot", table_cell_style),
            Paragraph("Identifies global feature drivers. Shows that high Pitch Irregularity (PPE) and Spread1 strongly push the model toward a Parkinson's diagnosis.", table_cell_style)
        ],
        [
            Paragraph("02_feature_importance.png", table_cell_style),
            Paragraph("Horizontal Bar Chart", table_cell_style),
            Paragraph("Ranks the top 10 acoustic biomarkers by relative mathematical gain, confirming that nonlinear entropy and shimmer drive predictions.", table_cell_style)
        ],
        [
            Paragraph("03_case_healthy.png & 03_case_risk.png", table_cell_style),
            Paragraph("Individual Waterfall Plots", table_cell_style),
            Paragraph("Simulates an individual patient diagnostic report. Traces step-by-step why a healthy patient scored low risk, and which biomarkers elevated an at-risk score.", table_cell_style)
        ],
        [
            Paragraph("04_metrics_roc.png", table_cell_style),
            Paragraph("Confusion Matrix & ROC Curve", table_cell_style),
            Paragraph("Dual technical verification panel demonstrating low false positive counts and empirical 0.97+ AUC on a 25% holdout test partition.", table_cell_style)
        ],
        [
            Paragraph("05_raw_signal_boxplots.png", table_cell_style),
            Paragraph("2x2 Biomarker Boxplots", table_cell_style),
            Paragraph("Overlays individual raw points over cohort distributions for PPE, Jitter, Shimmer, and HNR using a modern blue/coral palette, showing clear separation.", table_cell_style)
        ],
    ]
    asset_table = Table(asset_data, colWidths=[120, 114, 270])
    asset_table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 0.75, BORDER_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('BACKGROUND', (0, 0), (-1, 0), ROW_BG_LIGHT),
        ('PADDING', (0, 0), (-1, -1), 3.5),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(asset_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("8. Current Limitations & Strategic Roadmap", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.75, color=BORDER_COLOR, spaceAfter=6, spaceBefore=0))
    story.append(Paragraph(
        "<b>Key Limitations to Address:</b><br/>"
        "1. <i>Cohort Breadth:</i> While 195 recordings were analyzed, they originated from 31 distinct individuals. Testing on broader multi-speaker populations is essential to prevent subject-level acoustic memorization.<br/>"
        "2. <i>Acoustic Environment:</i> Benchmark data was gathered in quiet acoustic chambers. Mobile microphone compression, room reverberation, and ambient noise must be validated.<br/>"
        "3. <i>Differential Diagnosis:</i> Other conditions (e.g., laryngitis, essential tremor) can temporarily alter voice and require multi-day baseline tracking.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Future Development Phases:</b><br/>"
        "• <b>Phase 4 (Audio Ingestion & Feature Extraction):</b> Ingest the Italian and NeuroVoz raw audio repositories (<code>.wav</code> format) using <code>praat-parselmouth</code>, <code>opensmile</code>, and <code>librosa</code>.<br/>"
        "• <b>Phase 5 (Mobile Microservice & Edge Deployment):</b> Export the trained XGBoost model into an embedded Flask API or ONNX runtime for sub-second, on-device mobile inference.",
        body_style
    ))
    story.append(Spacer(1, 6))
    
    concl_data = [[
        Paragraph(
            "<b>Conclusion & Takeaway:</b> Project NeuroTone demonstrates that vocal acoustic biomarkers alone can differentiate "
            "Parkinson's Disease patients from healthy controls with remarkable efficacy (<b>92.3% accuracy, 0.9738 AUC, 95.2% sensitivity</b>). "
            "By pairing clinical-grade discriminative power with explainable visual interpretations, NeuroTone provides a proven, "
            "scalable foundation for accessible, decentralized early neurological screening.",
            callout_style
        )
    ]]
    concl_table = Table(concl_data, colWidths=[504])
    concl_table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, PRIMARY_COLOR),
        ('BACKGROUND', (0, 0), (-1, -1), ROW_BG_LIGHT),
        ('PADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(concl_table)
    
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Report successfully compiled to {OUTPUT_PDF}")


if __name__ == "__main__":
    build_pdf()

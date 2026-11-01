import os
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def generate_pdf_report(regression_results, classification_results, clustering_results, output_pdf_path):
    """
    Generate a professional PDF report containing the comparison results and charts.
    """
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=letter,
        rightMargin=54, leftMargin=54,
        topMargin=54, bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles for premium aesthetics
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#1e1b4b'), # Deep Indigo
        spaceAfter=12
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#4b5563'),
        spaceAfter=24
    )
    
    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=colors.HexColor('#312e81'),
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#4f46e5'),
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'Body',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#1f2937'),
        spaceAfter=8
    )
    
    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#1f2937'),
        leftIndent=20,
        firstLineIndent=-10,
        spaceAfter=4
    )
    
    table_text_style = ParagraphStyle(
        'TableText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#1f2937')
    )
    
    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.white
    )

    story = []
    
    # --- Page 1: Header & Problem Statement ---
    story.append(Paragraph("Multi-Algorithm Recommendation System Comparison", title_style))
    story.append(Paragraph("E-Commerce Recommendation System Analysis Report", subtitle_style))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("1. Problem Statement", h1_style))
    p_text = (
        "Modern e-commerce platforms rely heavily on personalization to enhance user experience, drive engagement, "
        "and boost conversions. A robust recommendation system must address multiple dimensions of customer interaction: "
        "predicting potential product ratings (regression), forecasting purchase likelihood (classification), and "
        "segmenting users into distinct behavioral cohorts (clustering). This report implements and compares three "
        "machine learning algorithms—Ridge Regression, Logistic Regression, and K-Means Clustering—on an e-commerce dataset "
        "to deliver actionable business intelligence and optimize recommendation strategies."
    )
    story.append(Paragraph(p_text, body_style))
    
    story.append(Paragraph("2. Dataset Description & Preprocessing", h1_style))
    p_text = (
        "The dataset contains 5,000 transaction records documenting interactions between users and products. "
        "Columns include User ID, Product ID, Product Category, Price, Rating, Purchase Status, Number of Views, "
        "Cart Status, Time Spent, Previous Purchases, and Interaction Date."
    )
    story.append(Paragraph(p_text, body_style))
    story.append(Paragraph("<b>Preprocessing Steps Performed:</b>", h2_style))
    story.append(Paragraph("&bull; Verified dimensions and checked for duplicate/missing records (none found/handled).", bullet_style))
    story.append(Paragraph("&bull; One-Hot Encoded categorical product categories to construct numerical feature vectors.", bullet_style))
    story.append(Paragraph("&bull; Split supervised datasets into 80% Training and 20% Testing partitions using stratified random states.", bullet_style))
    story.append(Paragraph("&bull; Standardized numerical features using standard scaling to ensure zero mean and unit variance.", bullet_style))
    story.append(Paragraph("&bull; Aggregated transaction records at the User level to generate behavior profiles for clustering.", bullet_style))
    
    story.append(Spacer(1, 10))
    
    # --- Page 2: Regression & Classification Models ---
    story.append(Paragraph("3. Regression Model: Ridge Regression (Rating Prediction)", h1_style))
    p_text = (
        "Ridge Regression was trained to predict user product ratings. Input features included price, views, time spent, "
        "previous purchases, cart status, and product categories. Hyperparameter tuning was conducted on the regularizer "
        "strength alpha via 5-fold GridSearchCV."
    )
    story.append(Paragraph(p_text, body_style))
    
    reg_tuned = regression_results['tuned']
    reg_base = regression_results['base']
    story.append(Paragraph(
        f"<b>Key Findings:</b> The best regularizer strength was found at <b>alpha = {regression_results['best_params']['alpha']}</b>. "
        f"The tuned model achieved an MAE of <b>{reg_tuned['mae']:.4f}</b>, RMSE of <b>{reg_tuned['rmse']:.4f}</b>, and R&sup2; Score of <b>{reg_tuned['r2']:.4f}</b>. "
        f"This indicates that user ratings are driven by page interaction duration and view frequency, allowing the business to highlight products aligned with customer taste.",
        body_style
    ))
    
    if os.path.exists('images/regression_results.png'):
        story.append(Spacer(1, 5))
        img = Image('images/regression_results.png', width=4.5*inch, height=2.8*inch)
        story.append(img)
    
    story.append(PageBreak())
    
    # --- Page 3: Classification Model ---
    story.append(Paragraph("4. Classification Model: Logistic Regression (Purchase Likelihood)", h1_style))
    p_text = (
        "Logistic Regression was implemented to forecast whether a user is likely to buy a product (Purchase_Status = 1). "
        "GridSearchCV tuned regularizer C, solver, and max_iter."
    )
    story.append(Paragraph(p_text, body_style))
    
    clf_tuned = classification_results['tuned']
    story.append(Paragraph(
        f"<b>Key Findings:</b> The best parameters identified were <b>C = {classification_results['best_params']['C']}</b>, "
        f"solver = <b>{classification_results['best_params']['solver']}</b>, and max_iter = <b>{classification_results['best_params']['max_iter']}</b>. "
        f"The tuned model achieved an Accuracy of <b>{clf_tuned['accuracy']*100:.2f}%</b>, Precision of <b>{clf_tuned['precision']*100:.2f}%</b>, "
        f"Recall of <b>{clf_tuned['recall']*100:.2f}%</b>, and F1 Score of <b>{clf_tuned['f1']*100:.2f}%</b>.",
        body_style
    ))
    
    if os.path.exists('images/classification_confusion_matrix.png'):
        story.append(Spacer(1, 5))
        img = Image('images/classification_confusion_matrix.png', width=4.0*inch, height=3.0*inch)
        story.append(img)
        
    story.append(Spacer(1, 10))
    
    story.append(PageBreak())
    
    # --- Page 4: Clustering Model ---
    story.append(Paragraph("5. Clustering Model: K-Means (Customer Segmentation)", h1_style))
    p_text = (
        "K-Means clustering grouped users into cohorts using behavioral aggregations. "
        "The Elbow Method and Silhouette scores were calculated for K values 2 through 6 to identify the optimal segment size."
    )
    story.append(Paragraph(p_text, body_style))
    
    story.append(Paragraph(
        f"<b>Key Findings:</b> The optimal number of segments was selected as <b>K = {clustering_results['best_k']}</b> based on "
        f"the highest Silhouette Score of <b>{clustering_results['best_silhouette']:.4f}</b> and the elbow bend. "
        f"Each cluster corresponds to distinct shopping personas (e.g. High-Value Loyalists, Active Window Shoppers).",
        body_style
    ))
    
    if os.path.exists('images/cluster_characteristics.png'):
        story.append(Spacer(1, 5))
        img = Image('images/cluster_characteristics.png', width=5.5*inch, height=3.2*inch)
        story.append(img)
        
    story.append(PageBreak())
    
    # --- Page 5: Model Comparison Table & Business Insights ---
    story.append(Paragraph("6. Model Comparison Table", h1_style))
    
    # Construct data matrix for Table
    table_data = [
        [
            Paragraph("<b>ML Task</b>", table_header_style), 
            Paragraph("<b>Algorithm</b>", table_header_style), 
            Paragraph("<b>Target / Goal</b>", table_header_style), 
            Paragraph("<b>Metrics Used</b>", table_header_style), 
            Paragraph("<b>Best Result</b>", table_header_style), 
            Paragraph("<b>Business Use Case</b>", table_header_style)
        ],
        [
            Paragraph("Regression", table_text_style),
            Paragraph("Ridge Regression", table_text_style),
            Paragraph("Predict Rating", table_text_style),
            Paragraph("MAE, RMSE, R&sup2;", table_text_style),
            Paragraph(f"MAE: {reg_tuned['mae']:.3f}<br/>RMSE: {reg_tuned['rmse']:.3f}<br/>R&sup2;: {reg_tuned['r2']:.3f}", table_text_style),
            Paragraph("Recommend highly rated products to users.", table_text_style)
        ],
        [
            Paragraph("Classification", table_text_style),
            Paragraph("Logistic Regression", table_text_style),
            Paragraph("Predict Purchase Status", table_text_style),
            Paragraph("Acc, Prec, Rec, F1", table_text_style),
            Paragraph(f"Acc: {clf_tuned['accuracy']*100:.1f}%<br/>F1: {clf_tuned['f1']*100:.1f}%", table_text_style),
            Paragraph("Target discounts to customers likely to purchase.", table_text_style)
        ],
        [
            Paragraph("Clustering", table_text_style),
            Paragraph("K-Means", table_text_style),
            Paragraph("Segment Customers", table_text_style),
            Paragraph("Inertia, Silhouette", table_text_style),
            Paragraph(f"K: {clustering_results['best_k']}<br/>Silhouette: {clustering_results['best_silhouette']:.3f}", table_text_style),
            Paragraph("Tailor marketing strategies by user segment.", table_text_style)
        ]
    ]
    
    col_widths = [70, 85, 95, 90, 80, 110]
    comp_table = Table(table_data, colWidths=col_widths)
    comp_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e1b4b')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#f8fafc'), colors.white]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
    ]))
    
    story.append(comp_table)
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("7. Business Insights & Recommendations", h1_style))
    story.append(Paragraph("<b>Segment-Based Recommendations:</b>", h2_style))
    
    profiles = clustering_results['profiles']
    for idx, row in profiles.iterrows():
        seg_desc = (
            f"&bull; <b>{row['Segment_Name']}</b> (Size: {int(row['Size'])}): "
            f"Averages {row['Number_of_Products_Viewed']:.1f} views, {row['Number_of_Purchases']:.1f} purchases, "
            f"and total spend of ${row['Total_Amount_Spent']:.2f}. "
        )
        if 'High-Value' in row['Segment_Name']:
            seg_desc += "Action: Enroll in VIP loyalty programs, provide early-access products, and avoid aggressive discounting."
        elif 'Window' in row['Segment_Name']:
            seg_desc += "Action: Deploy retargeting emails, trigger pop-up promotions for viewed products, and display reviews."
        elif 'Occasional' in row['Segment_Name']:
            seg_desc += "Action: Send re-engagement offers, run seasonal clearance campaigns, and cross-sell trending items."
        elif 'Cart' in row['Segment_Name']:
            seg_desc += "Action: Set up automated abandoned cart emails with small incentives/free shipping options."
        else:
            seg_desc += "Action: Provide standard recommended items based on top purchase category."
            
        story.append(Paragraph(seg_desc, bullet_style))
        
    story.append(Spacer(1, 10))
    story.append(Paragraph("8. Final Conclusion", h1_style))
    conclusion_text = (
        "By integrating Ridge Regression (predictive ratings), Logistic Regression (purchase intent), and K-Means "
        "(demographic/behavioral grouping), the recommendation system establishes a multi-layered personalization funnel. "
        "Clustering classifies the user's cohort, Classification filters products with the highest purchase intent, "
        "and Regression ranks them to maximize engagement. Implementing this composite pipeline will optimize ad spending, "
        "elevate click-through rates, and enhance e-commerce transaction volumes."
    )
    story.append(Paragraph(conclusion_text, body_style))
    
    # Build Document
    doc.build(story)
    print(f"PDF report successfully compiled at '{output_pdf_path}'")

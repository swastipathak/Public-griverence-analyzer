# Public-griverence-analyzer

An automated system for processing handwritten or scanned grievance letters. It extracts text from uploaded complaint documents (PDFs/Images), classifies the grievance into predefined categories, detects urgency using priority scoring, and visualizes results on a Streamlit dashboard.

Features:
• Supports multiple file uploads at once
• OCR text extraction from scanned PDF and images
• Category classification based on keyword matching
• Urgency detection using weighted NLP rules
• Interactive dashboard with charts and metrics
• High-priority complaint filtering
• CSV export option

NLP Logic:
Category Classification:
Road & Transport, Water Supply, Electricity, Sanitation, Health & Safety, Fraud or Legal, Government Service Delay, Other

Priority Scoring:
High – Emergency related keywords (accident, fire, danger)
Medium – Threat, fraud, refund related complaints
Low – General complaints

Tech Stack:
Frontend – Streamlit (Dashboard UI)
Backend – Python (Core logic)
OCR – EasyOCR (Extract text from images and PDFs)
File Handling – pdf2image, PIL (Convert PDF pages into images)
Data Processing – Pandas and NumPy
Visualization – Altair Charts, Streamlit display components
Regex based NLP – re library for keyword detection

How to Run:

Create a virtual environment

Activate the virtual environment

Install dependencies using pip install -r requirements.txt

Run the Streamlit app using streamlit run app.py
This will launch the dashboard in the browser.

Requirements:
streamlit
pandas
numpy
altair
easyocr
pdf2image
Pillow

Dashboard Output:
• Total complaints displayed
• High priority complaints highlighted
• Priority-wise pie chart
• Category-wise bar graph
• Detailed table view of all complaints
• CSV download button

Future Scope:
• Deep learning-based NLP for better accuracy
• Multilingual grievance support
• Mobile app integration
• Complaint routing to appropriate department
• Real-time emergency alerts for dangerous cases

Conclusion:
This project helps improve public grievance handling by speeding up the review process. It identifies urgent issues quickly and provides an organized dashboard for better decision-making.

Author: 
#Swasti Pathak

# ✅ Grievance Analyzer – Final Improved Version

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import re
from io import BytesIO
from PIL import Image
import easyocr
from deep_translator import GoogleTranslator
from pdf2image import convert_from_bytes

st.set_page_config(page_title="Grievance Analyzer", layout="wide")

reader = easyocr.Reader(['en'])

CATEGORY_KEYWORDS = {
    "Road & Transport": ["road", "pothole", "traffic", "street", "bridge"],
    "Water Supply": ["water", "pipeline", "tap", "sewage"],
    "Electricity": ["electricity", "power", "transformer", "light", "voltage"],
    "Sanitation": ["garbage", "cleaning", "toilet", "waste"],
    "Health & Safety": ["injury", "hospital", "health", "emergency", "danger"],
    "Fraud / Legal": ["fraud", "scam", "unauthorized", "threat", "harass"],
    "Government Service Delay": ["delay", "pending", "no response", "late"],
    "Other": []
}

PRIORITY_WEIGHTS = [
    (r"\b(fire|injury|accident|emergency|critical|danger)\b", 50),
    (r"\b(urgent|immediately|asap|now|please help)\b", 25),
    (r"\b(threat|violent|attack|assault)\b", 30),
    (r"\b(fraud|scam|unauthorized|refund)\b", 20),
    (r"\b(delay|pending|waiting)\b", 10)
]


def compute_priority(text):
    t = text.lower()
    score = sum(w for p, w in PRIORITY_WEIGHTS if re.search(p, t))
    if score >= 50: return score, "High"
    if score >= 20: return score, "Medium"
    return score, "Low"


def extract_title(text):
    match = re.search(r"(sub:|subject:)\s*(.+)", text, re.I)
    return match.group(2).strip() if match else text.split("\n")[0][:80]


def extract_category(text):
    t = text.lower()
    for cat, keys in CATEGORY_KEYWORDS.items():
        if any(word in t for word in keys):
            return cat
    return "Other"


def run_ocr(file):
    raw = file.read()
    name = file.name.lower()
    text = ""

    if name.endswith(".pdf"):
        pages = convert_from_bytes(raw, dpi=250)
        text = " ".join([" ".join(reader.readtext(np.array(p), detail=0)) for p in pages])
    else:
        img = Image.open(BytesIO(raw)).convert("RGB")
        text = " ".join(reader.readtext(np.array(img), detail=0))

    try:
        return GoogleTranslator(source="auto", target="en").translate(text)
    except:
        return text


# UI
st.title("📊 Grievance Analyzer – Batch Complaint Dashboard")

uploaded_files = st.file_uploader("Upload Complaints (Multi-file Support)", type=["pdf","png","jpg","jpeg"], accept_multiple_files=True)

if uploaded_files:
    data = []

    for file in uploaded_files:
        text = run_ocr(file)
        title = extract_title(text)
        category = extract_category(text)
        score, priority = compute_priority(text)

        data.append({
            "File": file.name,
            "Title": title,
            "Complaint": text,
            "Category": category,
            "Priority": priority,
            "Score": score
        })

    df = pd.DataFrame(data)

    st.success("✅ Complaints Analyzed Successfully!")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Complaints", len(df))
    col2.metric("High Priority", (df.Priority == "High").sum())
    col3.metric("Medium Priority", (df.Priority == "Medium").sum())

    # 📌 Priority Chart
    st.markdown("### Priority Distribution")
    priority_chart = alt.Chart(df).mark_arc().encode(
        theta="count()",
        color=alt.Color("Priority", scale=alt.Scale(
            domain=["High", "Medium", "Low"],
            range=["#FF4C4C", "#FFA726", "#29CC7E"]
        )),
        tooltip=["Priority","count()"]
    )
    st.altair_chart(priority_chart, use_container_width=True)

    # 📌 Category Distribution
    st.markdown("### Complaint Categories")
    st.bar_chart(df["Category"].value_counts())

    st.markdown("### 🔥 High Priority Complaints — Fix First")
    st.dataframe(df[df.Priority=="High"])

    st.markdown("### 📄 All Complaints")
    st.dataframe(df)

    st.download_button("⬇ Download CSV", df.to_csv(index=False).encode('utf-8'), "grievance_results.csv")

else:
    st.info("Upload Complaint Letters… ✅")

# ai_helpers.py
# Local-only simple AI helpers

import sqlite3
import os
from datetime import date, timedelta

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "prms_patients.db")


import re


def summarize_notes(text):
    """
    2-3 line human-style summary + scored disease guess (better detection).
    """
    import re

    if not text or not text.strip():
        return ""

    t = text.lower()
    red_flags = [
        "chest pain", "shortness of breath", "breathless",
         "unconscious", "severe bleeding", "low bp"
        ]

    urgent = any(flag in t for flag in red_flags)

    # --- symptom keyword groups (word -> weight) ---
    groups = {
        "fever": {"fever", "temperature", "chill", "febrile"},
        "throat": {"throat", "tonsil", "swallow", "sore throat", "redness"},
        "respiratory": {"cough", "cold", "shortness", "breath", "wheeze", "sputum"},
        "gastro": {"diarr", "stool", "vomit", "nausea", "abdomen", "cramp"},
        "headache": {"headache", "migraine", "dizzy"},
        "joint": {
            "joint",
            "knee",
            "elbow",
            "hip",
            "arthritis",
            "stiffness",
            "swelling",
        },
        "chest": {"chest", "angina", "pressure", "ecg", "palpit"},
        "rash": {"rash", "petechiae", "bleeding", "spots"},
        "anxiety": {"anxiety", "restless", "panic", "palpitations", "sweat"},
    }

    # disease candidates mapped from groups (higher priority first)
    disease_map = {
        "Dengue-like": ["fever", "rash"],
        "Viral Fever / Throat Infection": ["fever", "throat", "respiratory"],
        "Common Cold / Viral Infection": ["respiratory"],
        "Gastrointestinal Infection": ["gastro"],
        "Migraine / Headache": ["headache"],
        "Arthritis / Joint Pain": ["joint"],
        "Cardiac / Chest Concern": ["chest"],
        "Anxiety / Panic": ["anxiety"],
    }

    # --- score groups ---
    token_counts = {}
    words = re.findall(r"\w+", t)
    for g, keys in groups.items():
        count = 0
        for k in keys:
            # count substring occurrences for multi-word tokens too
            count += t.count(k)
        token_counts[g] = count

    # --- score diseases by summing relevant groups ---
    disease_scores = {}
    for disease, related in disease_map.items():
        sc = 0
        for g in related:
            sc += token_counts.get(g, 0)
        disease_scores[disease] = sc

    # pick best disease (if all zero, fallback to generic)
    best = max(disease_scores.items(), key=lambda x: x[1])
    best_name, best_score = best
    if best_score == 0:
        # fallback guessing using simple heuristics
        if "fever" in t:
            best_name = "Fever (likely viral)"
        elif any(w in t for w in ["cough", "cold", "sore throat"]):
            best_name = "Common viral respiratory infection"
        elif any(w in t for w in ["diarr", "vomit", "stomach", "nausea"]):
            best_name = "Gastrointestinal infection"
        elif any(w in t for w in ["joint", "knee", "arthritis"]):
            best_name = "Arthritis / Joint Pain"
        else:
            best_name = "General illness"

    # --- extract detail pieces ---
    days = ""
    m = re.search(r"(\d+)\s+day", t)
    if m:
        days = f"for about {m.group(1)} days"
    elif "yesterday" in t:
        days = "since yesterday"

    has_fever = "fever" in t or "temperature" in t
    has_headache = "headache" in t or "migraine" in t
    has_nausea = "nausea" in t or "vomit" in t
    has_appetite = "appetite" in t or "reduced appetite" in t
    has_bodypain = "body pain" in t or "bodyache" in t or "myalgia" in t
    has_joint = token_counts.get("joint", 0) > 0

    # --- build 2-3 lines ---
    lines = []

    # line 1: main condition
    if has_fever:
        lines.append(f"The patient is experiencing fever {days}.".strip())
    elif has_joint:
        lines.append(f"The patient reports joint pain {days}.".strip())
    else:
        lines.append(
            "The patient reports illness and symptoms suggestive of an infection."
        )

    # line 2: symptoms
    sym = []
    if has_headache:
        sym.append("headache")
    if has_nausea:
        sym.append("nausea")
    if has_appetite:
        sym.append("reduced appetite")
    if has_bodypain:
        sym.append("body pain")
    if has_joint and "joint pain" not in " ".join(sym):
        sym.append("joint pain")

    if sym:
        lines.append("Key symptoms: " + ", ".join(sym) + ".")
    else:
        lines.append("Key symptoms noted in the record were reviewed.")

    # line 3: disease guess
    if urgent:
        lines.append("⚠ Urgent symptoms detected. Immediate medical attention advised.")
    else:
        lines.append(f"Likely condition: {best_name}.")
    return "\n".join(lines[:3])
    return "\n".join(lines)


# --- 3) Risk Flag (rule-based) ---
def risk_flag(age, disease, is_chronic):
    high = {
        "Heart Failure",
        "Stroke",
        "Coronary Artery Disease",
        "Chronic Kidney Disease",
        "Liver Cirrhosis",
        "Lung Cancer",
    }
    try:
        age = int(age)
    except:
        age = 0
    if disease in high or (is_chronic and age >= 55) or age >= 65:
        return "High"
    if is_chronic or age >= 50:
        return "Medium"
    return "Low"


# --- New: Predict top diseases (simple rule-based scorer) ---
def predict_diseases(text, top=3):
    if not text or not text.strip():
        return []
    t = text.lower()
    groups = {
        "fever": {"fever", "temperature", "chill", "febrile"},
        "throat": {"throat", "tonsil", "swallow", "sore throat"},
        "respiratory": {"cough", "cold", "shortness", "breath", "wheeze", "sputum"},
        "gastro": {"diarr", "stool", "vomit", "nausea", "abdomen", "cramp"},
        "headache": {"headache", "migraine", "dizzy"},
        "joint": {
            "joint",
            "knee",
            "elbow",
            "hip",
            "arthritis",
            "stiffness",
            "swelling",
        },
        "chest": {"chest", "angina", "pressure", "ecg", "palpit"},
        "rash": {"rash", "petechiae", "bleeding", "spots"},
        "anxiety": {"anxiety", "restless", "panic", "palpitations", "sweat"},
    }
    disease_map = {
        "Dengue-like": ["fever", "rash"],
        "Viral Fever / Throat Infection": ["fever", "throat", "respiratory"],
        "Common Cold / Viral Infection": ["respiratory"],
        "Gastrointestinal Infection": ["gastro"],
        "Migraine / Headache": ["headache"],
        "Arthritis / Joint Pain": ["joint"],
        "Cardiac / Chest Concern": ["chest"],
        "Anxiety / Panic": ["anxiety"],
    }
    token_counts = {}
    for g, keys in groups.items():
        count = 0
        for k in keys:
            count += t.count(k)
        token_counts[g] = count
    disease_scores = {}
    for disease, related in disease_map.items():
        sc = 0
        for g in related:
            sc += token_counts.get(g, 0)
        disease_scores[disease] = sc
    items = sorted(disease_scores.items(), key=lambda x: x[1], reverse=True)
    if items and items[0][1] == 0:
        fallback = []
        if "fever" in t:
            fallback.append(("Fever (likely viral)", 1))
        if any(w in t for w in ["cough", "cold", "sore throat"]):
            fallback.append(("Common viral respiratory infection", 1))
        if any(w in t for w in ["diarr", "vomit", "stomach", "nausea"]):
            fallback.append(("Gastrointestinal infection", 1))
        return fallback[:top]
    return items[:top]


# --- New: Admission / bed recommendation (uses risk_flag) ---
def admission_recommendation(age, disease, is_chronic, notes=""):
    try:
        age = int(age)
    except Exception:
        age = 0
    red_flags = [
        "chest pain",
        "shortness of breath",
        "breathless",
        "low bp",
        "unconscious",
        "severe bleeding",
    ]
    t = (notes or "").lower()
    if any(k in t for k in red_flags):
        return "Recommend urgent admission"
    risk = risk_flag(age, disease, is_chronic)
    if risk == "High":
        return "Recommend admission"
    return "Outpatient / Monitor"


# --- New: Follow-up suggestion mapping ---
FOLLOWUP_MAP = {
    "Dengue-like": 7,
    "Viral Fever / Throat Infection": 7,
    "Common Cold / Viral Infection": 3,
    "Gastrointestinal Infection": 7,
    "Migraine / Headache": 7,
    "Arthritis / Joint Pain": 14,
    "Cardiac / Chest Concern": 7,
    "Anxiety / Panic": 14,
    # 🔴 Cancer follow-ups
    "Breast Cancer": 7,
    "Lung Cancer": 7,
    "Thyroid Cancer": 7,
    "Cancer": 7,
}


def suggest_followup_days(disease):
    if not disease:
        return 14

    d = disease.lower()

    if "cancer" in d:
        return 7
    if "cold" in d or "viral" in d:
        return 3
    if "fever" in d:
        return 7
    if "arthritis" in d:
        return 14
    if "cardiac" in d or "heart" in d:
        return 7

    return 14


# --- 4) Auto chronic/acute detection ---
CHRONIC_DISEASES = {
    "Diabetes",
    "Hypertension",
    "Asthma",
    "COPD",
    "Chronic Kidney Disease",
    "Coronary Artery Disease",
    "Heart Failure",
    "Osteoarthritis",
    "Hypothyroidism",
    "Hyperthyroidism",
    "PCOS",
    "Thyroid Cancer",
}


def ai_insight(age, disease, chronic):
    """
    Returns: (message, color)
    """
    if not age or not disease:
        return None, "#777"

    try:
        age = int(age)
    except:
        return None, "#777"

    risk = risk_flag(age, disease, chronic)
    similar = find_similar_patients(age, disease)

    if risk == "High":
        msg = "🔴 High risk | Immediate attention advised"
        color = "red"
    elif risk == "Medium":
        msg = "🟠 Moderate risk | Regular monitoring advised"
        color = "orange"
    else:
        msg = "🟢 Low risk | Routine care sufficient"
        color = "green"

    if similar:
        msg += f" | {len(similar)} similar cases found"

    return msg, color


def guess_type(disease):
    if not disease:
        return None
    if disease in CHRONIC_DISEASES:
        return "Chronic"
    return "Acute"


# --- 5) Similar patient finder (using DB) ---
def find_similar_patients(age, disease):
    try:
        age = int(age)
    except:
        return []
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(
        """
    SELECT id, name, age, gender, phone, disease, admission_date
    FROM patients
    WHERE disease = ?
      AND ABS(age - ?) <= 5
    """,
        (disease, age),
    )
    rows = cur.fetchall()
    conn.close()
    return rows


def suggest_followup_date(admission_date, disease):
    try:
        days = suggest_followup_days(disease)
        adm = date.fromisoformat(admission_date)
        return (adm + timedelta(days=days)).isoformat()
    except Exception:
        return None

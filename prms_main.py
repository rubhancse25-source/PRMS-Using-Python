#!/usr/bin/env python3
"""
prms_final.py — Patient Records Management System (single-file)

Run:
    python3 prms_final.py

DB stored at: ~/prms_patients.db
Config (password) at: ~/.prms_config.json

This file is self-contained and has a dependency-free fallback reports window.
"""


import datetime
import sqlite3
import os
import sys
import hashlib
import json
import datetime
import calendar as pycalendar
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import csv
import matplotlib.pyplot as plt




APP_NAME = "🩺 Smart Patient Records Management System"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "prms_patients.db")
CFG_FILE = os.path.join(os.path.expanduser("~"), ".prms_config.json")
SIDEBAR_IMAGE = "/mnt/data/84bdbd41-643f-4a9c-a0fc-05bd5d7f2011.png"
SIDEBAR_BLUE = "#174f86"


def get_conn():
    return sqlite3.connect(DB_FILE, timeout=10)


def init_db():
    import sqlite3

    with sqlite3.connect(DB_FILE, timeout=15) as conn:
        cur = conn.cursor()

        # Enable WAL mode (prevents locks)
        cur.execute("PRAGMA journal_mode=WAL;")
        cur.execute("PRAGMA foreign_keys=ON;")

        cur.execute(
            """
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            phone TEXT,
            disease TEXT,
            chronic INTEGER,
            admission_date TEXT,
            notes TEXT,
            followup_date TEXT
        )
        """
        )

        # Insert sample data ONLY if table is empty
        cur.execute("SELECT COUNT(*) FROM patients")
        if cur.fetchone()[0] == 0:
            sample = [
                (
                    "Alice Smith",
                    32,
                    "Female",
                    "9876543210",
                    "Hypertension",
                    1,
                    "2025-10-12",
                    "",
                    None,
                ),
                (
                    "Bob Kumar",
                    45,
                    "Male",
                    "9123456780",
                    "Diabetes",
                    1,
                    "2025-11-01",
                    "",
                    None,
                ),
                (
                    "Carol Jain",
                    26,
                    "Female",
                    "9988776655",
                    "Influenza",
                    0,
                    "2025-11-05",
                    "",
                    None,
                ),
                (
                    "Deepak Rao",
                    50,
                    "Male",
                    "9123456781",
                    "Coronary Artery Disease",
                    1,
                    "2025-09-21",
                    "",
                    None,
                ),
                (
                    "Esha Patel",
                    29,
                    "Female",
                    "9876501234",
                    "Asthma",
                    0,
                    "2025-08-14",
                    "",
                    None,
                ),
                (
                    "Farhan Ali",
                    60,
                    "Male",
                    "9012345678",
                    "Chronic Kidney Disease",
                    1,
                    "2025-07-03",
                    "",
                    None,
                ),
                (
                    "Gita Menon",
                    41,
                    "Female",
                    "9001123344",
                    "Thyroid Disorder",
                    1,
                    "2025-06-11",
                    "",
                    None,
                ),
                (
                    "Himanshu Verma",
                    35,
                    "Male",
                    "9988123456",
                    "Gastritis",
                    0,
                    "2025-05-25",
                    "",
                    None,
                ),
                (
                    "Isha Nair",
                    22,
                    "Female",
                    "9955123456",
                    "Migraine",
                    0,
                    "2025-04-02",
                    "",
                    None,
                ),
                (
                    "Jatin Singh",
                    67,
                    "Male",
                    "9933456789",
                    "Osteoarthritis",
                    1,
                    "2025-03-18",
                    "",
                    None,
                ),
                (
                    "Kavya Rao",
                    31,
                    "Female",
                    "9922334455",
                    "PCOS",
                    0,
                    "2025-02-06",
                    "",
                    None,
                ),
                (
                    "Lalit Sharma",
                    48,
                    "Male",
                    "9911223344",
                    "COPD",
                    1,
                    "2025-01-29",
                    "",
                    None,
                ),
                (
                    "Meera Joshi",
                    56,
                    "Female",
                    "9900112233",
                    "Breast Cancer",
                    1,
                    "2024-12-19",
                    "",
                    None,
                ),
                (
                    "Naveen K",
                    38,
                    "Male",
                    "9899001122",
                    "Diabetes",
                    1,
                    "2024-11-09",
                    "",
                    None,
                ),
                (
                    "Ojaswini Patel",
                    27,
                    "Female",
                    "9888776655",
                    "Anemia",
                    0,
                    "2024-10-01",
                    "",
                    None,
                ),
                (
                    "Pranav Gupta",
                    44,
                    "Male",
                    "9876504321",
                    "Pneumonia",
                    0,
                    "2025-09-05",
                    "",
                    None,
                ),
                (
                    "Riya Sharma",
                    36,
                    "Female",
                    "9865432109",
                    "Dengue",
                    0,
                    "2025-08-20",
                    "",
                    None,
                ),
                (
                    "Siddharth Roy",
                    53,
                    "Male",
                    "9854321098",
                    "Stroke",
                    1,
                    "2025-07-12",
                    "",
                    None,
                ),
                (
                    "Tanvi Desai",
                    30,
                    "Female",
                    "9843210987",
                    "Thyroid Cancer",
                    1,
                    "2025-06-01",
                    "",
                    None,
                ),
                (
                    "Uday Mehta",
                    28,
                    "Male",
                    "9832109876",
                    "Appendicitis",
                    0,
                    "2025-05-02",
                    "",
                    None,
                ),
                ('Himanshu Rao', 34, 'Male', '9812345670', 'Diabetes', 1, '2023-03-15', '', None),
                ('Riya Singh', 29, 'Female', '9823456701', 'Asthma', 0, '2024-01-22', '', None),
                ('Arjun Patel', 41, 'Male', '9834567012', 'Hypertension', 1, '2022-11-10', '', None),
                ('Sneha Gupta', 25, 'Female', '9845670123', 'Migraine', 0, '2025-02-18', '', None),
                ('Rahul Sharma', 52, 'Male', '9856701234', 'Coronary Artery Disease', 1, '2021-07-09', '', None),
                ('Divya Menon', 38, 'Female', '9867012345', 'Gastritis', 0, '2023-09-27', '', None),
                ('Vikram Desai', 60, 'Male', '9870123456', 'Chronic Kidney Disease', 1, '2020-12-05', '', None),
                ('Priya Nair', 33, 'Female', '9881234567', 'Anxiety Disorder', 1, '2024-08-14', '', None),
                ('Karan Jain', 47, 'Male', '9892345678', 'COPD', 1, '2021-10-21', '', None),
                ('Tanvi Iyer', 31, 'Female', '9803456789', 'PCOS', 0, '2022-05-30', '', None),
                ('Manish Kumar', 44, 'Male', '9814567890', 'Pneumonia', 0, '2023-01-11', '', None),
                ('Pooja Yadav', 27, 'Female', '9825678901', 'Dengue', 0, '2024-06-03', '', None),
                ('Rohan Verma', 39, 'Male', '9836789012', 'Depression', 1, '2022-09-19', '', None),
                ('Neha Reddy', 36, 'Female', '9847890123', 'Thyroid Cancer', 1, '2021-03-28', '', None),
                ('Siddharth Das', 58, 'Male', '9858901234', 'Stroke', 1, '2020-04-17', '', None),
                ('Kavya Saha', 24, 'Female', '9869012345', 'Common Cold', 0, '2025-03-09', '', None),
                ('Amit Roy', 49, 'Male', '9879123456', 'Lung Cancer', 1, '2023-10-01', '', None),
                ('Meera Khan', 42, 'Female', '9880234567', 'Rheumatoid Arthritis', 1, '2022-02-26', '', None),
                ('Naveen Joshi', 55, 'Male', '9891345678', 'Heart Failure', 1, '2021-09-05', '', None),
                ('Isha Bansal', 28, 'Female', '9802456789', 'Urinary Tract Infection', 0, '2024-07-16', '', None),
                ('Farhan Ali', 63, 'Male', '9813567890', 'Liver Cirrhosis', 1, '2020-06-22', '', None),
                ('Riya Mehta', 30, 'Female', '9824678901', 'Allergic Rhinitis', 0, '2023-11-12', '', None),
                ('Arjun Singh', 46, 'Male', '9835789012', 'Ischemic Stroke', 1, '2021-12-19', '', None),
                ('Sneha Patel', 35, 'Female', '9846890123', 'IBS', 1, '2022-08-08', '', None),
                ('Himanshu Shah', 50, 'Male', '9857901234', 'Hypertension', 1, '2020-10-30', '', None),
                ('Divya Rao', 26, 'Female', '9868012345', 'Chickenpox', 0, '2024-04-04', '', None),
                ('Rahul Jain', 40, 'Male', '9879123457', 'GERD', 1, '2023-02-15', '', None),
                ('Priya Singh', 37, 'Female', '9880234568', 'Migraine', 0, '2022-01-29', '', None),
                ('Vikram Gupta', 61, 'Male', '9891345679', 'CKD', 1, '2021-05-18', '', None),
                ('Tanvi Rao', 32, 'Female', '9802456790', 'Asthma', 0, '2023-06-24', '', None),
                ('Rohan Kumar', 54, 'Male', '9813567801', 'Myocardial Infarction', 1, '2020-03-13', '', None),
                ('Kavya Jain', 29, 'Female', '9824678012', 'PCOS', 0, '2024-10-07', '', None),
                ('Manish Sharma', 48, 'Male', '9835780123', 'Diabetes', 1, '2021-08-01', '', None),
                ('Pooja Desai', 34, 'Female', '9846890234', 'Hypothyroidism', 1, '2022-03-21', '', None),
                ('Naveen Iyer', 57, 'Male', '9857900345', 'COPD', 1, '2020-01-27', '', None),
                ('Riya Kumar', 23, 'Female', '9868010456', 'Anxiety Disorder', 0, '2025-01-05', '', None),
                ('Arjun Yadav', 45, 'Male', '9879120567', 'Tuberculosis', 1, '2023-05-14', '', None),
                ('Sneha Verma', 33, 'Female', '9880230678', 'Psoriasis', 1, '2022-09-02', '', None),
                ('Rahul Nair', 51, 'Male', '9891340789', 'Coronary Artery Disease', 1, '2021-11-25', '', None),
                ('Divya Patel', 27, 'Female', '9802450890', 'Dengue', 0, '2024-02-28', '', None),
                ('Vikram Singh', 59, 'Male', '9813560901', 'Chronic Kidney Disease', 1, '2020-09-19', '', None),
                ('Priya Gupta', 39, 'Female', '9824671012', 'Depression', 1, '2023-07-03', '', None),
                ('Farhan Khan', 62, 'Male', '9835781123', 'Heart Failure', 1, '2021-04-11', '', None),
                ('Kavya Roy', 30, 'Female', '9846891234', 'Migraine', 0, '2022-12-06', '', None),
                ('Himanshu Patel', 43, 'Male', '9857901345', 'Hypertension', 1, '2020-02-09', '', None),
                ('Neha Singh', 28, 'Female', '9868011456', 'Common Cold', 0, '2024-09-13', '', None),
                ('Rohan Das', 52, 'Male', '9879121567', 'Stroke', 1, '2021-06-01', '', None),
                ('Tanvi Shah', 31, 'Female', '9880231678', 'PCOS', 0, '2023-03-26', '', None),
                ('Amit Gupta', 49, 'Male', '9891341789', 'Lung Cancer', 1, '2022-05-07', '', None),
                ('Meera Rao', 41, 'Female', '9802451890', 'Rheumatoid Arthritis', 1, '2020-08-20', '', None),
                ('Naveen Singh', 56, 'Male', '9813561901', 'Diabetes', 1, '2021-02-04', '', None),
                ('Isha Desai', 25, 'Female', '9824672012', 'Urinary Tract Infection', 0, '2024-11-18', '', None),
                ('Farhan Mehta', 64, 'Male', '9835782123', 'Liver Cirrhosis', 1, '2020-07-29', '', None),
                ('Riya Jain', 29, 'Female', '9846892234', 'Allergy', 0, '2023-01-02', '', None),
                ('Arjun Kumar', 47, 'Male', '9857902345', 'Ischemic Stroke', 1, '2022-04-15', '', None),
                ('Sneha Roy', 32, 'Female', '9868012456', 'Gastritis', 0, '2024-03-20', '', None),
                ('Rahul Patel', 53, 'Male', '9879122567', 'Heart Attack', 1, '2021-09-09', '', None),
                ('Divya Singh', 26, 'Female', '9880232678', 'Influenza', 0, '2025-02-01', '', None),
                ('Vikram Rao', 60, 'Male', '9891342789', 'CKD', 1, '2020-05-24', '', None),
                ('Priya Shah', 38, 'Female', '9802452890', 'Anxiety Disorder', 1, '2023-10-10', '', None),
                ('Manish Verma', 46, 'Male', '9813562901', 'COPD', 1, '2022-06-06', '', None),
                ('Pooja Gupta', 34, 'Female', '9824673012', 'Migraine', 0, '2024-08-27', '', None),
                ('Naveen Rao', 58, 'Male', '9835783123', 'Coronary Artery Disease', 1, '2021-03-03', '', None),
                ('Riya Patel', 27, 'Female', '9846893234', 'Dengue', 0, '2023-12-22', '', None),
                ('Arjun Mehta', 50, 'Male', '9857903345', 'Hypertension', 1, '2020-11-14', '', None),
                ('Sneha Kumar', 33, 'Female', '9868013456', 'Psoriasis', 1, '2022-02-18', '', None),
                ('Rahul Roy', 55, 'Male', '9879123567', 'Heart Failure', 1, '2021-01-31', '', None),
                ('Kavya Nair', 30, 'Female', '9880233678', 'PCOS', 0, '2024-05-25', '', None),
                ('Himanshu Singh', 42, 'Male', '9891343789', 'Diabetes', 1, '2022-09-30', '', None),
                ('Neha Gupta', 29, 'Female', '9802453890', 'Common Cold', 0, '2023-04-08', '', None),
                ('Rohan Iyer', 51, 'Male', '9813563901', 'Stroke', 1, '2020-06-16', '', None),
                ('Tanvi Das', 35, 'Female', '9824674012', 'Asthma', 0, '2024-01-19', '', None),
                ('Amit Shah', 48, 'Male', '9835784123', 'Lung Cancer', 1, '2021-07-27', '', None),
                ('Meera Patel', 40, 'Female', '9846894234', 'Rheumatoid Arthritis', 1, '2022-03-05', '', None),
                ('Naveen Yadav', 57, 'Male', '9857904345', 'Chronic Kidney Disease', 1, '2020-09-01', '', None),
                ('Isha Rao', 24, 'Female', '9868014456', 'Urinary Tract Infection', 0, '2025-03-14', '', None),
                ('Farhan Singh', 63, 'Male', '9879124567', 'Liver Cirrhosis', 1, '2021-10-23', '', None),
                ('Riya Desai', 31, 'Female', '9880234678', 'Allergic Rhinitis', 0, '2023-02-09', '', None),
                ('Arjun Patel', 46, 'Male', '9891344789', 'Ischemic Stroke', 1, '2022-11-06', '', None),
                ('Sneha Mehta', 36, 'Female', '9802454890', 'Gastritis', 0, '2024-09-04', '', None),
                ('Rahul Singh', 54, 'Male', '9813564901', 'Heart Attack', 1, '2021-05-20', '', None),
                ('Divya Kumar', 28, 'Female', '9824675123', 'Influenza', 0, '2023-06-29', '', None),
                ('Vikram Shah', 59, 'Male', '9835785234', 'CKD', 1, '2020-02-12', '', None),
                ('Priya Rao', 37, 'Female', '9846895345', 'Depression', 1, '2022-08-17', '', None),
                ('Manish Patel', 47, 'Male', '9857905456', 'COPD', 1, '2021-12-01', '', None),
                ('Pooja Jain', 32, 'Female', '9868015567', 'Migraine', 0, '2024-07-07', '', None),
                ('Naveen Gupta', 56, 'Male', '9879125678', 'Coronary Artery Disease', 1, '2020-04-26', '', None),
                ('Riya Iyer', 26, 'Female', '9880235789', 'Dengue', 0, '2023-11-03', '', None),
                ('Arjun Saha', 49, 'Male', '9891345890', 'Hypertension', 1, '2022-01-22', '', None),
                ('Sneha Yadav', 34, 'Female', '9802455901', 'Psoriasis', 1, '2021-09-30', '', None),
                ('Rahul Mehta', 53, 'Male', '9813566012', 'Heart Failure', 1, '2020-08-08', '', None),
                ('Kavya Singh', 29, 'Female', '9824676123', 'PCOS', 0, '2024-06-02', '', None),
                ('Himanshu Desai', 41, 'Male', '9835786234', 'Diabetes', 1, '2021-03-18', '', None),
                ('Neha Rao', 27, 'Female', '9846896345', 'Common Cold', 0, '2023-05-11', '', None),
                ('Rohan Shah', 52, 'Male', '9857906456', 'Stroke', 1, '2020-10-05', '', None),
                ('Tanvi Gupta', 33, 'Female', '9868016567', 'Asthma', 0, '2024-12-09', '', None),
                ('Amit Singh', 47, 'Male', '9879126678', 'Lung Cancer', 1, '2022-07-16', '', None),
                ('Meera Jain', 39, 'Female', '9880236789', 'Rheumatoid Arthritis', 1, '2021-02-01', '', None),
                ('Naveen Patel', 58, 'Male', '9891346890', 'Chronic Kidney Disease', 1, '2020-06-28', '', None),
                ('Isha Sharma', 25, 'Female', '9802456901', 'Urinary Tract Infection', 0, '2025-04-23', '', None),
                ('Farhan Rao', 62, 'Male', '9813567013', 'Liver Cirrhosis', 1, '2021-11-30', '', None),
                ('Riya Kumar', 30, 'Female', '9824677124', 'Allergy', 0, '2023-08-19', '', None),
                ('Arjun Gupta', 45, 'Male', '9835787235', 'Ischemic Stroke', 1, '2022-03-27', '', None),
                ('Sneha Shah', 35, 'Female', '9846897346', 'Gastritis', 0, '2024-02-08', '', None),
                ('Rahul Rao', 55, 'Male', '9857907457', 'Heart Attack', 1, '2021-04-02', '', None),
                ('Divya Mehta', 28, 'Female', '9868017568', 'Influenza', 0, '2023-09-25', '', None),
                ('Vikram Kumar', 60, 'Male', '9879127679', 'CKD', 1, '2020-01-19', '', None),
                ('Priya Singh', 38, 'Female', '9880237780', 'Depression', 1, '2022-10-13','',None)
            ]

            cur.executemany(
                """
                INSERT INTO patients
                (name, age, gender, phone, disease, chronic, admission_date, notes, followup_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                sample,
            )

    conn.commit()
    conn.close()


DISEASES = sorted(
    list(
        {
            "Hypertension",
            "Diabetes",
            "Coronary Artery Disease",
            "Asthma",
            "Chronic Obstructive Pulmonary Disease",
            "COPD",
            "Pneumonia",
            "Bronchitis",
            "Influenza",
            "Common Cold",
            "COVID-19",
            "SARS-CoV-2 Infection",
            "Tuberculosis",
            "Hepatitis A",
            "Hepatitis B",
            "Hepatitis C",
            "HIV/AIDS",
            "Malaria",
            "Dengue",
            "Typhoid",
            "Cholera",
            "Urinary Tract Infection",
            "UTI",
            "Kidney Stones",
            "Chronic Kidney Disease",
            "CKD",
            "Gastritis",
            "Peptic Ulcer",
            "Gastroesophageal Reflux Disease",
            "GERD",
            "Irritable Bowel Syndrome",
            "IBS",
            "Celiac Disease",
            "Appendicitis",
            "Pancreatitis",
            "Stroke",
            "Ischemic Stroke",
            "Hemorrhagic Stroke",
            "Migraine",
            "Tension Headache",
            "Epilepsy",
            "Seizure Disorder",
            "Parkinson's Disease",
            "Alzheimer's Disease",
            "Dementia",
            "Multiple Sclerosis",
            "Rheumatoid Arthritis",
            "Osteoarthritis",
            "Gout",
            "Anemia",
            "Iron Deficiency Anemia",
            "Leukemia",
            "Lymphoma",
            "Breast Cancer",
            "Lung Cancer",
            "Colorectal Cancer",
            "Prostate Cancer",
            "Skin Cancer",
            "Basal Cell Carcinoma",
            "Melanoma",
            "Psoriasis",
            "Eczema",
            "Dermatitis",
            "Depression",
            "Anxiety Disorder",
            "Bipolar Disorder",
            "Schizophrenia",
            "Obsessive Compulsive Disorder",
            "OCD",
            "Autism Spectrum Disorder",
            "Attention Deficit Hyperactivity Disorder",
            "ADHD",
            "Hypothyroidism",
            "Hyperthyroidism",
            "Goiter",
            "Polycystic Ovary Syndrome",
            "PCOS",
            "Endometriosis",
            "Infertility",
            "Preeclampsia",
            "Gestational Diabetes",
            "Premature Birth Complication",
            "Chickenpox",
            "Measles",
            "Mumps",
            "Rubella",
            "Whooping Cough",
            "Pertussis",
            "Ear Infection",
            "Otitis Media",
            "Sinusitis",
            "Allergic Rhinitis",
            "Allergy",
            "Food Allergy",
            "Anaphylaxis",
            "Liver Cirrhosis",
            "Fatty Liver Disease",
            "Nonalcoholic Fatty Liver Disease",
            "NAFLD",
            "Alcoholic Liver Disease",
            "Peripheral Arterial Disease",
            "Varicose Veins",
            "Deep Vein Thrombosis",
            "DVT",
            "Pulmonary Embolism",
            "Sepsis",
            "Cellulitis",
            "Skin Infection",
            "Appendicitis",
            "Acute Respiratory Distress Syndrome",
            "ARDS",
            "Acute Bronchiolitis",
            "Bronchiectasis",
            "Eye Infection",
            "Conjunctivitis",
            "Glaucoma",
            "Cataract",
            "Periodontal Disease",
            "Tooth Decay",
            "Oral Cancer",
            "Laryngitis",
            "Thyroid Cancer",
            "Pancreatic Cancer",
            "Endocarditis",
            "Myocarditis",
            "Arrhythmia",
            "Atrial Fibrillation",
            "Heart Failure",
            "Congestive Heart Failure",
            "Heart Attack",
            "Myocardial Infarction",
            "Rheumatic Fever",
            "Sickle Cell Disease",
            "Hemophilia",
            "Vitiligo",
            "Nutritional Deficiency",
            "Obesity",
            "Metabolic Syndrome",
        }
    )
)

GENDER_CHOICES = ["Male", "Female", "Other"]
TYPE_CHOICES = ["Chronic", "Acute"]
SEARCH_FIELDS = [
    "ID",
    "Name",
    "Age",
    "Gender",
    "Phone",
    "Disease",
    "Type",
    "Admission Date",
]


def set_password(plain):
    salt = os.urandom(16).hex()
    digest = hashlib.sha256((salt + plain).encode()).hexdigest()
    json.dump({"salt": salt, "hash": digest}, open(CFG_FILE, "w"))
    try:
        os.chmod(CFG_FILE, 0o600)
    except Exception:
        pass


def verify_password(plain):
    if not os.path.exists(CFG_FILE):
        return False
    try:
        obj = json.load(open(CFG_FILE))
        salt = obj.get("salt", "")
        expected = obj.get("hash", "")
        return hashlib.sha256((salt + plain).encode()).hexdigest() == expected
    except Exception:
        return False


class AutocompleteEntry(ttk.Entry):
    def __init__(
        self, parent, suggestions=None, max_suggestions=8, textvariable=None, **kwargs
    ):
        if isinstance(textvariable, tk.StringVar):
            self.var = textvariable
            kwargs["textvariable"] = self.var
            super().__init__(parent, **kwargs)
        else:
            super().__init__(parent, textvariable=textvariable, **kwargs)
            tv_name = self.cget("textvariable")
            if tv_name:
                try:
                    val = self.getvar(tv_name)
                    self.var = tk.StringVar(value=val)
                    self.config(textvariable=self.var)
                except Exception:
                    self.var = tk.StringVar()
                    self.config(textvariable=self.var)
            else:
                self.var = tk.StringVar()
                self.config(textvariable=self.var)

        self.parent = parent
        self.suggestions = suggestions or []
        self.max_suggestions = max_suggestions

        try:
            self.var.trace_add("write", lambda *a: self._on_change())
        except Exception:
            self.var.trace("w", lambda *a: self._on_change())

        self.popup = None
        self.listbox = None
        self.selection_index = -1

        self.bind("<Down>", self._on_down)
        self.bind("<Up>", self._on_up)
        self.bind("<Return>", self._on_return)
        self.bind("<Escape>", self._hide_popup)

    def _on_change(self):
        text = self.var.get().strip()
        if not text:
            self._hide_popup()
            return
        matches = self._find_matches(text)
        if matches:
            self._show_popup(matches)
        else:
            self._hide_popup()

    def _find_matches(self, text):
        t = text.lower()
        results = []
        for s in self.suggestions:
            if t in s.lower():
                results.append(s)
                if len(results) >= self.max_suggestions:
                    break
        return results

    def _show_popup(self, matches):
        self._hide_popup()
        self.popup = tk.Toplevel(self)
        self.popup.wm_overrideredirect(True)
        self.popup.attributes("-topmost", True)
        self.listbox = tk.Listbox(
            self.popup,
            height=min(len(matches), self.max_suggestions),
            exportselection=False,
            font=("Helvetica", 12),
        )
        for m in matches:
            self.listbox.insert("end", m)
        self.listbox.pack(side="left", fill="both", expand=True)
        self.listbox.bind("<<ListboxSelect>>", self._on_list_select)
        self.listbox.bind("<Button-1>", self._on_click)
        try:
            x = self.winfo_rootx()
            y = self.winfo_rooty() + self.winfo_height()
            self.popup.geometry(f"+{x}+{y}")
            self.popup.update_idletasks()
            self.popup.wm_geometry(
                f"{self.winfo_width()}x{self.listbox.winfo_reqheight()}+{x}+{y}"
            )
        except Exception:
            pass
        self.selection_index = -1

    def _hide_popup(self, *args):
        if self.popup:
            try:
                self.popup.destroy()
            except Exception:
                pass
            self.popup = None
            self.listbox = None
            self.selection_index = -1

    def _on_list_select(self, event):
        if not self.listbox:
            return
        idxs = self.listbox.curselection()
        if not idxs:
            return
        val = self.listbox.get(idxs[0])
        self.var.set(val)
        self._hide_popup()
        try:
            self.icursor("end")
        except Exception:
            pass

    def _on_click(self, event):
        self._on_list_select(event)

    def _on_down(self, event):
        if not self.listbox:
            return "break"
        size = self.listbox.size()
        if size == 0:
            return "break"
        self.selection_index = (self.selection_index + 1) % size
        self.listbox.selection_clear(0, "end")
        self.listbox.selection_set(self.selection_index)
        self.listbox.activate(self.selection_index)
        return "break"

    def _on_up(self, event):
        if not self.listbox:
            return "break"
        size = self.listbox.size()
        if size == 0:
            return "break"
        self.selection_index = (self.selection_index - 1) % size
        self.listbox.selection_clear(0, "end")
        self.listbox.selection_set(self.selection_index)
        self.listbox.activate(self.selection_index)
        return "break"

    def _on_return(self, event):
        if self.listbox and self.listbox.curselection():
            self._on_list_select(event)
            return "break"
        return


class PRMSApp(tk.Tk):
    def _toggle_compact_ai(self, content_frame, header_btn):
        if getattr(self, "ai_open", False):
            content_frame.pack_forget()
            header_btn.config(text="▶ AI Tools")
            self.ai_open = False
        else:
            content_frame.pack(fill="x", pady=(2, 0))
            header_btn.config(text="▼ AI Tools")
            self.ai_open = True

            # --- Summarize Notes ---

    def summarize_notes(text, max_sentences=3):
        if not text or not text.strip():
            return ""

        import re

        # split into sentences (keep punctuation)
        sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
        if not sents:
            return ""

        # if already short, just return original trimmed text (or first sentences)
        if len(sents) <= max_sentences:
            return " ".join(sents)

        # build word frequency excluding common stopwords
        stop = {
            "the",
            "and",
            "is",
            "in",
            "to",
            "of",
            "a",
            "an",
            "for",
            "on",
            "with",
            "that",
            "this",
            "it",
            "was",
            "were",
            "are",
            "by",
            "as",
            "be",
            "have",
            "has",
            "had",
            "at",
            "from",
            "or",
            "not",
            "i",
            "we",
            "you",
            "he",
            "she",
            "they",
            "their",
            "them",
            "but",
            "if",
            "so",
            "than",
            "then",
        }
        words = re.findall(r"\w+", text.lower())
        freqs = {}
        for w in words:
            if w in stop:
                continue
            freqs[w] = freqs.get(w, 0) + 1

        # score sentences
        scored = []
        for i, s in enumerate(sents):
            toks = re.findall(r"\w+", s.lower())
            score = sum(freqs.get(t, 0) for t in toks)
            scored.append((score, i, s))

        # choose top N sentences, then sort by original index to keep coherence
        top = sorted(scored, key=lambda x: (-x[0], x[1]))[:max_sentences]
        top_sorted = sorted(top, key=lambda x: x[1])
        summary = " ".join(s for _, _, s in top_sorted)

        # ensure it ends with a period for neatness
        if summary and summary[-1] not in ".!?":
            summary = summary + "."

        return summary

    # --- Similar Patients ---
    def _ui_similar_patients(self):
        import ai_helpers

        age = self.age_var.get().strip()
        disease = self.disease_var.get().strip()

        if not age or not disease:
            messagebox.showwarning(
                "Similar Patients", "Enter Age and Disease first.", parent=self
            )
            return

        rows = ai_helpers.find_similar_patients(age, disease)

        if not rows:
            messagebox.showinfo(
                "Similar Patients", "No similar patients found.", parent=self
            )
            return
        msg = ""
        for r in rows:
            msg += f"{r[0]} | Age {r[1]} | {r[4]}\n"
            messagebox.showinfo("Similar Patients", msg, parent=self)

    def _ui_patient_history(self):
        name = self.name_var.get().strip()
        phone = self.phone_var.get().strip()

        if not name or not phone:
            messagebox.showwarning(
                "Patient History",
                "Enter patient name and phone number first.",
                parent=self,
            )
            return

        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            """
                SELECT admission_date, disease
                FROM patients
                WHERE LOWER(name) = LOWER(?)
                AND phone = ?
                ORDER BY admission_date
            """,
            (name, phone),
        )

        rows = cur.fetchall()
        conn.close()

        if not rows:
            messagebox.showinfo(
                "Patient History",
                "No visit history found for this patient.",
                parent=self,
            )
            return

        msg = ""
        for i, (adm, disease) in enumerate(rows, start=1):
            msg += f"Visit {i}: {adm} | {disease}\n"

        messagebox.showinfo("Patient Visit History", msg, parent=self)

    def update_risk_display(self):
        import ai_helpers

        age = self.age_var.get().strip()
        disease = self.disease_var.get().strip()
        if not disease:
            # clear display until a disease is selected
            try:
                self.risk_label.config(text="Risk: —", foreground="black")
                self.admission_label.config(text="Admission: —")
            except Exception:
                pass
            return
        chronic_flag = 1 if self.chronic_var.get() == "Chronic" else 0
        risk = ai_helpers.risk_flag(age, disease, chronic_flag)
        self.risk_label.config(
            text=f"Risk: {risk}",
            foreground=(
                "red" if risk == "High" else "orange" if risk == "Medium" else "green"
            ),
        )
        try:
            rec = ai_helpers.admission_recommendation(
                age, disease, chronic_flag, self.notes_text.get("1.0", "end")
            )
            self.admission_label.config(text=f"Admission: {rec}")
        except Exception:
            pass

        self.update_ai_insight()

        import ai_helpers

    def update_ai_insight(self):
        try:
            import ai_helpers

            age = self.age_var.get()
            disease = self.disease_var.get()
            dtype = self.chronic_var.get()
            adm = self.adm_var.get()

            if not age or not disease or not dtype or not adm:
                self.ai_insight_label.config(text="AI Insight: —", foreground="#777")
                return

            chronic_flag = 1 if dtype == "Chronic" else 0

            msg, color = ai_helpers.ai_insight(age, disease, chronic_flag)

            # ---- FOLLOW-UP DATE (DISPLAY ONLY) ----
            days = ai_helpers.suggest_followup_days(disease)
            fdate = ai_helpers.suggest_followup_date(adm, disease)

            if fdate:
                msg += f" | Follow-up in {days} days ({fdate})"

            self.ai_insight_label.config(text="AI Insight: " + msg, foreground=color)

        except Exception as e:
            print("AI Insight error:", e)
            self.ai_insight_label.config(text="AI Insight: —", foreground="#777")

    def _guess_type(self):
        import ai_helpers

        d = self.disease_var.get().strip()
        guess = ai_helpers.guess_type(d)
        if guess:
            self.chronic_var.set(guess)

    def __init__(self):
        super().__init__()
        self.title(APP_NAME)
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))
        BG_MAIN = "#f4f6fb"
        self.configure(background=BG_MAIN)

        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self._configure_styles()
        init_db()

        today = datetime.date.today()
        self.sidebar_year = today.year
        self.sidebar_month = today.month
        self._sidebar_cal_frame = None

        self._build_ui()
        self.load_records()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self._update_clock()

    def _configure_styles(self):
        self.H1 = ("Segoe UI", 22, "bold")
        self.BIG = ("Segoe UI", 16)
        self.MED = ("Segoe UI", 13)
        self.SM = ("Segoe UI", 11)

        # sidebar
        self.style.configure("Sidebar.TFrame", background=SIDEBAR_BLUE)
        self.style.configure("Main.TFrame", background="#f7f7fb")
        self.style.configure("Card.TFrame", background="#ffffff")
        self.style.configure("Header.TLabel", font=self.H1, background="#f7f7fb")
        self.style.configure(
            "Muted.TLabel", background="#f7f7fb", foreground="#444444", font=self.MED
        )

        # Tree / table styles - larger, clearer fonts
        self.style.configure("Treeview", font=self.MED, rowheight=44)
        self.style.configure("Treeview.Heading", font=("Segoe UI", 13, "bold"))

        # selection color
        self.style.map(
            "Treeview",
            background=[("selected", "#2563eb")],
            foreground=[("selected", "white")],
        )

    def _build_ui(self):
        container = ttk.Frame(self, style="Main.TFrame")
        container.pack(fill="both", expand=True)

        container.columnconfigure(1, weight=1)
        container.rowconfigure(1, weight=1)

        sidebar = ttk.Frame(container, style="Sidebar.TFrame", width=300)
        sidebar.grid(row=0, column=0, sticky="nsw", rowspan=2)
        sidebar.grid_propagate(False)
        self._build_sidebar(sidebar)

        header = ttk.Frame(container, style="Main.TFrame")
        header.grid(row=0, column=1, sticky="new", padx=(12, 12), pady=(12, 0))
        header.columnconfigure(0, weight=1)
        ttk.Label(header, text=APP_NAME, style="Header.TLabel").grid(
            row=0, column=0, sticky="w"
        )
        ttk.Label(
            header, text="STATUS: Connected to sqlite database ✅", style="Muted.TLabel"
        ).grid(row=1, column=0, sticky="w", pady=(6, 0))

        body = ttk.Frame(container, style="Main.TFrame")
        body.grid(row=1, column=1, sticky="nsew", padx=(12, 12), pady=(12, 12))
        body.columnconfigure(0, weight=1)
        body.rowconfigure(1, weight=1)

        form_card = ttk.Frame(body, style="Card.TFrame", padding=(24, 24, 24, 24))
        form_card.grid(row=0, column=0, sticky="ew")
        self._build_form(form_card)

        table_card = ttk.Frame(body, style="Card.TFrame", padding=(12, 12, 12, 12))
        table_card.grid(row=1, column=0, sticky="nsew")
        table_card.columnconfigure(0, weight=1)
        table_card.rowconfigure(0, weight=1)
        self._build_table(table_card)

        self.statusbar = ttk.Label(
            self,
            text=f"DB: {DB_FILE}",
            anchor="w",
            padding=(8, 8),
            background="#ffffff",
            font=self.SM,
        )
        self.statusbar.pack(side="bottom", fill="x")

        self.after(200, lambda: self._adjust_columns_responsive())

    def _check_for_graph_command(self, event=None):
        try:
            text = self.notes_text.get("1.0", "end").lower()
            # bind once to call the checker on each key release
            self.notes_text.bind("<KeyRelease>", self._check_for_graph_command)

        except Exception:
            return

        # look for graph request words
        if "graph" in text or "chart" in text or "plot" in text:
            # optional: avoid repeatedly opening the chart many times in a row
            if getattr(self, "_chart_open_recently", False):
                return
            self._chart_open_recently = True
            try:
                self._show_disease_chart()
            finally:
                # reset the flag after 2 seconds so the chart can be opened again later
                try:
                    self.after(
                        2000, lambda: setattr(self, "_chart_open_recently", False)
                    )
                except Exception:
                    # if after fails, just clear the flag immediately
                    self._chart_open_recently = False

    def _show_disease_chart(self):
        

        # ✅ USE SAME DB AS MAIN APP
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()

        cur.execute(
            """
           SELECT disease, COUNT(*)
           FROM patients
           WHERE disease IS NOT NULL AND disease != ''
           GROUP BY disease
           ORDER BY COUNT(*) DESC
        """
        )
        data = cur.fetchall()
        conn.close()

        if not data:
            messagebox.showinfo("Chart", "No data to plot.")
            return

        diseases = [r[0] for r in data]
        counts = [r[1] for r in data]

        plt.figure(figsize=(10, 5))
        plt.bar(diseases, counts)
        plt.xticks(rotation=45, ha="right")
        plt.ylabel("Number of Patients")
        plt.title("Patient Count by Disease")
        plt.tight_layout()
        plt.show()

    def _build_sidebar(self, parent):
        try:
            self._logo_img = tk.PhotoImage(file=SIDEBAR_IMAGE)
            logo = ttk.Label(parent, image=self._logo_img, style="Sidebar.TFrame")
            logo.image = self._logo_img
            logo.pack(pady=(18, 6))
        except Exception:
            canvas = tk.Canvas(
                parent, width=160, height=160, bg=SIDEBAR_BLUE, highlightthickness=0
            )

            canvas.create_oval(16, 16, 144, 144, fill="#2f7ce0", outline="")
            canvas.create_text(80, 80, text="🏥", font=("Helvetica", 54), fill="white")
            canvas.pack(pady=(18, 6))
        sidebar = tk.Frame(parent, bg=SIDEBAR_BLUE, width=260)
        sidebar.pack(side="left", fill="y")

        dashboard_btn = ttk.Button(sidebar, text="🏠 Dashboard")
        dashboard_btn.pack(fill="x", padx=20, pady=8)

        reports_btn = ttk.Button(sidebar, text="📊 Reports", command=self.open_reports)
        reports_btn.pack(fill="x", padx=20, pady=8)

        # --- Compact collapsible AI Tools (compact buttons) ---
        self.ai_frame = ttk.Frame(sidebar)
        self.ai_frame.pack(fill="x", pady=(6, 4))
        self.ai_open = False
        self.ai_header_btn = ttk.Button(
            self.ai_frame,
            text="▶ AI Tools",
            width=12,
            command=lambda: self._toggle_compact_ai(
                self.ai_content, self.ai_header_btn
            ),
        )
        self.ai_header_btn.pack(padx=14, pady=(6, 4))
        self.ai_content = ttk.Frame(self.ai_frame)  # hidden initially
        # compact small buttons (use small width and minimal padding)
        ttk.Button(
            self.ai_content,
            text="🤖 Summary",
            width=10,
            command=lambda: getattr(self, "_ui_summarize_notes", lambda: None)(),
        ).pack(pady=2, padx=12)
        ttk.Button(
            self.ai_content,
            text="🧠 Risk",
            width=10,
            command=lambda: (
                getattr(self, "update_risk_display", lambda: None)(),
                messagebox.showinfo(
                    "Risk",
                    (
                        getattr(self, "risk_label", ttk.Label()).cget("text")
                        if hasattr(self, "risk_label")
                        else "Risk not available"
                    ),
                    parent=self,
                ),
            ),
        ).pack(pady=2, padx=12)
        ttk.Button(
            self.ai_content,
            text="👥 Similar",
            width=10,
            command=lambda: getattr(self, "_ui_similar_patients", lambda: None)(),
        ).pack(pady=2, padx=12)
        ttk.Button(
            self.ai_content, text="History", command=self._ui_patient_history
        ).pack(pady=2, padx=12)

        ttk.Button(
            self.ai_content,
            text="📊 Chart",
            width=10,
            command=lambda: getattr(self, "_show_disease_chart", lambda: None)(),
        ).pack(pady=2, padx=12)

        spacer = tk.Frame(sidebar, bg=SIDEBAR_BLUE)
        spacer.pack(expand=True, fill="both")

        self.clock_lbl = tk.Label(
            sidebar,
            text="",
            bg=SIDEBAR_BLUE,
            fg="white",
            font=("Helvetica", 16, "bold"),
        )
        self.clock_lbl.pack(side="bottom", anchor="w", padx=16, pady=(8, 4))

        csv_btn = ttk.Button(sidebar, text="⬇ Export CSV", command=self.export_csv)
        csv_btn.pack(pady=10, padx=20, fill="x")

        self._sidebar_cal_frame = tk.Frame(sidebar, bg=SIDEBAR_BLUE)
        self._sidebar_cal_frame.pack(side="bottom", anchor="w", padx=8, pady=(4, 12))
        self._render_sidebar_calendar(
            self._sidebar_cal_frame, year=self.sidebar_year, month=self.sidebar_month
        )

    def _ui_summarize_notes(self):
        try:
            import importlib
            import ai_helpers

            try:
                importlib.reload(ai_helpers)
            except Exception:
                pass

            text = self.notes_text.get("1.0", "end").strip()
            if not text:
                messagebox.showinfo("Summary", "No notes to summarize.", parent=self)
                return

            summary = ai_helpers.summarize_notes(text)

            if not summary:
                summary = "No meaningful summary could be generated."

            messagebox.showinfo("Summary", summary, parent=self)

        except Exception as e:
            messagebox.showerror(
                "Summary Error", f"Failed to summarize notes:\n{e}", parent=self
            )

    def _toggle_notes(self):
        """
        Robust notes toggle: remembers initial pack options so the notes_frame
        is restored exactly as before. Button text flips between Show/Hide.
        """
        # ensure we have a stored pack spec
        if not hasattr(self, "_notes_pack_info"):
            # default pack options used when notes were first packed
            self._notes_pack_info = {"fill": "x", "pady": (4, 4)}

        # visible -> hide
        if getattr(self, "notes_visible", True):
            try:
                self.notes_frame.pack_forget()
                self.notes_toggle_btn.config(text="Show Notes")
            except Exception:
                pass
            self.notes_visible = False
            return

        # hidden -> show (restore original pack options)
        try:
            self.notes_frame.pack(**self._notes_pack_info)
            self.notes_toggle_btn.config(text="Hide Notes")
        except Exception:
            pass
        self.notes_visible = True

    def _update_clock(self):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            self.clock_lbl.config(text="🕒 " + now)
        except Exception:
            pass
        self.after(1000, self._update_clock)

    def _render_sidebar_calendar(self, parent_frame, year=None, month=None):
        # clean
        for w in parent_frame.winfo_children():
            w.destroy()

        today = datetime.date.today()
        year = year or today.year
        month = month or today.month
        self.sidebar_year = year
        self.sidebar_month = month

        # navigation frame (fixed)
        nav_frame = tk.Frame(parent_frame, bg=SIDEBAR_BLUE, height=40)
        nav_frame.pack(anchor="w", fill="x", pady=(0, 2))
        nav_frame.pack_propagate(False)

        prev_btn = tk.Button(
            nav_frame,
            text="◀",
            bg=SIDEBAR_BLUE,
            fg="black",
            bd=0,
            font=("Helvetica", 12, "bold"),
            activebackground="#1e5b90",
            activeforeground="black",
            command=lambda: self._change_sidebar_month(-1),
        )
        prev_btn.pack(side="left", padx=(8, 4), pady=4)

        next_btn = tk.Button(
            nav_frame,
            text="▶",
            bg=SIDEBAR_BLUE,
            fg="black",
            bd=0,
            font=("Helvetica", 12, "bold"),
            activebackground="#1e5b90",
            activeforeground="black",
            command=lambda: self._change_sidebar_month(1),
        )
        next_btn.pack(side="right", padx=(4, 8), pady=4)

        hdr_frame = tk.Frame(parent_frame, bg=SIDEBAR_BLUE)
        hdr_frame.pack(anchor="w", fill="x")
        hdr = tk.Label(
            hdr_frame,
            text=f"{pycalendar.month_name[month]} {year}",
            bg=SIDEBAR_BLUE,
            fg="white",
            font=("Helvetica", 14, "bold"),
        )
        hdr.pack(side="left", padx=(6, 0))

        cal = pycalendar.monthcalendar(year, month)
        days_frame = tk.Frame(parent_frame, bg=SIDEBAR_BLUE)
        days_frame.pack(anchor="w", pady=(6, 0))
        wkds = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
        for c, wd in enumerate(wkds):
            tk.Label(
                days_frame,
                text=wd,
                bg=SIDEBAR_BLUE,
                fg="white",
                font=("Helvetica", 10, "bold"),
            ).grid(row=0, column=c, padx=2)

        for r, week in enumerate(cal, start=1):
            for c, day in enumerate(week):
                if day == 0:
                    tk.Label(days_frame, text=" ", bg=SIDEBAR_BLUE).grid(
                        row=r, column=c, padx=2, pady=1
                    )
                else:
                    lbl = tk.Label(
                        days_frame,
                        text=str(day),
                        bg="#2a66a9",
                        fg="white",
                        width=3,
                        font=("Helvetica", 11, "bold"),
                    )
                    lbl.grid(row=r, column=c, padx=2, pady=1)

                    def make_handler(d=day, yr=year, mo=month):
                        def handler(ev=None):
                            selected = datetime.date(yr, mo, d).isoformat()
                            self._open_date_action_dialog(selected)

                        return handler

                    lbl.bind("<Double-Button-1>", make_handler())

    def _change_sidebar_month(self, delta):
        m = self.sidebar_month + delta
        y = self.sidebar_year
        while m < 1:
            m += 12
            y -= 1
        while m > 12:
            m -= 12
            y += 1
        self.sidebar_month = m
        self.sidebar_year = y
        try:
            if self._sidebar_cal_frame:
                self._render_sidebar_calendar(
                    self._sidebar_cal_frame,
                    year=self.sidebar_year,
                    month=self.sidebar_month,
                )
        except Exception:
            pass

    def _open_date_action_dialog(self, selected_date_iso):

        dlg = tk.Toplevel(self)
        dlg.title("Choose action")
        dlg.transient(self)
        dlg.grab_set()
        dlg.resizable(False, False)
        dlg_bg = SIDEBAR_BLUE
        dlg.configure(bg=dlg_bg)

        lbl = tk.Label(
            dlg,
            text=f"Selected date: {selected_date_iso}",
            font=self.MED,
            bg=dlg_bg,
            fg="white",
        )
        lbl.pack(padx=12, pady=(12, 6))

        btn_frame = tk.Frame(dlg, bg=dlg_bg)
        btn_frame.pack(padx=12, pady=(6, 12))

        def set_only():
            try:
                self.adm_var.set(selected_date_iso)
            except Exception:
                pass
            dlg.grab_release()
            dlg.destroy()

        def use_only():
            try:
                self.search_var.set(selected_date_iso)
                self.search_field_var.set("Admission Date")
            except Exception:
                pass
            dlg.grab_release()
            dlg.destroy()

        def set_and_use():
            try:
                self.adm_var.set(selected_date_iso)
                self.search_var.set(selected_date_iso)
                self.search_field_var.set("Admission Date")
            except Exception:
                pass
            dlg.grab_release()
            dlg.destroy()

        b1 = tk.Button(
            btn_frame,
            text="Set as Admission Date",
            command=set_only,
            bg=self.cget("bg"),
            fg="black",
            padx=8,
            pady=6,
        )
        b1.grid(row=0, column=0, padx=6, pady=4)
        b2 = tk.Button(
            btn_frame,
            text="Use for Search",
            command=use_only,
            bg=self.cget("bg"),
            fg="black",
            padx=8,
            pady=6,
        )
        b2.grid(row=0, column=1, padx=6, pady=4)
        b3 = tk.Button(
            btn_frame,
            text="Set & Use",
            command=set_and_use,
            bg=self.cget("bg"),
            fg="black",
            padx=8,
            pady=6,
        )
        b3.grid(row=1, column=0, padx=6, pady=4)
        b4 = tk.Button(
            btn_frame,
            text="Cancel",
            command=lambda: (dlg.grab_release(), dlg.destroy()),
            bg=self.cget("bg"),
            fg="black",
            padx=8,
            pady=6,
        )
        b4.grid(row=1, column=1, padx=6, pady=4)

        dlg.update_idletasks()
        w = dlg.winfo_reqwidth()
        h = dlg.winfo_reqheight()
        x = self.winfo_rootx() + (self.winfo_width() - w) // 2
        y = self.winfo_rooty() + (self.winfo_height() - h) // 2
        dlg.geometry(f"{w}x{h}+{x}+{y}")

    def _build_form(self, parent):
        row0 = ttk.Frame(parent)
        row0.pack(fill="x", pady=(0, 10))
        ttk.Label(row0, text="Full Name", font=self.MED).grid(
            row=0, column=0, sticky="w"
        )
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(
            row0, textvariable=self.name_var, font=self.BIG, width=40
        )
        self.name_entry.grid(row=1, column=0, sticky="w", padx=(0, 12))

        ttk.Label(row0, text="Age", font=self.MED, foreground="#374151").grid(
            row=0, column=1, sticky="w"
        )
        self.age_var = tk.StringVar()
        self.age_entry = ttk.Entry(
            row0, textvariable=self.age_var, width=8, font=self.BIG
        )
        self.age_entry.grid(row=1, column=1, sticky="w")
        vcmd = (self.register(self._validate_age), "%P")
        self.age_entry.config(validate="key", validatecommand=vcmd)
        self.age_var.trace_add("write", lambda *a: self.update_risk_display())

        row1 = ttk.Frame(parent)
        row1.pack(fill="x", pady=(0, 10))
        ttk.Label(row1, text="Gender", font=self.MED).grid(row=0, column=0, sticky="w")
        self.gender_var = tk.StringVar()
        gender_combo = ttk.Combobox(
            row1,
            textvariable=self.gender_var,
            values=GENDER_CHOICES,
            width=14,
            state="readonly",
            font=self.BIG,
        )
        gender_combo.grid(row=1, column=0, sticky="w", padx=(0, 12))

        ttk.Label(row1, text="Phone 📞", font=self.MED).grid(
            row=0, column=1, sticky="w"
        )
        self.phone_var = tk.StringVar()
        vcmd_phone = (self.register(self._vcmd_phone), "%P")
        self.phone_entry = ttk.Entry(
            row1,
            textvariable=self.phone_var,
            font=self.BIG,
            width=20,
            validate="key",
            validatecommand=vcmd_phone,
        )
        self.phone_entry.grid(row=1, column=1, sticky="w")

        row2 = ttk.Frame(parent)
        row2.pack(fill="x", pady=(0, 10))
        ttk.Label(row2, text="Disease 🧾", font=self.MED).grid(
            row=0, column=0, sticky="w"
        )
        self.disease_var = tk.StringVar()
        self.disease_entry = AutocompleteEntry(
            row2, suggestions=DISEASES, textvariable=self.disease_var, font=self.BIG
        )
        self.disease_entry.grid(row=1, column=0, sticky="w", padx=(0, 12))
        self.disease_entry.var.trace_add("write", lambda *a: self._guess_type())
        self.disease_entry.var.trace_add("write", lambda *a: self.update_risk_display())

        ttk.Label(row2, text="Type", font=self.MED).grid(row=0, column=1, sticky="w")
        self.chronic_var = tk.StringVar(value="")
        chronic_choice = ttk.Combobox(
            row2,
            textvariable=self.chronic_var,
            values=TYPE_CHOICES,
            width=12,
            state="readonly",
            font=self.BIG,
        )
        self.chronic_var.trace_add("write", lambda *a: self.update_risk_display())

        chronic_choice.grid(row=1, column=1, sticky="w")

        row3 = ttk.Frame(parent)
        row3.pack(fill="x", pady=(0, 10))
        ttk.Label(
            row3,
            text="Admission Date (double-click a date on left calendar) 📅",
            font=self.MED,
        ).grid(row=0, column=0, sticky="w")
        self.adm_var = tk.StringVar(value=datetime.date.today().isoformat())
        ttk.Entry(row3, textvariable=self.adm_var, font=self.BIG, width=20).grid(
            row=1, column=0, sticky="w", pady=(6, 0)
        )

        btn_row = ttk.Frame(parent)
        btn_row.pack(fill="x", pady=(12, 0))

        # create a toolbar frame so CRUD buttons have their own row
        toolbar = ttk.Frame(parent)
        toolbar.pack(fill="x", pady=(12, 0))

        # left side buttons (Add/Update/Delete/Clear)
        btn_left = ttk.Frame(toolbar)
        btn_left.pack(side="left", padx=(0, 8), fill="x", expand=False)
        add_btn = ttk.Button(btn_left, text="➕ Add New", command=self.add_record)
        add_btn.pack(side="left", padx=6)
        upd_btn = ttk.Button(btn_left, text="✏️ Update", command=self.update_record)
        upd_btn.pack(side="left", padx=6)
        del_btn = ttk.Button(btn_left, text="🗑️ Delete", command=self.delete_record)
        del_btn.pack(side="left", padx=6)
        clear_btn = ttk.Button(btn_left, text="🧹 Clear", command=self._clear_all)
        clear_btn.pack(side="left", padx=6)

        # AI buttons area
        ai_btns = ttk.Frame(btn_row)
        ai_btns.pack(side="left", padx=(12, 8))
        self.risk_label = ttk.Label(ai_btns, text="Risk:", font=self.SM)
        self.risk_label.pack(side="left", padx=10)

        self.admission_label = ttk.Label(ai_btns, text="Admission:", font=self.SM)
        self.admission_label.pack(side="left", padx=8)

        # ---- AI Insight row (NEW LINE, BELOW) ----
        ai_insight_frame = ttk.Frame(parent)
        ai_insight_frame.pack(fill="x", pady=(4, 0))

        self.ai_insight_label = ttk.Label(
            ai_insight_frame,
            text="AI Insight:—",
            font=("Helvetica", 10, "italic"),
            foreground="#444",
            wraplength=900,  # VERY IMPORTANT (prevents overflow)
            anchor="w",
            justify="left",
        )
        self.ai_insight_label.pack(side="left", padx=24)

        # Notes / Symptoms - single, consistent block (placed under the main form)
        self.notes_frame = ttk.Frame(parent)
        # allow the text widget inside notes_frame to expand
        self.notes_frame.columnconfigure(0, weight=1)
        self.notes_frame.rowconfigure(1, weight=1)

        self.notes_toggle_btn = ttk.Button(
            parent, text="Hide Notes", command=self._toggle_notes
        )
        self.notes_toggle_btn.pack(anchor="e", pady=(6, 0))
        self.notes_visible = False
        self.notes_toggle_btn.config(text="Show Notes")
        self.notes_frame.pack_forget()

        # remember how we packed notes so toggle can restore identical layout
        self._notes_pack_info = {"fill": "x", "pady": (12, 12)}
        # self.notes_frame.pack(**self._notes_pack_info)
        ttk.Label(self.notes_frame, text="Notes / Symptoms:", font=self.MED).grid(
            row=0, column=0, sticky="w"
        )
        self.notes_text = tk.Text(self.notes_frame, height=4, wrap="word")
        self.notes_text.grid(row=1, column=0, sticky="nsew", padx=(0, 6))
        # bind to detect doctor typing graph/chart commands
        try:
            self.notes_text.bind(
                "<KeyRelease>", lambda e: self._check_for_graph_command()
            )
        except Exception:
            pass
        # allow the text widget inside notes_frame to expand

        # Search bar (right side)
        search_frame = ttk.Frame(btn_row)
        search_frame.pack(side="right", padx=(0, 12), anchor="e")

        self.search_field_var = tk.StringVar(value="Name")
        self.search_field_combo = ttk.Combobox(
            search_frame,
            textvariable=self.search_field_var,
            values=SEARCH_FIELDS,
            width=14,
            state="readonly",
            font=self.MED,
        )
        self.search_field_combo.pack(side="left", padx=(0, 8))

        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(
            search_frame, textvariable=self.search_var, width=28, font=self.BIG
        )
        self.search_entry.pack(side="left", padx=(0, 8))
        self.search_entry.bind("<Return>", lambda e: self.perform_search())

        search_btn = ttk.Button(
            search_frame, text="🔍 Search", command=self.perform_search
        )
        search_btn.pack(side="left", padx=(0, 6))
        search_clear_btn = ttk.Button(search_frame, text="✖", command=self.clear_search)
        search_clear_btn.pack(side="left")

    def _vcmd_phone(self, new_value):
        # allow empty or up to 10 digits while typing; final validation occurs on save
        if new_value == "":
            return True
        if new_value.isdigit() and len(new_value) <= 10:
            return True
        return False

    def _validate_age(self, proposed_value: str) -> bool:
        """
        Tkinter validatecommand: allow empty or up to 3 digits only (0-120 later checked).
        Used with validate='key' and '%P' to get the would-be value.
        """
        if proposed_value == "":
            return True
        if not proposed_value.isdigit():
            return False
        # limit typed length to 3 characters (you can change to 2 if you prefer)
        return len(proposed_value) <= 3

    def _clear_all(self):
        self.clear_form()
        try:
            self.search_var.set("")
            self.search_field_var.set("")
            self.gender_var.set("")
            self.chronic_var.set("")
        except Exception:
            pass
        try:
            self.load_records()
        except Exception as e:
            print("Warning: failed to reload records after clear:", e)

    def export_csv(self):
        try:
            # ask where to save
            fpath = filedialog.asksaveasfilename(
                title="Export CSV",
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            )
            if not fpath:
                return
            # gather headers from tree headings
            cols = [self.tree.heading(c)["text"] for c in self.tree["columns"]]
            with open(fpath, "w", newline="", encoding="utf-8") as fh:
                writer = csv.writer(fh)
                writer.writerow(cols)
                for iid in self.tree.get_children():
                    vals = self.tree.item(iid)["values"]
                    writer.writerow(vals)
            messagebox.showinfo(
                "Export CSV",
                f"Exported {len(self.tree.get_children())} rows to:\n{fpath}",
                parent=self,
            )

        except Exception as e:
            messagebox.showerror("Export CSV", str(e), parent=self)

    def _build_table(self, parent):
        cols = (
            "id",
            "name",
            "age",
            "gender",
            "phone",
            "disease",
            "type",
            "admission_date",
        )
        self.tree = ttk.Treeview(
            parent, columns=cols, show="headings", selectmode="browse", height=12
        )

        self.tree.tag_configure("oddrow", background="#f7f7fb")
        self.tree.tag_configure("evenrow", background="#ffffff")

        initial = {
            "id": 80,
            "name": 360,
            "age": 110,
            "gender": 140,
            "phone": 180,
            "disease": 260,
            "type": 140,
            "admission_date": 170,
        }
        for c in cols:
            heading = c.replace("_", " ").title()
            self.tree.heading(c, text=heading)
            self.tree.column(c, width=initial.get(c, 120), anchor="w", stretch=True)
            self.tree.grid(row=0, column=0, sticky="nsew")
        parent.columnconfigure(0, weight=1)  # tree column stretches
        parent.rowconfigure(0, weight=1)
        parent.rowconfigure(1, weight=0)

        vsb = ttk.Scrollbar(parent, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        vsb.grid(row=0, column=1, sticky="ns", padx=(6, 2))
        vsb.grid(row=0, column=1, sticky="ns", padx=(6, 2))
        # Horizontal scrollbar
        hsb = ttk.Scrollbar(parent, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=hsb.set)
        hsb.grid(row=1, column=0, sticky="ew", pady=(2, 0))

        self.tree.bind("<Double-1>", self.on_tree_double)
        parent.bind("<Configure>", lambda e: self._adjust_columns_responsive())

    def _adjust_columns_responsive(self):
        try:
            total_width = self.tree.winfo_width()
            if total_width <= 100:
                return
            weights = {
                "id": 0.06,
                "name": 0.26,
                "age": 0.07,
                "gender": 0.08,
                "phone": 0.16,
                "disease": 0.22,
                "type": 0.08,
                "admission_date": 0.13,
            }
            s = sum(weights.values())
            for col, w in weights.items():
                width = max(50, int(total_width * (w / s)))
                self.tree.column(col, width=width)
        except Exception:
            pass

    def load_records(self, where=None, params=()):
        for r in self.tree.get_children():
            self.tree.delete(r)
        conn = get_conn()
        cur = conn.cursor()
        q = "SELECT id, name, age, gender, phone, disease, chronic, admission_date FROM patients"
        if where:
            q += " WHERE " + where
        q += " ORDER BY id"
        cur.execute(q, params)
        rows = cur.fetchall()
        i = 0
        for row in rows:
            _id, name, age, gender, phone, disease, chronic, adm = row
            type_label = "Chronic" if chronic == 1 else "Acute"
            tag = "oddrow" if i % 2 == 0 else "evenrow"
            self.tree.insert(
                "",
                "end",
                iid=str(_id),
                values=(
                    _id,
                    name,
                    age or "",
                    gender or "",
                    phone or "",
                    disease or "",
                    type_label,
                    adm or "",
                ),
                tags=(tag,),
            )
            i += 1
        conn.close()
        self._update_status()

    def _update_status(self):
        total = len(self.tree.get_children())
        self.statusbar.config(text=f"DB: {DB_FILE} · Rows: {total}")

    def clear_form(self):
        """Clear inputs and ensure autocomplete widget cleared and popup hidden."""
        try:
            self.name_var.set("")
            self.age_var.set("")
            self.phone_var.set("")
            try:
                self.disease_var.set("")
            except Exception:
                pass
            try:
                if hasattr(self, "disease_entry") and hasattr(
                    self.disease_entry, "var"
                ):
                    self.disease_entry.var.set("")
                    if (
                        hasattr(self.disease_entry, "popup")
                        and self.disease_entry.popup
                    ):
                        try:
                            self.disease_entry._hide_popup()
                        except Exception:
                            try:
                                self.disease_entry.popup.destroy()
                            except Exception:
                                pass
            except Exception:
                pass
            # chronic/type intentionally cleared by caller when needed
            self.adm_var.set(datetime.date.today().isoformat())
            for iid in self.tree.get_children():
                self.tree.item(iid, tags=())
                self.tree.tag_configure("match", background="")
        except Exception as exc:
            print("Warning: clear_form encountered an error:", exc)
        # Reset AI Insight
        # Clear AI Insight
        try:
            self.ai_insight_label.config(text="AI Insight: —", foreground="#777")
        except:
            pass
        # clear Notes / Symptoms text box
        self.notes_text.delete("1.0", "end")

    def clear_search(self):
        try:
            self.search_var.set("")
            self.search_field_var.set("")
        except Exception:
            pass
        self.load_records()

    def _validate_phone(self, phone):
        return phone.isdigit() and len(phone) == 10

    def _validate_name_strict(self, name):
        # Reject if any digit in name; require at least one alphabetic character.
        if any(ch.isdigit() for ch in name):
            return False, "Name must not contain digits."
        if not any(ch.isalpha() for ch in name):
            return False, "Name must contain alphabetic characters."
        return True, ""

    def _validate_disease_strict(self, disease):
        # Require exact match with one of DISEASES (case-insensitive match allowed)
        if not disease:
            return False, "Disease is required."
        for d in DISEASES:
            if d.lower() == disease.lower():
                return True, d  # return canonical form
        return False, "Disease must be chosen from suggestions (select one)."

    def add_record(self):
        """Add with validation and duplicate-check guard."""
        try:
            name = self.name_var.get().strip()
            age_str = self.age_var.get().strip()
            gender = self.gender_var.get().strip()
            phone = self.phone_var.get().strip()

            # disease: prefer external var, fallback to widget.get()
            try:
                disease = self.disease_var.get().strip()
            except Exception:
                disease = ""
            if not disease and hasattr(self, "disease_entry"):
                try:
                    disease = self.disease_entry.get().strip()
                except Exception:
                    disease = disease or ""

            chronic = self.chronic_var.get().strip()
            adm = self.adm_var.get().strip()

            if not name:
                messagebox.showerror(
                    "Validation error", "Name is required.", parent=self
                )
                return

            ok_name, reason = self._validate_name_strict(name)
            if not ok_name:
                messagebox.showerror("Validation error", reason, parent=self)
                return

            if gender not in ("Male", "Female", "Other"):
                messagebox.showerror(
                    "Validation error",
                    "Please select a gender: Male / Female / Other.",
                    parent=self,
                )
                return

            if age_str:
                try:
                    age_val = int(age_str)
                    if age_val <= 0 or age_val > 120:
                        messagebox.showerror(
                            "Validation error",
                            "Age must be between 1 and 120.",
                            parent=self,
                        )
                        return
                    age = age_val
                except ValueError:
                    messagebox.showerror(
                        "Validation error", "Age must be a valid integer.", parent=self
                    )
                    return
            else:
                age = None

            if phone:
                if not self._validate_phone(phone):
                    messagebox.showerror(
                        "Validation error",
                        "Phone number must be exactly 10 digits (digits only).",
                        parent=self,
                    )
                    return

            ok_disease, d_or_msg = self._validate_disease_strict(disease)
            if not ok_disease:
                messagebox.showerror("Validation error", d_or_msg, parent=self)
                return
            disease_canonical = d_or_msg

            if chronic not in TYPE_CHOICES:
                messagebox.showerror(
                    "Validation error",
                    f"Type must be one of: {', '.join(TYPE_CHOICES)}.",
                    parent=self,
                )
                return
            chronic_flag = 1 if chronic == "Chronic" else 0

            if adm:
                # --- Clean/validate admission date ---
                # --- Clean/validate admission date (normalize) ---
                adm = adm.strip() if isinstance(adm, str) else adm
                from datetime import datetime

                date_valid = True
                try:
                    # ensure the value has correct format YYYY-MM-DD
                    if adm:
                        datetime.strptime(adm, "%Y-%m-%d")
                    else:
                        date_valid = False
                except Exception:
                    date_valid = False

                if not date_valid:
                    # Option A: warn and continue (current behavior)
                    messagebox.showwarning(
                        "Warning",
                        f"Admission date '{adm}' is invalid or empty. Expected YYYY-MM-DD. Proceeding anyway.",
                        parent=self,
                    )
            # Option B (strict): stop saving
            # messagebox.showerror("Invalid date", "Admission date must be YYYY-MM-DD", parent=self); return

            # --- Unified duplicate detection (phone strong match + similar name+age+disease) ---
            try:
                conn = get_conn()
                cur = conn.cursor()
                dup_list = []

                # 1) Strong phone match (exact)
                if phone:
                    cur.execute(
                        "SELECT id, name, age, disease, admission_date FROM patients WHERE phone = ? LIMIT 5",
                        (phone,),
                    )
                    for r in cur.fetchall():
                        dup_list.append(
                            {
                                "type": "phone",
                                "id": r[0],
                                "text": f"{r[1]} | age {r[2]} | {r[3]} | adm {r[4]}",
                            }
                        )

                # 2) Similar records: lower(name) + disease + age (if age provided)
                if name and disease_canonical:
                    age_param = age if age is not None else -1
                    cur.execute(
                        "SELECT id, name, phone, admission_date FROM patients "
                        "WHERE lower(name)=? AND disease=? AND (age=? OR age IS NULL) LIMIT 10",
                        (name.lower(), disease_canonical, age_param),
                    )
                for r in cur.fetchall():
                    dup_list.append(
                        {
                            "type": "similar",
                            "id": r[0],
                            "text": f"{r[1]} | phone {r[2]} | adm {r[3]}",
                        }
                    )

                conn.close()

                if dup_list:
                    # Build the human-friendly lines list for popup
                    lines = []
                    for d in dup_list:
                        prefix = "[PHONE]" if d["type"] == "phone" else "[SIMILAR]"
                        lines.append(f"{prefix} {d['text']}  (id={d['id']})")

                    # custom small dialog
                    dlg = tk.Toplevel(self)
                    dlg.transient(self)
                    dlg.grab_set()
                    dlg.title("Duplicates found")
                    tk.Label(dlg, text="Duplicates found:").pack(padx=12, pady=8)
                    text = tk.Text(dlg, height=8, width=60)
                    text.insert("1.0", "\n".join(lines))
                    text.config(state="disabled")
                    text.pack(padx=12, pady=(0, 8))
                    btn_frame = tk.Frame(dlg)
                    btn_frame.pack(pady=(0, 12))

                    def on_view():
                        dlg.destroy()
                        # select first duplicate row in tree (you can adapt which id)
                        try:
                            first_id = dup_list[0]["id"]
                            if str(first_id) in self.tree.get_children():
                                self.tree.selection_set(str(first_id))
                                self.tree.see(str(first_id))
                        except Exception:
                            pass

                    def on_add():
                        dlg.result = "add"
                        dlg.destroy()

                    def on_cancel():
                        dlg.result = "cancel"
                        dlg.destroy()

                    tk.Button(btn_frame, text="View", command=on_view).pack(
                        side="left", padx=6
                    )
                    tk.Button(btn_frame, text="Add anyway", command=on_add).pack(
                        side="left", padx=6
                    )
                    tk.Button(btn_frame, text="Cancel", command=on_cancel).pack(
                        side="left", padx=6
                    )
                    self.wait_window(dlg)
                    if getattr(dlg, "result", None) == "add":
                        pass  # continue to insert
                    else:
                        return

            except Exception as e:
                # If duplicate check fails for any reason, continue but log warning
                print("Warning: duplicate check failed:", e)

            # --- Suggest followup and store it ---

            import ai_helpers

            days = ai_helpers.suggest_followup_days(disease_canonical)

            try:
                from datetime import datetime, timedelta

                followup_date = (
                    (datetime.strptime(adm, "%Y-%m-%d") + timedelta(days=days))
                    .date()
                    .isoformat()
                )
            except Exception:
                from datetime import date, timedelta

                followup_date = (date.today() + timedelta(days=days)).isoformat()

            notes = self.notes_text.get("1.0", "end").strip()
            followup_date = ai_helpers.suggest_followup_date(adm, disease_canonical)

            # insert
            try:
                conn = get_conn()
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO patients (name, age, gender, phone, disease, chronic, admission_date, notes) VALUES (?,?,?,?,?,?,?,?)",
                    (
                        name,
                        (
                            int(age)
                            if (isinstance(age, str) and age.strip().isdigit())
                            else (age if isinstance(age, int) else None)
                        ),
                        gender,
                        phone,
                        disease_canonical,
                        1 if chronic == "Chronic" else 0,
                        adm,
                        notes,
                    ),
                )
                conn.commit()
                conn.close()
            except Exception as exc:
                messagebox.showerror(
                    "Error", f"Failed to add record: {exc}", parent=self
                )
                import traceback

                traceback.print_exc(file=sys.stderr)
                try:
                    conn.close()
                except Exception:
                    pass
                return

            self.load_records()
            self.clear_form()
            messagebox.showinfo(
                "Added", f"➕ Patient added. Follow-up: {followup_date}", parent=self
            )
        except Exception as exc:
            messagebox.showerror(
                "Unexpected Error", f"Failed to add record: {exc}", parent=self
            )
            import traceback

            traceback.print_exc(file=sys.stderr)

    def perform_search(self):
        field = (self.search_field_var.get() or "").strip()
        text = (self.search_var.get() or "").strip()

        if not field:
            messagebox.showerror(
                "Search error",
                "Please select a search field from the dropdown (it was cleared).",
                parent=self,
            )
            return

        if text == "":
            self.load_records()
            return

        where = None
        params = ()

        if field == "ID":
            try:
                iid = int(text)
            except Exception:
                messagebox.showerror(
                    "Search error", "ID must be an integer.", parent=self
                )
                return
            where = "id = ?"
            params = (iid,)
        elif field == "Name":
            if any(ch.isdigit() for ch in text):
                messagebox.showerror(
                    "Search error",
                    "Name search cannot contain numbers. Enter alphabetic characters only.",
                    parent=self,
                )
                return
            where = "name LIKE ?"
            params = (f"%{text}%",)
        elif field == "Age":
            if "-" in text:
                parts = text.split("-", 1)
                try:
                    a = int(parts[0].strip())
                    b = int(parts[1].strip())
                    where = "age BETWEEN ? AND ?"
                    params = (min(a, b), max(a, b))
                except Exception:
                    messagebox.showerror(
                        "Search error",
                        "Age range invalid. Use e.g. 20-30 or a single age like 45.",
                        parent=self,
                    )
                    return
            else:
                try:
                    a = int(text)
                    where = "age = ?"
                    params = (a,)
                except Exception:
                    messagebox.showerror(
                        "Search error",
                        "Age must be a number or range (20-30).",
                        parent=self,
                    )
                    return
        elif field == "Gender":
            if text not in GENDER_CHOICES:
                allowed = ", ".join(GENDER_CHOICES)
                messagebox.showerror(
                    "Search error", f"Gender must be one of: {allowed}.", parent=self
                )
                return
            where = "LOWER(gender) = LOWER(?)"
            params = (text,)
        elif field == "Phone":
            where = "phone LIKE ?"
            params = (f"%{text}%",)
        elif field == "Disease":
            if text.isdigit():
                messagebox.showerror(
                    "Search error",
                    "Disease search cannot be numeric. Type a disease name.",
                    parent=self,
                )
                return
            where = "disease LIKE ?"
            params = (f"%{text}%",)
        elif field == "Type":
            if text not in TYPE_CHOICES:
                allowed = ", ".join(TYPE_CHOICES)
                messagebox.showerror(
                    "Search error", f"Type must be one of: {allowed}.", parent=self
                )
                return
            where = "chronic = ?"
            params = (1 if text == "Chronic" else 0,)
        elif field == "Admission Date":
            txt = text
            if len(txt) >= 4:
                where = "admission_date LIKE ?"
                params = (f"{txt}%",)
            else:
                messagebox.showerror(
                    "Search error",
                    "Enter a year-month (YYYY-MM) or full date (YYYY-MM-DD) or YYYY.",
                    parent=self,
                )
                return
        else:
            where = "(name LIKE ? OR disease LIKE ?)"
            params = (f"%{text}%", f"%{text}%")

        try:
            self.load_records(where=where, params=params)
        except Exception as e:
            messagebox.showerror(
                "Search error", f"Failed to run search: {e}", parent=self
            )

    def update_record(self):
        import ai_helpers

        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning(
                "Select", "Double-click a row to load it for update.", parent=self
            )
            return
        iid = sel[0]

        name = self.name_var.get().strip()
        if not name:
            messagebox.showerror("Validation", "Name is required.", parent=self)
            return

        ok_name, reason = self._validate_name_strict(name)
        if not ok_name:
            messagebox.showerror("Validation error", reason, parent=self)
            return

        gender = self.gender_var.get().strip()
        if gender not in GENDER_CHOICES:
            messagebox.showerror(
                "Validation",
                "Please select a gender: Male / Female / Other.",
                parent=self,
            )
            return

        age_str = self.age_var.get().strip()
        if age_str:
            age = int(age_str)
            if age <= 0 or age > 120:
                messagebox.showerror("Validation", "Age must be 1–120", parent=self)
                return
            else:
                age = None

        try:
            age = int(age_str) if age_str != "" else None
        except Exception:
            age = None

        phone = self.phone_var.get().strip()
        if phone and not self._validate_phone(phone):
            messagebox.showerror(
                "Validation",
                "Phone number must be exactly 10 digits (digits only).",
                parent=self,
            )
            return

        disease = ""
        try:
            disease = self.disease_var.get().strip()
        except Exception:
            pass
        if not disease and hasattr(self, "disease_entry"):
            try:
                disease = self.disease_entry.get().strip()
            except Exception:
                disease = disease or ""
        ok_disease, d_or_msg = self._validate_disease_strict(disease)
        if not ok_disease:
            messagebox.showerror("Validation", d_or_msg, parent=self)
            return
        disease_canonical = d_or_msg

        chronic = self.chronic_var.get().strip()
        if chronic not in TYPE_CHOICES:
            messagebox.showerror(
                "Validation",
                f"Type must be one of: {', '.join(TYPE_CHOICES)}.",
                parent=self,
            )
            return
        chronic_flag = 1 if chronic == "Chronic" else 0

        adm = self.adm_var.get().strip()
        notes = self.notes_text.get("1.0", "end").strip()
        followup_date = ai_helpers.suggest_followup_date(adm, disease_canonical)
        try:
            conn = get_conn()
            cur = conn.cursor()

            cur.execute(
                """
                UPDATE patients SET
                name = ?,
                age = ?,
                gender = ?,
                phone = ?,
                disease = ?,
                chronic = ?,
                admission_date = ?,
                notes = ?,
                followup_date = ?
                WHERE id = ?
                """,
                (
                    name,
                    age,
                    gender,
                    phone,
                    disease_canonical,
                    chronic_flag,
                    adm,
                    notes,
                    followup_date,
                    iid,
                ),
            )

            conn.commit()
            self.load_records()
            messagebox.showinfo(
                "Updated", "✅ Patient record updated successfully.", parent=self
            )
        except Exception as e:
            messagebox.showerror("Update failed", str(e), parent=self)
        finally:
            try:
                conn.close()
            except Exception:
                pass

    def delete_record(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Select a record to delete.", parent=self)
            return
        iid = sel[0]
        if not messagebox.askyesno("Confirm", f"Delete patient id {iid}?", parent=self):
            return
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM patients WHERE id=?", (int(iid),))
        conn.commit()
        conn.close()
        self.load_records()
        self.clear_form()
        messagebox.showinfo("Deleted", "🗑️ Patient deleted.", parent=self)

    def on_tree_double(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        iid = sel[0]
        vals = self.tree.item(iid, "values")
        # populate form fields
        self.name_var.set(vals[1])
        self.age_var.set(vals[2])
        self.gender_var.set(vals[3])
        self.phone_var.set(vals[4])
        type_label = vals[6]  # column "Type"
        self.chronic_var.set(type_label)

        disease_val = vals[5] if len(vals) > 5 and vals[5] is not None else ""
        try:
            self.disease_var.set(disease_val)
        except Exception:
            pass
        try:
            if hasattr(self, "disease_entry") and hasattr(self.disease_entry, "var"):
                self.disease_entry.var.set(disease_val)
                if hasattr(self.disease_entry, "_hide_popup"):
                    try:
                        self.disease_entry._hide_popup()
                    except Exception:
                        pass
        except Exception:
            pass

        try:
            if isinstance(vals[6], int):
                self.chronic_var.set("Chronic" if vals[6] == 1 else "Acute")
            else:
                self.chronic_var.set(vals[6])
        except Exception:
            try:
                self.chronic_var.set("")
            except Exception:
                pass

        try:
            self.adm_var.set(vals[7])
        except Exception:
            pass
        # Clear notes box
        self.notes_text.delete("1.0", "end")

        # Get selected row ID
        selected = self.tree.focus()
        vals = self.tree.item(selected, "values")

        # Fetch notes directly from DB (NOT tree column)
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT notes FROM patients WHERE id = ?", (vals[0],))
        row = cur.fetchone()
        conn.close()

        if row and row[0]:
            self.notes_text.insert("1.0", row[0])
        try:
            patient_name = vals[1]
            patient_phone = vals[4]

            conn = get_conn()
            cur = conn.cursor()
            cur.execute(
                """
                        SELECT admission_date, disease, chronic
                        FROM patients
                        WHERE name = ? AND phone = ?
                        ORDER BY admission_date
                        """,
                (patient_name, patient_phone),
            )
            visits = cur.fetchall()
            conn.close()
            if len(visits) > 1:
                history_text = ""
                for i, v in enumerate(visits, 1):
                    visit_type = "Chronic" if v[2] == 1 else "Acute"
                    history_text += (
                        f"Visit {i}\n"
                        f"Date: {v[0]}\n"
                        f"Disease: {v[1]}\n"
                        f"Type: {visit_type}\n\n"
                    )
                    messagebox.showinfo(
                        f"Visit History – {patient_name}",
                        history_text.strip(),
                        parent=self,
                    )
        except Exception:
            pass

    def on_reset(self):
        self.load_records()
        self.clear_form()

    def on_close(self):
        """Attempt clean shutdown; force exit if GUI hangs."""
        if messagebox.askyesno(
            "Confirm Exit", "Do you really want to exit the application?", parent=self
        ):
            try:
                try:
                    self.quit()
                    self.update_idletasks()
                    self.destroy()
                except Exception as e:
                    print("Warning during clean quit/destroy:", e)
                try:
                    sys.exit(0)
                except SystemExit:
                    os._exit(0)
            except Exception as e:
                print("Error during final exit:", e)
                try:
                    os._exit(0)
                except Exception:
                    pass
        else:
            return

    def open_reports(self):
        """
        Try to open external prms_reports.ReportsWindow if available.
        If import fails, open an internal lightweight fallback reports window.
        """
        # Preferred: external module (unchanged behavior)
        try:
            import prms_reports

            try:
                prms_reports.ReportsWindow(self, db_path=DB_FILE)
                return
            except Exception as e:
                messagebox.showwarning(
                    "Reports warning",
                    f"prms_reports imported but failed to open: {e}\nFalling back to built-in reports.",
                    parent=self,
                )
        except Exception:
            pass

        # Fallback: dependency-free reports window using tkinter canvas & labels
        try:
            conn = get_conn()
            cur = conn.cursor()

            # Gender counts
            cur.execute("SELECT gender, COUNT(*) FROM patients GROUP BY gender")
            gender_rows = cur.fetchall()

            # Chronic vs Acute
            cur.execute("SELECT chronic, COUNT(*) FROM patients GROUP BY chronic")
            type_rows = cur.fetchall()

            # Top diseases
            cur.execute(
                "SELECT disease, COUNT(*) as cnt FROM patients GROUP BY disease ORDER BY cnt DESC LIMIT 12"
            )
            disease_rows = cur.fetchall()

            # Monthly counts (YYYY-MM)
            cur.execute(
                "SELECT substr(admission_date,1,7) as ym, COUNT(*) FROM patients WHERE admission_date IS NOT NULL AND admission_date != '' GROUP BY ym ORDER BY ym"
            )
            month_rows = cur.fetchall()

            conn.close()
        except Exception as e:
            messagebox.showerror(
                "Reports error", f"Failed to read DB for reports: {e}", parent=self
            )
            return

        # Create reports window
        win = tk.Toplevel(self)
        win.title("📊 Reports - PRMS (Fallback)")
        win.geometry("1000x700")
        win.transient(self)
        win.grab_set()

        header = ttk.Frame(win, padding=(12, 12))
        header.pack(fill="x")
        ttk.Label(header, text="Reports & Quick Charts", font=self.H1).pack(
            side="left", anchor="w"
        )
        ttk.Button(
            header, text="Refresh", command=lambda: (win.destroy(), self.open_reports())
        ).pack(side="right")

        body = ttk.Frame(win, padding=(12, 12))
        body.pack(fill="both", expand=True)

        # vertical scrollable frame
        canvas_outer = tk.Canvas(body)
        vsb = ttk.Scrollbar(body, orient="vertical", command=canvas_outer.yview)
        canvas_outer.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        canvas_outer.pack(side="left", fill="both", expand=True)

        inner = ttk.Frame(canvas_outer)
        canvas_outer.create_window((0, 0), window=inner, anchor="nw")

        def _on_config(e):
            canvas_outer.configure(scrollregion=canvas_outer.bbox("all"))

        inner.bind("<Configure>", _on_config)

        # helper to draw horizontal bar chart
        def draw_bar_chart(parent, title, items, bar_height=26, max_width=700):
            ttk.Label(parent, text=title, font=self.MED).pack(anchor="w", pady=(6, 2))
            if not items:
                ttk.Label(parent, text="No data", font=self.SM).pack(
                    anchor="w", pady=(2, 6)
                )
                return
            max_v = max(v for _, v in items) or 1
            chart_frame = ttk.Frame(parent)
            chart_frame.pack(fill="x", pady=(4, 8))
            for label, value in items:
                row = ttk.Frame(chart_frame)
                row.pack(fill="x", pady=2)
                ttk.Label(row, text=f"{label}", width=24, anchor="w").pack(side="left")
                c = tk.Canvas(
                    row, height=bar_height, width=max_width, highlightthickness=0
                )
                c.pack(side="left", fill="x", expand=True)
                w = int((value / max_v) * (max_width - 10))
                c.create_rectangle(
                    2, 4, 2 + w, bar_height - 4, fill="#2f7ce0", outline=""
                )
                try:
                    if w > 20:
                        c.create_text(
                            4 + min(w, max(40, w // 2)),
                            bar_height // 2,
                            anchor="w",
                            text=str(value),
                            fill="white",
                        )
                except Exception:
                    pass
                ttk.Label(row, text=str(value), width=6, anchor="e").pack(
                    side="left", padx=(6, 0)
                )

        # Gender distribution
        gender_items = []
        for g, cnt in gender_rows:
            lab = g if g and g.strip() else "Unknown"
            gender_items.append((lab, cnt))
        gender_frame = ttk.Frame(inner, padding=(6, 6), relief="ridge")
        gender_frame.pack(fill="x", pady=(6, 6))
        draw_bar_chart(gender_frame, "Gender distribution", gender_items)

        # Type: Chronic vs Acute
        type_map = {0: "Acute", 1: "Chronic"}
        type_items = []
        for val, cnt in type_rows:
            lab = type_map.get(val, str(val))
            type_items.append((lab, cnt))
        type_frame = ttk.Frame(inner, padding=(6, 6), relief="ridge")
        type_frame.pack(fill="x", pady=(6, 6))
        draw_bar_chart(type_frame, "Type: Chronic vs Acute", type_items)

        # Top diseases
        disease_items = [(d if d else "Unknown", cnt) for d, cnt in disease_rows]
        disease_frame = ttk.Frame(inner, padding=(6, 6), relief="ridge")
        disease_frame.pack(fill="x", pady=(6, 6))
        draw_bar_chart(
            disease_frame, "Top diseases (by count)", disease_items, max_width=800
        )

        # Monthly admissions
        month_items = []
        for ym, cnt in month_rows:
            lab = ym if ym else "Unknown"
            month_items.append((lab, cnt))
        month_frame = ttk.Frame(inner, padding=(6, 6), relief="ridge")
        month_frame.pack(fill="x", pady=(6, 6))
        draw_bar_chart(
            month_frame, "Admissions per month (YYYY-MM)", month_items, max_width=900
        )

        # Quick textual summary
        summary_frame = ttk.Frame(inner, padding=(6, 6), relief="ridge")
        summary_frame.pack(fill="x", pady=(6, 6))
        ttk.Label(summary_frame, text="Quick summary", font=self.MED).pack(
            anchor="w", pady=(4, 4)
        )
        total_rows = sum(cnt for _, cnt in gender_items) if gender_items else 0
        ttk.Label(
            summary_frame, text=f"Total patients: {total_rows}", font=self.SM
        ).pack(anchor="w", pady=(2, 2))

        win.update_idletasks()
        canvas_outer.configure(scrollregion=canvas_outer.bbox("all"))


def login_flow():
    root = tk.Tk()
    root.withdraw()
    if not os.path.exists(CFG_FILE):
        while True:
            p1 = simpledialog.askstring(
                "Set Password",
                "Set admin password (will be saved locally):",
                show="*",
                parent=root,
            )
            if p1 is None:
                messagebox.showinfo(
                    "Cancelled", "No password set. Exiting.", parent=root
                )
                root.destroy()
                raise SystemExit
            p2 = simpledialog.askstring(
                "Confirm Password", "Confirm password:", show="*", parent=root
            )
            if p1 == p2:
                set_password(p1)
                messagebox.showinfo("Saved", "Password saved.", parent=root)
                break
            else:
                messagebox.showwarning(
                    "Mismatch", "Passwords did not match. Try again.", parent=root
                )
    for attempt in range(3):
        pw = simpledialog.askstring(
            "Login", "Enter admin password:", show="*", parent=root
        )
        if pw is None:
            root.destroy()
            raise SystemExit
        if verify_password(pw):
            root.destroy()
            return True
        else:
            messagebox.showerror("Access denied", "Invalid password.", parent=root)
    root.destroy()
    raise SystemExit


if __name__ == "__main__":
    try:
        login_flow()
    except SystemExit:
        print("Exiting: login failed or cancelled.")
        raise SystemExit
    app = PRMSApp()
    app.mainloop()

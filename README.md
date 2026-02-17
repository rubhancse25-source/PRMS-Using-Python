Patient Records Management System (PRMS)


A professional, local-first desktop application designed for healthcare providers to manage patient data, perform clinical trend analysis, and utilize rule-based decision support. This system is engineered for privacy and efficiency, operating entirely offline with no external API dependencies or recurring costs.




Overview:

The Patient Records Management System (PRMS) provides a centralized interface for clinical documentation. It combines a robust SQLite database backend with a modern Python-based graphical user interface (GUI). The system includes built-in logic for risk assessment and automated patient summarization, ensuring that practitioners can quickly identify high-priority cases and historical trends.




Core Functionalities:

1. Clinical Data Management
Patient Records: Comprehensive CRUD (Create, Read, Update, Delete) operations for patient profiles, medical histories, and clinical notes.

Persistent Storage: Utilizes SQLite with Write-Ahead Logging (WAL) mode enabled to ensure high concurrency and prevent database locking during intensive operations.

Optimized Search: Real-time filtering by patient name, diagnosis, or chronic status for rapid information retrieval.

2. Clinical Decision Support (Local AI)
Automated Risk Assessment: Heuristic-based flagging (High, Medium, Low) based on patient age, chronic conditions, and urgent clinical markers.

Intelligent Note Summarization: Algorithmically generates concise clinical summaries from raw practitioner notes using keyword weighting.

Similarity Matching: Identifies historically similar cases within the database to assist in comparative diagnostics based on patient demographics and symptoms.

Condition Classification: Automatically classifies conditions as Acute or Chronic based on diagnostic metadata.

3. Analytics and Reporting
Data Visualization: Integration with Matplotlib and Numpy to generate demographic distributions, disease prevalence charts, and patient volume trends.

Longitudinal Analysis: Detects statistical trends, such as month-over-month increases or decreases in specific diagnoses.

Report Exportation: Ability to export clinical charts and statistical graphs to high-resolution PNG files for administrative reviews or presentations.

4. Security and Privacy
Local-First Architecture: Ensures all patient data remains on-premises, facilitating compliance with data privacy standards.

Secure Authentication: Administrative access is protected by password hashing.

Encrypted Configuration: Application settings and authentication tokens are stored in a secure local JSON configuration.





Technical Specifications:

Programming Language: Python 3.x
GUI Framework: Tkinter (Custom Themed)
Database Engine: SQLite3
Computational Libraries: Matplotlib, Numpy
Security Modules: Hashlib, Secrets




Prerequisites
Ensure Python 3.8 or higher is installed on your system.





System Architecture
prms_main.py: The primary application controller handling the GUI lifecycle, database interactions, and authentication logic.

ai_helpers.py: The logic engine for clinical decision support, risk scoring, and text processing.

prms_reports.py: A specialized module for statistical computation and graphical rendering of clinic data.




Configuration
Upon the initial launch, the system will prompt the administrator to establish a secure password. This password is used to encrypt the local session. The database (prms_patients.db) is initialized automatically in the application directory.

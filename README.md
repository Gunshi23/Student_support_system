# 🎓 CampusCare — AI-Powered University Student Support System (Text + Voice)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40%2B-red.svg)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3%2B-orange.svg)](https://scikit-learn.org/)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)]()

**CampusCare** is a production-grade, full-stack student support chatbot designed for university campuses. It features dual text and voice input/output pipelines, hybrid semantic search over 5,000 real-world student inquiries, automated human escalation detection, an interactive analytics suite, and a modern glassmorphic interface.

---

## ✨ Features

- 💬 **Multi-Turn Conversational Support**:
  - Contextual responses across 10 campus domains (Tuition Fees, Exam Cell, Class Schedules, Admissions, Hostel, IT Support, Placements, Library, Counseling, and Student Grievances).
- 🎙️ **Voice-to-Text & Audio Synthesis**:
  - Native microphone recording with direct WAV audio parsing (no external ffmpeg required).
  - Speech transcription using SpeechRecognition and spoken response generation via gTTS.
- 🛡️ **Automated Human Escalation Engine**:
  - Automatically identifies sensitive inquiries (mental wellbeing, grievances, harassment, low semantic confidence) and immediately flags recommended staff intervention.
- 📊 **Interactive Dataset Analytics**:
  - Full breakdown of `student_support_chatbot_dataset_5000.csv` with intent distributions, escalation rates, and student satisfaction ratings.
  - **Live Semantic Intent Simulator**: Test custom queries against the TF-IDF vector space in real time.
- 🏛️ **Campus Services Directory**:
  - Direct contacts, office hours, and locations for the Examination Cell, Accounts Office, IT Helpdesk, 24/7 Counseling Helpline, and Chief Warden.
- 🎨 **Modern Dark Glassmorphism UI**:
  - Tailored color palette, Inter/Plus Jakarta Sans typography, sleek sidebar quick-launcher, and responsive design.

---

## 📂 Dataset Integration

The system natively loads `student_support_chatbot_dataset_5000.csv` with 5,000 examples containing:
- `session_id`: Unique student session identifier.
- `user_query_type`: Natural language query text.
- `intent`: Primary category (`exams`, `fees`, `hostel`, `admissions`, `schedule`, `library`, `grievance`).
- `confidence_score`: Historical confidence metrics.
- `escalated`: Ground-truth escalation flag (0 or 1).
- `user_rating`: Historical student satisfaction rating (1 to 5).

The app fits an n-gram `TfidfVectorizer` with cosine similarity matching to locate the most relevant student inquiry patterns and determine safe responses and escalation triggers.

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10 or higher
- Git

### 2. Installation
Clone the repository and install dependencies:
```bash
git clone https://github.com/Gunshi23/Student_support_system.git
cd Student_support_system
pip install -r requirements.txt
```

### 3. Launch the Application
```bash
streamlit run app.py
```
The application will open automatically in your browser at `http://localhost:8501`.

### 4. Optional: Enable Gemini Neural Engine
To enable dynamic generative responses via Google Gemini alongside verified FAQs:
```powershell
$env:GEMINI_API_KEY="YOUR_API_KEY"
streamlit run app.py
```
*(Alternatively, you can paste your API key directly into the sidebar field inside the running app).*

---

## 🔒 Privacy & Safety
CampusCare strictly operates in-memory for session privacy and never stores passwords, OTPs, or student credentials. Sensitive grievances and safety concerns are directed to official university authorities and 24/7 helplines.

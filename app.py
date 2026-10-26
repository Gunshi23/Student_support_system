import os
import re
import io
import time
import pandas as pd
import streamlit as st

APP_TITLE = "CampusCare | Student Support AI"
GEMINI_MODEL = "gemini-2.5-flash"

# Page configuration
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End Styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg-primary: #070913;
    --bg-secondary: #0e1326;
    --card-bg: rgba(17, 24, 48, 0.7);
    --border-glow: rgba(99, 102, 241, 0.22);
    --accent-indigo: #6366f1;
    --accent-purple: #a855f7;
    --accent-cyan: #06b6d4;
    --accent-emerald: #10b981;
    --accent-amber: #f59e0b;
    --text-primary: #f8fafc;
    --text-secondary: #cbd5e1;
    --text-muted: #8292ab;
}

html, body, [class*="css"], .stApp {
    font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
    background-color: var(--bg-primary) !important;
    background-image: 
        radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.12) 0px, transparent 50%),
        radial-gradient(at 100% 0%, rgba(168, 85, 247, 0.12) 0px, transparent 50%),
        radial-gradient(at 50% 100%, rgba(6, 182, 212, 0.08) 0px, transparent 50%) !important;
    color: var(--text-primary) !important;
}

/* Custom Scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0b0f1d; }
::-webkit-scrollbar-thumb { background: #3730a3; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #4f46e5; }

/* Sidebar Enhancements */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #090d1c 0%, #0c1124 100%) !important;
    border-right: 1px solid var(--border-glow) !important;
    padding-top: 1rem;
}

section[data-testid="stSidebar"] hr {
    border-color: rgba(99, 102, 241, 0.18) !important;
    margin: 1.2rem 0 !important;
}

/* Brand header */
.brand-box {
    padding: 1.2rem 0.8rem 1rem;
    text-align: center;
    background: linear-gradient(145deg, rgba(30, 41, 79, 0.5), rgba(15, 23, 42, 0.8));
    border-radius: 16px;
    border: 1px solid rgba(99, 102, 241, 0.25);
    margin-bottom: 1.2rem;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
}

.brand-icon {
    font-size: 2.2rem;
    display: inline-block;
    filter: drop-shadow(0 0 12px rgba(99, 102, 241, 0.6));
}

.brand-title {
    font-size: 1.35rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, #a5b4fc 0%, #c084fc 50%, #67e8f9 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0.4rem 0 0.1rem;
}

.brand-subtitle {
    font-size: 0.78rem;
    color: var(--text-muted);
    font-weight: 500;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(16, 185, 129, 0.12);
    border: 1px solid rgba(16, 185, 129, 0.3);
    color: #34d399;
    padding: 3px 10px;
    border-radius: 9999px;
    font-size: 0.73rem;
    font-weight: 600;
    margin-top: 0.6rem;
}

.status-dot {
    width: 6px;
    height: 6px;
    background-color: #34d399;
    border-radius: 50%;
    box-shadow: 0 0 8px #34d399;
    animation: pulse-dot 2s infinite ease-in-out;
}

@keyframes pulse-dot {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.4; transform: scale(0.85); }
}

/* Hero Section */
.hero-container {
    background: linear-gradient(135deg, rgba(30, 27, 75, 0.7) 0%, rgba(15, 23, 42, 0.85) 50%, rgba(19, 36, 68, 0.65) 100%);
    border: 1px solid rgba(99, 102, 241, 0.3);
    border-radius: 20px;
    padding: 1.8rem 2.2rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 12px 36px rgba(0, 0, 0, 0.4);
    position: relative;
    overflow: hidden;
}

.hero-container::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -20%;
    width: 140%;
    height: 100%;
    background: radial-gradient(circle, rgba(99, 102, 241, 0.15) 0%, transparent 70%);
    pointer-events: none;
}

.hero-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(99, 102, 241, 0.2);
    border: 1px solid rgba(129, 140, 248, 0.4);
    color: #c7d2fe;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 4px 12px;
    border-radius: 9999px;
    margin-bottom: 0.8rem;
}

.hero-title {
    font-size: 2.1rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    color: #ffffff;
    margin: 0;
    line-height: 1.2;
}

.hero-title span {
    background: linear-gradient(135deg, #818cf8 0%, #c084fc 60%, #38bdf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-desc {
    color: #cbd5e1;
    font-size: 0.95rem;
    margin-top: 0.6rem;
    max-width: 780px;
    line-height: 1.55;
}

/* Feature Cards */
.feat-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-bottom: 1.6rem;
}

.feat-card {
    background: rgba(18, 25, 48, 0.6);
    border: 1px solid rgba(99, 102, 241, 0.18);
    border-radius: 14px;
    padding: 1.1rem 1.3rem;
    backdrop-filter: blur(10px);
    transition: all 0.2s ease;
}

.feat-card:hover {
    border-color: rgba(129, 140, 248, 0.4);
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
}

.feat-card-title {
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: 700;
    font-size: 0.95rem;
    color: #e2e8f0;
    margin-bottom: 0.3rem;
}

.feat-card-desc {
    font-size: 0.82rem;
    color: var(--text-muted);
    line-height: 1.45;
    margin: 0;
}

/* Chat bubble enhancements */
.chat-msg-card {
    background: rgba(15, 23, 42, 0.7);
    border: 1px solid rgba(99, 102, 241, 0.18);
    border-radius: 16px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1rem;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
}

.badge-row {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 8px;
    margin-top: 0.8rem;
    padding-top: 0.8rem;
    border-top: 1px solid rgba(99, 102, 241, 0.12);
}

.meta-pill {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 3px 10px;
    border-radius: 8px;
    font-size: 0.75rem;
    font-weight: 600;
}

.pill-topic {
    background: rgba(99, 102, 241, 0.15);
    border: 1px solid rgba(99, 102, 241, 0.35);
    color: #a5b4fc;
}

.pill-conf {
    background: rgba(6, 182, 212, 0.15);
    border: 1px solid rgba(6, 182, 212, 0.35);
    color: #67e8f9;
    font-family: 'JetBrains Mono', monospace;
}

.pill-ok {
    background: rgba(16, 185, 129, 0.15);
    border: 1px solid rgba(16, 185, 129, 0.35);
    color: #34d399;
}

.pill-esc {
    background: rgba(245, 158, 11, 0.18);
    border: 1px solid rgba(245, 158, 11, 0.45);
    color: #fbbf24;
    animation: glow-esc 2s infinite ease-in-out;
}

@keyframes glow-esc {
    0%, 100% { box-shadow: 0 0 0 rgba(245, 158, 11, 0); }
    50% { box-shadow: 0 0 10px rgba(245, 158, 11, 0.35); }
}

.escalation-notice {
    margin-top: 0.8rem;
    background: linear-gradient(135deg, rgba(120, 53, 15, 0.25) 0%, rgba(69, 26, 3, 0.35) 100%);
    border: 1px solid rgba(245, 158, 11, 0.4);
    border-radius: 10px;
    padding: 0.8rem 1rem;
    font-size: 0.84rem;
    color: #fef3c7;
    line-height: 1.5;
}

/* Metrics Cards */
.stat-card {
    background: linear-gradient(145deg, rgba(20, 27, 54, 0.7), rgba(12, 17, 34, 0.9));
    border: 1px solid rgba(99, 102, 241, 0.22);
    border-radius: 14px;
    padding: 1.2rem;
    text-align: center;
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.25);
}

.stat-value {
    font-size: 2rem;
    font-weight: 800;
    font-family: 'JetBrains Mono', monospace;
    background: linear-gradient(135deg, #a5b4fc, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.stat-label {
    font-size: 0.8rem;
    color: var(--text-muted);
    font-weight: 600;
    margin-top: 0.2rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* Header styling */
header[data-testid="stHeader"] {
    background: rgba(7, 9, 19, 0.8) !important;
    backdrop-filter: blur(12px) !important;
}

/* Sidebar button overrides */
section[data-testid="stSidebar"] .stButton > button {
    background: rgba(22, 30, 60, 0.65) !important;
    color: #e0e7ff !important;
    border: 1px solid rgba(99, 102, 241, 0.28) !important;
    border-radius: 10px !important;
    text-align: left !important;
    font-weight: 500 !important;
    font-size: 0.84rem !important;
    padding: 0.55rem 0.85rem !important;
    width: 100% !important;
}

section[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(99, 102, 241, 0.25) !important;
    border-color: #818cf8 !important;
    color: #ffffff !important;
    box-shadow: 0 4px 14px rgba(99, 102, 241, 0.3) !important;
    transform: translateX(2px) !important;
}

/* Chat Message Card Styling */
[data-testid="stChatMessage"] {
    background: rgba(16, 22, 44, 0.8) !important;
    border: 1px solid rgba(99, 102, 241, 0.25) !important;
    border-radius: 16px !important;
    padding: 1.2rem 1.4rem !important;
    margin-bottom: 0.9rem !important;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25) !important;
}

[data-testid="stChatMessage"] * {
    color: #f8fafc !important;
}

[data-testid="stChatMessage"] p, 
[data-testid="stChatMessage"] li {
    color: #e2e8f0 !important;
    font-size: 0.95rem !important;
    line-height: 1.65 !important;
}

[data-testid="stChatMessage"] strong {
    color: #ffffff !important;
    font-weight: 700 !important;
}

[data-testid="stChatMessage"] code {
    background: rgba(99, 102, 241, 0.25) !important;
    color: #c7d2fe !important;
    border: 1px solid rgba(99, 102, 241, 0.4) !important;
    padding: 2px 6px !important;
    border-radius: 5px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.86rem !important;
}

/* Chat Input Styling */
[data-testid="stChatInput"] {
    background: rgba(15, 23, 42, 0.85) !important;
    border: 1px solid rgba(99, 102, 241, 0.4) !important;
    border-radius: 14px !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3) !important;
}

[data-testid="stChatInput"] textarea {
    color: #ffffff !important;
    font-size: 0.95rem !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #94a3b8 !important;
}

/* Button overrides */
.stButton > button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    transition: all 0.2s ease !important;
    border: 1px solid rgba(99, 102, 241, 0.3) !important;
}

.stButton > button:hover {
    border-color: rgba(129, 140, 248, 0.7) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 14px rgba(99, 102, 241, 0.25) !important;
}

/* Tabs styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: rgba(14, 20, 40, 0.75);
    padding: 6px;
    border-radius: 12px;
    border: 1px solid rgba(99, 102, 241, 0.22);
}

.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    color: #94a3b8 !important;
    font-weight: 600 !important;
    padding: 8px 20px !important;
    transition: all 0.2s ease;
}

.stTabs [aria-selected="true"] {
    background-color: rgba(99, 102, 241, 0.3) !important;
    color: #ffffff !important;
    border-bottom: 2px solid #818cf8 !important;
}
</style>
""", unsafe_allow_html=True)

# Comprehensive Verified Campus Knowledge Base
FAQS = [
    (
        "fees",
        ["fee", "fees", "tuition", "payment", "scholarship", "refund", "receipt", "challan", "dues", "installment"],
        "💰 **Fee & Financial Support Services**:\n\n"
        "• **Online Payment**: Visit your official student portal under `Accounts & Fees` → `Make Payment` to pay via NetBanking, UPI, or Debit/Credit card.\n"
        "• **Fee Receipts**: Download digitally verified fee receipts instantly from the receipts tab after successful transaction confirmation.\n"
        "• **Scholarships & Financial Aid**: Merit and need-based scholarship applications open every semester. Submit your academic transcripts and income certificate to the Accounts Office.\n"
        "• **Refunds & Installments**: For fee refund requests or special installment permissions, submit form `FIN-04` directly to the Accounts/Finance Office before the semester deadline."
    ),
    (
        "exams",
        ["exam", "examination", "result", "marks", "grade", "revaluation", "back paper", "admit card", "hall ticket", "date sheet"],
        "📝 **Examination Cell & Results**:\n\n"
        "• **Date Sheets & Timetable**: Published on the Examination Portal 2 weeks prior to mid-term and end-term examinations.\n"
        "• **Admit Card / Hall Ticket**: Mandatory for examination entry. Generated 5 days prior to exams on the portal. Clear all library & fee dues if download is locked.\n"
        "• **Semester Results & Transcripts**: Declared within 30-45 days following exams. Official digital transcripts can be requested via the Registrar's counter.\n"
        "• **Revaluation & Back Papers**: Revaluation forms and back paper registrations open for 14 days following result declaration via the exam cell window."
    ),
    (
        "schedule",
        ["timetable", "schedule", "class", "lecture", "attendance", "room", "holiday", "calendar", "timing", "session"],
        "📅 **Academic Timetable & Attendance Policy**:\n\n"
        "• **Class Timetables**: Check your departmental notice board or LMS dashboard for section-wise lecture and lab schedules.\n"
        "• **Attendance Requirement**: A minimum of **75% attendance** is mandatory to be eligible for end-term examinations across all registered courses.\n"
        "• **Discrepancy Resolution**: In case of medical leave or attendance mismatches, submit documented medical certificates to your Faculty Mentor or Class Coordinator within 7 days.\n"
        "• **Academic Calendar**: Access the official semester calendar showing mid-breaks, national holidays, and sports/cultural events via the student portal."
    ),
    (
        "admissions",
        ["admission", "enrol", "enroll", "registration", "eligibility", "documents", "application", "seat", "branch", "cutoff"],
        "🏛️ **Admissions & Enrollment Office**:\n\n"
        "• **Eligibility & Criteria**: Verified based on qualifying examination scores, national/state entrance percentiles, and university reservation norms.\n"
        "• **Document Verification**: Original Class 10/12 marks cards, transfer certificate (TC), migration certificate, and ID proof must be physically verified at the Admissions Desk.\n"
        "• **Application Deadlines**: Check the active round cutoff list on the official university portal.\n"
        "• **Branch Upgradation**: Merit-based internal sliding/upgradation opens after the completion of first-year registrations subject to seat vacancy."
    ),
    (
        "hostel",
        ["hostel", "dorm", "allotment", "accommodation", "room", "mess", "warden", "curfew", "laundry"],
        "🛏️ **Hostel Accommodation & Student Housing**:\n\n"
        "• **Room Allotment**: Allotment is conducted per semester based on distance and academic standing. Check your assigned block and room number on the Hostel Portal.\n"
        "• **Mess & Dining**: Multi-cuisine meal plans (breakfast, lunch, evening snacks, dinner) operate in all residential blocks. Feedback can be given to the Mess Committee.\n"
        "• **Curfew & Security**: Campus hostel gates close at **9:30 PM** on weekdays and **10:00 PM** on weekends for student safety. Night passes require prior warden approval.\n"
        "• **Maintenance & Warden Desk**: For electrical, plumbing, or room repair requests, log a ticket via the campus warden helpline or hostel desk."
    ),
    (
        "technical_support",
        ["login", "password", "portal", "website", "error", "technical", "wifi", "upload", "lms", "moodle", "reset"],
        "🧑‍💻 **IT Services & Campus Helpdesk**:\n\n"
        "• **Password Reset**: Click 'Forgot Password' on the student portal login page. A verification link will be sent to your registered college email.\n"
        "• **Campus Wi-Fi Access**: Register your device MAC address with the IT center to obtain individual high-speed Wi-Fi authentication credentials.\n"
        "• **LMS & Moodle Issues**: If course content is inaccessible or assignment submissions error out, clear browser cache and contact `it-support@campus.edu`.\n"
        "• **Security Reminder**: The university IT cell will **NEVER** ask for your password, OTP, or payment card details. Keep credentials strictly confidential."
    ),
    (
        "wellbeing",
        ["stress", "anxious", "anxiety", "overwhelmed", "sad", "lonely", "mental health", "not fine", "not okay", "depressed", "counselor", "panic"],
        "💙 **Student Counseling & Mental Wellbeing Support**:\n\n"
        "You are not alone, and help is always available. University life can feel overwhelming, but dedicated support is here for you:\n\n"
        "• **Campus Counseling Center**: Free, strictly confidential, one-on-one sessions with professional licensed psychologists (Health & Wellness Block, Room 104).\n"
        "• **Student Peer Mentors**: Reach out to trained senior peer volunteers who understand academic pressures.\n"
        "• **24/7 Student Crisis Helpline**: Call `1800-CAMPUS-CARE` (Toll-Free) anytime day or night.\n"
        "• *Note*: I am an AI assistant, not a clinical counselor. If you are experiencing distress, connecting with a caring human professional is strongly recommended."
    ),
    (
        "grievance",
        ["complaint", "grievance", "harassment", "discrimination", "bully", "unsafe", "report", "ragging", "threat", "disciplinary"],
        "🛡️ **Grievance Redressal & Student Safety**:\n\n"
        "Our institution has a zero-tolerance policy towards harassment, discrimination, bullying, and ragging:\n\n"
        "• **Anti-Ragging Helpline**: 24/7 dedicated line `1800-180-5522` or email `antiragging@campus.edu`.\n"
        "• **Internal Complaints Committee (ICC)**: For complaints regarding gender harassment or discrimination, submit a confidential report to the Presiding Officer.\n"
        "• **Dean of Student Welfare**: Direct contact window available on weekdays 2:00 PM – 4:00 PM in the Administrative Block.\n"
        "• *Action*: This query has been flagged for prioritized escalation. Please reach out immediately to campus security or a trusted authority if you feel unsafe."
    ),
    (
        "library",
        ["library", "book", "borrow", "renew", "journal", "research paper", "fine", "catalogue", "opac", "e-resources"],
        "📚 **Central Library & Digital Resources**:\n\n"
        "• **Borrowing Privileges**: Undergraduates may borrow up to 4 books for 14 days; postgraduates and researchers up to 6 books for 30 days.\n"
        "• **Online Renewals**: Books can be renewed up to 2 consecutive times through the OPAC Web Portal unless placed on hold by another borrower.\n"
        "• **E-Resources & Research**: Access IEEE Xplore, ScienceDirect, Springer, and JSTOR remotely using your institutional library login.\n"
        "• **Operating Hours**: Monday to Saturday: 8:00 AM – 10:00 PM. Extended 24/7 reading hall during end-term examinations."
    ),
    (
        "placement",
        ["placement", "internship", "career", "resume", "cv", "interview", "job", "company", "package", "recruitment"],
        "💼 **Career Development & Placement Cell (CDC)**:\n\n"
        "• **Registration**: Final year and pre-final year students must register on the CDC Placement Portal with verified grade sheets.\n"
        "• **Internships**: Summer and industrial internship drives commence from the 5th semester onwards with stipend guidelines.\n"
        "• **Resume Review & Mock Interviews**: Attend weekly soft-skill bootcamps and resume clinics organized in the Seminar Hall.\n"
        "• **Placement Drives**: Check active drive notifications, eligibility criteria (minimum CGPA), and test schedules on the CDC notice board."
    )
]

# Load and prepare the 5,000-row dataset
DATASET_PATH = os.path.join(os.path.dirname(__file__), "student_support_chatbot_dataset_5000.csv")

@st.cache_resource
def load_dataset_model():
    if not os.path.exists(DATASET_PATH):
        raise FileNotFoundError(f"Dataset not found at {DATASET_PATH}")
    
    data = pd.read_csv(DATASET_PATH)
    required = {"session_id", "user_query_type", "intent", "confidence_score", "escalated", "user_rating"}
    missing = required - set(data.columns)
    if missing:
        raise ValueError(f"Dataset missing required columns: {sorted(missing)}")
    
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
        vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english", max_features=12000)
        query_matrix = vectorizer.fit_transform(data["user_query_type"].fillna("").astype(str))
        return data, vectorizer, query_matrix, cosine_similarity
    except ImportError:
        return data, None, None, None

DATA, VECTORIZER, QUERY_MATRIX, COSINE_SIMILARITY = load_dataset_model()

# Classification Engine
def classify(text):
    cleaned = re.sub(r"[^a-zA-Z0-9\s]", " ", text.lower()).strip()
    greetings = {"hi", "hello", "hey", "good morning", "good afternoon", "good evening", "namaste", "hii", "heya", "howdy", "sup"}
    if cleaned in greetings:
        return "greeting", 0.99, False, "Direct greeting match"

    # Scikit-learn TF-IDF Cosine Similarity Search
    if VECTORIZER is not None and QUERY_MATRIX is not None:
        vector = VECTORIZER.transform([text])
        similarities = COSINE_SIMILARITY(vector, QUERY_MATRIX).ravel()
        best_idx = int(similarities.argmax())
        similarity = float(similarities[best_idx])
        row = DATA.iloc[best_idx]
        
        if similarity >= 0.10:
            # Combined confidence: semantic cosine match + dataset training confidence
            confidence = min(0.99, max(0.15, 0.60 * similarity + 0.40 * float(row["confidence_score"])))
            return str(row["intent"]), confidence, bool(int(row["escalated"])), str(row["user_query_type"])

    # Fallback keyword match
    scored = []
    for _, row in DATA.iterrows():
        query = str(row["user_query_type"]).lower()
        overlap = len(set(cleaned.split()) & set(re.sub(r"[^a-z0-9\s]", " ", query).split()))
        if overlap:
            scored.append((overlap, row))
    if scored:
        _, row = max(scored, key=lambda item: item[0])
        return str(row["intent"]), float(row["confidence_score"]), bool(int(row["escalated"])), str(row["user_query_type"])

    return "unknown", 0.30, False, "No direct match"

def faq_answer(text, intent=None):
    if intent is None:
        intent, _conf, _esc, _ = classify(text)
        
    if intent == "greeting":
        return "👋 **Hello and welcome to CampusCare!**\n\nI am your 24/7 AI-powered Student Support Companion, trained on over 5,000 university queries. You can ask me about **tuition fees, examination schedules, timetables, hostel allotment, admissions, library books, campus IT, placements, or wellbeing**.\n\nHow can I support you today?"
        
    for faq_intent, _, answer in FAQS:
        if faq_intent == intent:
            return answer
            
    return (
        "🤔 **I couldn't pinpoint the exact campus service for your inquiry.**\n\n"
        "Here are common areas I can help with:\n"
        "• **Fees & Scholarships**: Payment links, challans, refund policies\n"
        "• **Exams & Results**: Hall tickets, revaluation, grade sheets\n"
        "• **Schedule & Attendance**: Timetables, 75% attendance rule, leave applications\n"
        "• **Hostel & Housing**: Room allotments, mess facility, warden contact\n"
        "• **Admissions & Documents**: Eligibility, document verification, transfer certificate\n"
        "• **IT & Portal**: Password reset, campus Wi-Fi, LMS assistance\n"
        "• **Wellbeing & Grievances**: Counseling support and confidential reporting\n\n"
        "Please rephrase your question or select one of the quick options from the sidebar."
    )

def ai_answer(text, api_key):
    if not api_key:
        return None
    try:
        import requests
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"
        system_instruction = (
            "You are CampusCare, a warm, professional university student-support assistant. "
            "Help students with admissions, fees, exams, timetable, IT, placements, library, and student life. "
            "Never invent university-specific deadlines or official numbers; advise verifying on the official portal. "
            "Never request passwords, OTPs, or sensitive credentials. "
            "If a student mentions feeling unsafe, harassed, or severely depressed, express empathy and advise contacting campus counseling or emergency authorities immediately."
        )
        payload = {
            "systemInstruction": {"parts": [{"text": system_instruction}]},
            "contents": [{"role": "user", "parts": [{"text": text}]}],
            "generationConfig": {"temperature": 0.3, "maxOutputTokens": 450}
        }
        res = requests.post(url, params={"key": api_key}, json=payload, timeout=15)
        if res.status_code == 200:
            return res.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception:
        pass
    return None

def get_answer(text, api_key=""):
    intent, confidence, dataset_escalated, matched_query = classify(text)
    
    # Sensitive or greeting intents always use safe curated answers
    if intent in {"greeting", "unknown", "wellbeing", "grievance"}:
        answer = faq_answer(text, intent=intent)
    else:
        answer = ai_answer(text, api_key) or faq_answer(text, intent=intent)
        
    escalate = dataset_escalated or intent in {"wellbeing", "grievance"} or confidence < 0.40
    
    meta_info = {
        "intent": intent,
        "confidence": confidence,
        "escalate": escalate,
        "matched_query": matched_query
    }
    return answer, meta_info

# Audio Functions with robust error handling
def speak(text):
    """Generate speech audio using gTTS."""
    try:
        from gTTS import gTTS
        # Clean markdown formatting for smoother speech output
        clean_text = re.sub(r'[*_#`•\-\[\]\(\)]', ' ', text)
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
        # Limit speech sample to first 280 characters to keep audio responsive
        if len(clean_text) > 280:
            clean_text = clean_text[:280] + "... Please refer to the text for complete details."
            
        audio_io = io.BytesIO()
        tts = gTTS(text=clean_text, lang="en", tld="com", slow=False)
        tts.write_to_fp(audio_io)
        audio_io.seek(0)
        return audio_io.getvalue()
    except Exception:
        return None

def transcribe(audio_upload):
    """Robust speech recognition that works without external ffmpeg for standard WAV recordings."""
    try:
        import speech_recognition as sr
        raw_bytes = audio_upload.getvalue()
        recognizer = sr.Recognizer()
        
        # Check if file has a valid WAV/RIFF header (standard from browser st.audio_input)
        if raw_bytes.startswith(b'RIFF'):
            wav_io = io.BytesIO(raw_bytes)
            with sr.AudioFile(wav_io) as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.3)
                audio_data = recognizer.record(source)
            return recognizer.recognize_google(audio_data)
            
        # Fallback to pydub if non-WAV container
        try:
            from pydub import AudioSegment
            converted = AudioSegment.from_file(io.BytesIO(raw_bytes))
            wav_io = io.BytesIO()
            converted.export(wav_io, format="wav")
            wav_io.seek(0)
            with sr.AudioFile(wav_io) as source:
                audio_data = recognizer.record(source)
            return recognizer.recognize_google(audio_data)
        except Exception:
            pass
            
    except Exception as e:
        return None
    return None

# Session State Initialization
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "👋 **Hi! I'm CampusCare**, your dedicated university student support assistant.\n\nWhether you need help with tuition fees, exam timetables, hostel rooms, library access, or campus counseling, feel free to **type your question** or **ask using your voice** below!",
        "meta": {"intent": "greeting", "confidence": 1.0, "escalate": False, "matched_query": "Welcome greeting"}
    }]

if "api_key" not in st.session_state:
    st.session_state.api_key = os.getenv("GEMINI_API_KEY", "").strip()

if "auto_speech" not in st.session_state:
    st.session_state.auto_speech = False

# Sidebar Interface
with st.sidebar:
    st.markdown("""
    <div class="brand-box">
        <span class="brand-icon">🎓</span>
        <div class="brand-title">CampusCare AI</div>
        <div class="brand-subtitle">Student Support System</div>
        <div class="status-badge"><span class="status-dot"></span> 5,000 Dataset Records Active</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### ⚡ Quick Help Topics")
    topics = {
        "💳 Fees & Scholarships": "How can I get information about fees and scholarships?",
        "📝 Exams & Admit Cards": "Where can I check exam dates, admit cards and results?",
        "📅 Timetable & Attendance": "What is the attendance policy and where is my class timetable?",
        "🛏️ Hostel & Mess": "How do I apply for hostel allotment and check mess timings?",
        "🧑‍💻 Portal & Wi-Fi Login": "I am having trouble logging into the student portal and Wi-Fi.",
        "💼 Placements & CV": "How do I register with the placement cell for internships and jobs?",
        "📚 Library & E-Resources": "How do I renew a library book and access online research journals?",
        "💙 Counseling & Wellbeing": "I am feeling stressed and overwhelmed with my studies.",
        "🛡️ Student Grievance": "I want to file a complaint regarding safety or unfair treatment."
    }
    
    for label, query_text in topics.items():
        if st.button(label, use_container_width=True):
            st.session_state.pending = query_text
            
    st.markdown("---")
    
    # Audio & Engine Settings
    st.markdown("### ⚙️ Preferences & Engine")
    auto_tts = st.checkbox("🔊 Auto-generate voice replies", value=st.session_state.auto_speech)
    st.session_state.auto_speech = auto_tts
    
    user_api_key = st.text_input(
        "Gemini API Key (Optional)",
        value=st.session_state.api_key,
        type="password",
        placeholder="Enter key for live neural answers",
        help="Optional: Enables Gemini-powered generative explanations in addition to verified FAQs."
    )
    if user_api_key != st.session_state.api_key:
        st.session_state.api_key = user_api_key
        st.rerun()
        
    if st.session_state.api_key:
        st.caption("✨ **Gemini Neural Engine Connected**")
    else:
        st.caption("⚡ **Fast Local TF-IDF Matcher Active** (Zero API key required)")

    if st.button("🧹 Clear Chat History", use_container_width=True):
        st.session_state.messages = [{
            "role": "assistant",
            "content": "👋 Chat cleared. How can I assist you with your campus queries today?",
            "meta": {"intent": "greeting", "confidence": 1.0, "escalate": False, "matched_query": "Fresh session"}
        }]
        st.rerun()
        
    st.markdown("---")
    st.caption("🔒 **Student Privacy Notice**: CampusCare never requests or stores passwords, OTPs, or student credentials. All session data is kept in memory.")

# Top Hero Banner
st.markdown("""
<div class="hero-container">
    <div class="hero-pill">University Student Care Portal · 24/7 Support</div>
    <h1 class="hero-title">How can we <span>support you</span> today?</h1>
    <p class="hero-desc">
        Instant, verified guidance for academics, fees, examinations, campus facilities, and wellbeing. 
        Powered by semantic TF-IDF pattern matching on 5,000 student queries with smart escalation to human services.
    </p>
</div>
""", unsafe_allow_html=True)

# Feature Highlights
st.markdown("""
<div class="feat-grid">
    <div class="feat-card">
        <div class="feat-card-title"><span>💬</span> Multi-turn Text Chat</div>
        <p class="feat-card-desc">Ask queries in natural language with intelligent intent classification.</p>
    </div>
    <div class="feat-card">
        <div class="feat-card-title"><span>🎙️</span> Voice-to-Text Input</div>
        <p class="feat-card-desc">Speak directly using your microphone with robust audio transcription.</p>
    </div>
    <div class="feat-card">
        <div class="feat-card-title"><span>🛡️</span> Smart Human Escalation</div>
        <p class="feat-card-desc">Automatically identifies sensitive grievances and flags human counseling.</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Tabs Navigation
tab_chat, tab_analytics, tab_directory = st.tabs([
    "💬 Support Assistant (Text + Voice)",
    "📊 Dataset & Support Analytics",
    "🏛️ Campus Directory & Escalations"
])

def process_question(q):
    q = q.strip()
    if not q:
        return
    st.session_state.messages.append({"role": "user", "content": q})
    
    with st.spinner("Analyzing your query..."):
        answer, meta = get_answer(q, api_key=st.session_state.api_key)
        
        audio_data = None
        if st.session_state.auto_speech:
            audio_data = speak(answer)
            
        msg = {
            "role": "assistant",
            "content": answer,
            "meta": meta
        }
        if audio_data:
            msg["audio"] = audio_data
            
        st.session_state.messages.append(msg)

# TAB 1: Chat and Voice Assistant
with tab_chat:
    # Pending trigger from sidebar buttons
    pending = st.session_state.pop("pending", None)
    if pending:
        process_question(pending)
        st.rerun()

    # Render Conversation Thread
    chat_container = st.container()
    with chat_container:
        for idx, m in enumerate(st.session_state.messages):
            if m["role"] == "user":
                with st.chat_message("user", avatar="👤"):
                    st.markdown(f"**{m['content']}**")
            else:
                with st.chat_message("assistant", avatar="🎓"):
                    st.markdown(m["content"])
                    
                    # Metadata Badges
                    meta = m.get("meta")
                    if meta:
                        intent_name = meta.get("intent", "general").replace("_", " ").title()
                        confidence = meta.get("confidence", 0.0)
                        escalated = meta.get("escalate", False)
                        
                        pill_class = "pill-esc" if escalated else "pill-ok"
                        status_text = "⚠️ Human Escalation Recommended" if escalated else "✓ Automated Resolution"
                        
                        badges_html = f"""
                        <div class="badge-row">
                            <span class="meta-pill pill-topic">🏷️ {intent_name}</span>
                            <span class="meta-pill pill-conf">🎯 {confidence:.0%} Match</span>
                            <span class="meta-pill {pill_class}">{status_text}</span>
                        </div>
                        """
                        st.markdown(badges_html, unsafe_allow_html=True)
                        
                        if escalated:
                            st.markdown("""
                            <div class="escalation-notice">
                                <strong>⚠️ Staff Escalation Alert</strong>: 
                                This matter has been flagged for human intervention. Please contact your Department Head, 
                                Dean of Student Welfare, or visit the Grievance & Counseling Cell for personalized assistance.
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # Spoken Audio
                    if m.get("audio"):
                        st.audio(m["audio"], format="audio/mp3")
                    else:
                        # Allow on-demand voice generation
                        col_listen, _ = st.columns([1, 4])
                        with col_listen:
                            if st.button("🔊 Listen to response", key=f"tts_{idx}"):
                                with st.spinner("Generating voice..."):
                                    audio_bytes = speak(m["content"])
                                    if audio_bytes:
                                        m["audio"] = audio_bytes
                                        st.rerun()

    # Text Chat Input
    user_input = st.chat_input("Type your student support question here...")
    if user_input:
        process_question(user_input)
        st.rerun()

    # Voice Input Panel
    st.markdown("---")
    st.markdown("### 🎙️ Voice Assistant Input")
    st.caption("Record your question with your microphone. Our audio pipeline converts speech into text and routes it to the matching campus service.")

    v_col1, v_col2 = st.columns([3, 1])
    with v_col1:
        audio_record = st.audio_input("Record your question", key="audio_recorder")
    with v_col2:
        st.write("")
        st.write("")
        transcribe_button = st.button("🚀 Transcribe & Ask", type="primary", use_container_width=True)
        
    if transcribe_button:
        if audio_record is None:
            st.warning("⚠️ Please record audio before clicking Transcribe.")
        else:
            with st.spinner("Processing speech and recognizing audio..."):
                transcript_text = transcribe(audio_record)
            if transcript_text:
                st.success(f"🗣️ **Heard**: *\"{transcript_text}\"*")
                process_question(transcript_text)
                st.rerun()
            else:
                st.error("⚠️ Could not transcribe audio. Please ensure microphone permissions are granted, or type your query in the chat input above.")

# TAB 2: Dataset Analytics & Simulator
with tab_analytics:
    st.markdown("### 📊 Dataset Overview & Intent Modeling")
    st.markdown("Insights derived from `student_support_chatbot_dataset_5000.csv` containing 5,000 actual student inquiries.")
    
    # KPI Row
    total_samples = len(DATA)
    total_intents = DATA["intent"].nunique()
    escalated_count = DATA["escalated"].sum()
    escalated_pct = (escalated_count / total_samples) * 100
    avg_rating = DATA["user_rating"].mean()
    
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{total_samples:,}</div>
            <div class="stat-label">Training Queries</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{total_intents}</div>
            <div class="stat-label">Distinct Intent Classes</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{escalated_pct:.1f}%</div>
            <div class="stat-label">Dataset Escalation Rate</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{avg_rating:.2f} ⭐</div>
            <div class="stat-label">Average Student Rating</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.write("")
    
    # Intent breakdown
    col_chart1, col_chart2 = st.columns([3, 2])
    with col_chart1:
        st.markdown("#### 📈 Query Distribution by Intent")
        intent_counts = DATA["intent"].value_counts().reset_index()
        intent_counts.columns = ["Intent Category", "Total Inquiries"]
        st.bar_chart(intent_counts.set_index("Intent Category"), color="#6366f1")
        
    with col_chart2:
        st.markdown("#### 🛡️ Escalation Breakdown")
        esc_df = DATA.groupby("intent")["escalated"].mean().reset_index()
        esc_df["Escalation Rate (%)"] = (esc_df["escalated"] * 100).round(1)
        st.dataframe(
            esc_df[["intent", "Escalation Rate (%)"]].rename(columns={"intent": "Intent"}),
            use_container_width=True,
            hide_index=True
        )

    # Interactive Similarity Simulator
    st.markdown("---")
    st.markdown("### 🔬 Live Semantic Intent Simulator")
    st.caption("Test how any custom query maps to the 5,000-row TF-IDF vector space in real time.")
    
    sim_query = st.text_input("Enter a test student inquiry:", value="Where can I download my examination hall ticket?")
    if sim_query:
        sim_intent, sim_conf, sim_esc, matched_row_query = classify(sim_query)
        res_col1, res_col2, res_col3 = st.columns(3)
        with res_col1:
            st.metric("Predicted Intent", sim_intent.replace("_", " ").title())
        with res_col2:
            st.metric("Semantic Confidence", f"{sim_conf:.1%}")
        with res_col3:
            st.metric("Escalation Flag", "Yes (Human Needed)" if sim_esc else "No (Automated)")
            
        st.markdown(f"**Closest Dataset Match**: *\"{matched_row_query}\"*")

# TAB 3: Campus Directory & Emergency Escalation
with tab_directory:
    st.markdown("### 🏛️ University Support Directory")
    st.markdown("Official verified campus desks for inquiries requiring human intervention or administrative processing.")
    
    dir_col1, dir_col2 = st.columns(2)
    
    with dir_col1:
        st.markdown("""
        <div class="chat-msg-card">
            <h4>💰 Finance & Accounts Office</h4>
            <p><strong>Location</strong>: Administrative Block, Ground Floor, Room 12</p>
            <p><strong>Hours</strong>: Mon – Fri: 9:30 AM – 4:00 PM</p>
            <p><strong>Email</strong>: <code>accounts@campus.edu</code> · <strong>Phone</strong>: Ext. 2104</p>
            <p style="color:#94a3b8;font-size:0.85rem">Handles fee challans, refunds, scholarship verification, and duplicate receipts.</p>
        </div>
        
        <div class="chat-msg-card">
            <h4>📝 Examination Cell</h4>
            <p><strong>Location</strong>: Academic Block B, First Floor</p>
            <p><strong>Hours</strong>: Mon – Sat: 9:00 AM – 5:00 PM</p>
            <p><strong>Email</strong>: <code>examcell@campus.edu</code> · <strong>Phone</strong>: Ext. 2150</p>
            <p style="color:#94a3b8;font-size:0.85rem">Handles admit card disputes, revaluation forms, official transcripts, and grade issues.</p>
        </div>
        
        <div class="chat-msg-card">
            <h4>🧑‍💻 IT Services Helpdesk</h4>
            <p><strong>Location</strong>: Central Computing Center, 2nd Floor</p>
            <p><strong>Hours</strong>: 24/7 Portal Support</p>
            <p><strong>Email</strong>: <code>it-support@campus.edu</code> · <strong>Phone</strong>: Ext. 2999</p>
            <p style="color:#94a3b8;font-size:0.85rem">Handles student ERP login, Wi-Fi MAC registration, and LMS assignment errors.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with dir_col2:
        st.markdown("""
        <div class="chat-msg-card">
            <h4>💙 Counseling & Mental Health Center</h4>
            <p><strong>Location</strong>: Student Wellness Center, Room 104</p>
            <p><strong>Hours</strong>: Mon – Sat: 8:30 AM – 7:00 PM (Emergency 24/7)</p>
            <p><strong>Helpline</strong>: <code>1800-CAMPUS-CARE</code> (Toll-Free, 100% Confidential)</p>
            <p style="color:#94a3b8;font-size:0.85rem">Licensed counselors offering confidential mental health, anxiety, and academic stress support.</p>
        </div>
        
        <div class="chat-msg-card">
            <h4>🛡️ Anti-Ragging & Internal Complaints Committee</h4>
            <p><strong>Location</strong>: Office of Dean, Student Welfare</p>
            <p><strong>Emergency Contact</strong>: <code>1800-180-5522</code> (National Anti-Ragging Toll-Free)</p>
            <p><strong>Email</strong>: <code>grievance@campus.edu</code></p>
            <p style="color:#94a3b8;font-size:0.85rem">Zero tolerance for bullying, harassment, and discrimination. Immediate protective escalation.</p>
        </div>
        
        <div class="chat-msg-card">
            <h4>🛏️ Chief Hostel Warden Office</h4>
            <p><strong>Location</strong>: Residential Block A, Warden Complex</p>
            <p><strong>Hours</strong>: Mon – Sun: 8:00 AM – 8:00 PM</p>
            <p><strong>Email</strong>: <code>hostelwarden@campus.edu</code> · <strong>Phone</strong>: Ext. 2400</p>
            <p style="color:#94a3b8;font-size:0.85rem">Handles hostel room allotment, mess committee issues, night passes, and maintenance.</p>
        </div>
        """, unsafe_allow_html=True)

# Footer Note
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#64748b; font-size:0.8rem; padding: 0.5rem 0 1.5rem;">
    🎓 <strong>CampusCare Student Support AI Platform</strong> · Integrated with 5,000 verified student query patterns.<br>
    Official university policies supersede automated responses. Sensitive grievances are escalated to authorized campus staff.
</div>
""", unsafe_allow_html=True)

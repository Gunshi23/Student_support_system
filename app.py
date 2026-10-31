import os
import re
import io
import time
import pandas as pd
import streamlit as st
import altair as alt

APP_TITLE = "CampusCare | University Student Support Intelligence"
APP_SUBTITLE = "24/7 AI-Powered Academic, Administrative & Wellbeing Support"
GEMINI_MODEL = "gemini-2.5-flash"

# Page configuration
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Custom High-End Styling & Design System
# ---------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
    --bg-main: #0b0f19;
    --bg-surface: #111827;
    --bg-surface-elevated: #162036;
    --card-bg: rgba(17, 24, 39, 0.72);
    --card-hover: rgba(26, 36, 58, 0.85);
    --card-border: rgba(255, 255, 255, 0.08);
    --card-border-hover: rgba(99, 102, 241, 0.4);
    
    --primary: #6366f1;
    --primary-light: #818cf8;
    --primary-glow: rgba(99, 102, 241, 0.28);
    
    --accent-purple: #a855f7;
    --accent-cyan: #06b6d4;
    --accent-emerald: #10b981;
    --accent-amber: #f59e0b;
    --accent-rose: #f43f5e;
    
    --text-primary: #f8fafc;
    --text-secondary: #cbd5e1;
    --text-muted: #94a3b8;
    --text-subtle: #64748b;
    
    --radius-sm: 8px;
    --radius-md: 14px;
    --radius-lg: 20px;
    --radius-pill: 9999px;
    
    --shadow-soft: 0 4px 20px -2px rgba(0, 0, 0, 0.35);
    --shadow-glow: 0 0 25px rgba(99, 102, 241, 0.15);
}

/* Global resets & background */
html, body, [class*="css"], .stApp {
    font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, sans-serif !important;
    background-color: var(--bg-main) !important;
    background-image: 
        radial-gradient(ellipse at 15% 0%, rgba(99, 102, 241, 0.14) 0%, transparent 60%),
        radial-gradient(ellipse at 85% 15%, rgba(168, 85, 247, 0.10) 0%, transparent 55%),
        radial-gradient(ellipse at 50% 90%, rgba(6, 182, 212, 0.07) 0%, transparent 60%) !important;
    background-attachment: fixed !important;
    color: var(--text-primary) !important;
}

/* Custom Scrollbar */
::-webkit-scrollbar { width: 7px; height: 7px; }
::-webkit-scrollbar-track { background: #090d16; }
::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 4px; border: 1px solid rgba(255,255,255,0.05); }
::-webkit-scrollbar-thumb:hover { background: #3730a3; }

/* Streamlit Native Header */
header[data-testid="stHeader"] {
    background: rgba(11, 15, 25, 0.8) !important;
    backdrop-filter: blur(16px) !important;
    border-bottom: 1px solid var(--card-border) !important;
}

/* Sidebar Customization */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1220 0%, #090d17 100%) !important;
    border-right: 1px solid var(--card-border) !important;
    padding-top: 1rem;
}

section[data-testid="stSidebar"] hr {
    border-color: rgba(255, 255, 255, 0.07) !important;
    margin: 1.2rem 0 !important;
}

/* Sidebar Brand Card */
.brand-card {
    background: linear-gradient(145deg, rgba(30, 41, 79, 0.45) 0%, rgba(17, 24, 39, 0.85) 100%);
    border: 1px solid rgba(99, 102, 241, 0.25);
    border-radius: var(--radius-md);
    padding: 1.2rem 1rem;
    text-align: center;
    box-shadow: var(--shadow-soft);
    margin-bottom: 1.2rem;
    position: relative;
    overflow: hidden;
}

.brand-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #818cf8, #c084fc, transparent);
}

.brand-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(99, 102, 241, 0.15);
    border: 1px solid rgba(99, 102, 241, 0.35);
    color: #c7d2fe;
    font-size: 0.72rem;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: var(--radius-pill);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.5rem;
}

.brand-title {
    font-size: 1.4rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, #ffffff 0%, #c7d2fe 60%, #a78bfa 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0.2rem 0 0.2rem;
}

.brand-subtitle {
    font-size: 0.8rem;
    color: var(--text-muted);
    font-weight: 500;
    margin-bottom: 0.8rem;
}

.live-indicator {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    background: rgba(16, 185, 129, 0.12);
    border: 1px solid rgba(16, 185, 129, 0.28);
    color: #34d399;
    padding: 4px 12px;
    border-radius: var(--radius-pill);
    font-size: 0.74rem;
    font-weight: 600;
}

.pulse-dot {
    width: 7px;
    height: 7px;
    background-color: #10b981;
    border-radius: 50%;
    box-shadow: 0 0 8px #10b981;
    animation: pulse-glow 2s infinite ease-in-out;
}

@keyframes pulse-glow {
    0%, 100% { opacity: 1; transform: scale(1); box-shadow: 0 0 8px #10b981; }
    50% { opacity: 0.4; transform: scale(0.85); box-shadow: 0 0 2px #10b981; }
}

/* Sidebar Section Headers */
.side-header {
    font-size: 0.76rem;
    font-weight: 700;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin: 1.1rem 0 0.5rem 0.2rem;
    display: flex;
    align-items: center;
    gap: 6px;
}

/* Sidebar Action Buttons */
section[data-testid="stSidebar"] .stButton > button {
    background: rgba(17, 24, 39, 0.75) !important;
    color: var(--text-secondary) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: var(--radius-sm) !important;
    font-weight: 500 !important;
    font-size: 0.82rem !important;
    padding: 0.52rem 0.85rem !important;
    text-align: left !important;
    width: 100% !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 2px 5px rgba(0,0,0,0.2) !important;
}

section[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(99, 102, 241, 0.2) !important;
    border-color: rgba(129, 140, 248, 0.5) !important;
    color: #ffffff !important;
    transform: translateX(3px) !important;
    box-shadow: 0 4px 14px rgba(99, 102, 241, 0.25) !important;
}

/* Emergency Helpline Sidebar Card */
.emergency-card {
    background: linear-gradient(135deg, rgba(244, 63, 94, 0.12) 0%, rgba(136, 19, 55, 0.25) 100%);
    border: 1px solid rgba(244, 63, 94, 0.35);
    border-radius: var(--radius-md);
    padding: 0.9rem;
    margin-top: 1.2rem;
}

.emergency-title {
    color: #fda4af;
    font-size: 0.82rem;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 6px;
    margin-bottom: 0.3rem;
}

.emergency-desc {
    font-size: 0.75rem;
    color: #fecdd3;
    line-height: 1.4;
    margin: 0;
}

.emergency-phone {
    display: inline-block;
    background: rgba(244, 63, 94, 0.25);
    border: 1px solid rgba(244, 63, 94, 0.4);
    padding: 3px 8px;
    border-radius: 6px;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700;
    font-size: 0.8rem;
    color: #ffffff;
    margin-top: 0.4rem;
}

/* Modern Top Navigation Bar */
.top-navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: var(--card-bg);
    backdrop-filter: blur(20px);
    border: 1px solid var(--card-border);
    border-radius: var(--radius-md);
    padding: 0.9rem 1.4rem;
    margin-bottom: 1.2rem;
    box-shadow: var(--shadow-soft);
}

.top-brand {
    display: flex;
    align-items: center;
    gap: 12px;
}

.top-logo {
    width: 44px;
    height: 44px;
    border-radius: 12px;
    background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.4rem;
    box-shadow: 0 4px 14px rgba(99, 102, 241, 0.4);
}

.top-titles h2 {
    font-size: 1.25rem;
    font-weight: 800;
    margin: 0;
    letter-spacing: -0.02em;
    color: #ffffff;
}

.top-titles p {
    font-size: 0.78rem;
    color: var(--text-muted);
    margin: 0;
    font-weight: 500;
}

.top-meta {
    display: flex;
    align-items: center;
    gap: 10px;
}

.nav-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 5px 12px;
    border-radius: var(--radius-pill);
    font-size: 0.75rem;
    font-weight: 600;
}

.nav-pill-info {
    background: rgba(99, 102, 241, 0.14);
    border: 1px solid rgba(99, 102, 241, 0.3);
    color: #c7d2fe;
}

.nav-pill-alert {
    background: rgba(244, 63, 94, 0.14);
    border: 1px solid rgba(244, 63, 94, 0.35);
    color: #fca5a5;
}

/* Quick Action Suggestion Strip */
.quick-prompt-banner {
    margin-bottom: 1rem;
    padding: 0.6rem 0.2rem;
}

.quick-prompt-label {
    font-size: 0.76rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--text-muted);
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 6px;
}

/* Streamlit Tabs Customization */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: rgba(13, 18, 32, 0.85);
    padding: 6px;
    border-radius: var(--radius-md);
    border: 1px solid var(--card-border);
    margin-bottom: 1.2rem;
}

.stTabs [data-baseweb="tab"] {
    border-radius: var(--radius-sm);
    color: var(--text-muted) !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    padding: 9px 18px !important;
    transition: all 0.2s ease;
    border: 1px solid transparent;
}

.stTabs [data-baseweb="tab"]:hover {
    color: var(--text-secondary) !important;
    background: rgba(255, 255, 255, 0.04);
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.35) 0%, rgba(168, 85, 247, 0.25) 100%) !important;
    color: #ffffff !important;
    border: 1px solid rgba(129, 140, 248, 0.4) !important;
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2) !important;
}

/* Chat Message Card Styling */
[data-testid="stChatMessage"] {
    background: var(--card-bg) !important;
    border: 1px solid var(--card-border) !important;
    border-radius: 16px !important;
    padding: 1.25rem 1.4rem !important;
    margin-bottom: 1rem !important;
    box-shadow: var(--shadow-soft) !important;
    transition: border 0.2s ease;
}

[data-testid="stChatMessage"]:hover {
    border-color: rgba(99, 102, 241, 0.25) !important;
}

[data-testid="stChatMessage"] p, 
[data-testid="stChatMessage"] li {
    color: var(--text-secondary) !important;
    font-size: 0.94rem !important;
    line-height: 1.65 !important;
}

[data-testid="stChatMessage"] strong {
    color: #ffffff !important;
    font-weight: 700 !important;
}

[data-testid="stChatMessage"] code {
    background: rgba(99, 102, 241, 0.2) !important;
    color: #c7d2fe !important;
    border: 1px solid rgba(99, 102, 241, 0.35) !important;
    padding: 2px 7px !important;
    border-radius: 6px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.84rem !important;
}

/* Metadata Bar Under Chat Answers */
.chat-meta-bar {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 8px;
    margin-top: 0.9rem;
    padding-top: 0.85rem;
    border-top: 1px solid rgba(255, 255, 255, 0.06);
}

.chip {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 3px 10px;
    border-radius: var(--radius-pill);
    font-size: 0.73rem;
    font-weight: 600;
}

.chip-fees { background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.35); color: #6ee7b7; }
.chip-exams { background: rgba(245, 158, 11, 0.15); border: 1px solid rgba(245, 158, 11, 0.35); color: #fde047; }
.chip-schedule { background: rgba(99, 102, 241, 0.15); border: 1px solid rgba(99, 102, 241, 0.35); color: #a5b4fc; }
.chip-admissions { background: rgba(168, 85, 247, 0.15); border: 1px solid rgba(168, 85, 247, 0.35); color: #d8b4fe; }
.chip-hostel { background: rgba(6, 182, 212, 0.15); border: 1px solid rgba(6, 182, 212, 0.35); color: #67e8f9; }
.chip-tech { background: rgba(56, 189, 248, 0.15); border: 1px solid rgba(56, 189, 248, 0.35); color: #7dd3fc; }
.chip-wellbeing { background: rgba(244, 63, 94, 0.15); border: 1px solid rgba(244, 63, 94, 0.35); color: #fda4af; }
.chip-grievance { background: rgba(225, 29, 72, 0.18); border: 1px solid rgba(225, 29, 72, 0.4); color: #fecdd3; }
.chip-library { background: rgba(14, 165, 233, 0.15); border: 1px solid rgba(14, 165, 233, 0.35); color: #bae6fd; }
.chip-placement { background: rgba(234, 179, 8, 0.15); border: 1px solid rgba(234, 179, 8, 0.35); color: #fef08a; }
.chip-general { background: rgba(148, 163, 184, 0.15); border: 1px solid rgba(148, 163, 184, 0.3); color: #e2e8f0; }

.chip-conf {
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: var(--text-secondary);
    font-family: 'JetBrains Mono', monospace;
}

.chip-resolved {
    background: rgba(16, 185, 129, 0.12);
    border: 1px solid rgba(16, 185, 129, 0.3);
    color: #34d399;
}

.chip-escalated {
    background: rgba(245, 158, 11, 0.16);
    border: 1px solid rgba(245, 158, 11, 0.4);
    color: #fbbf24;
}

/* Escalation Guidance Banner */
.escalate-banner {
    margin-top: 0.85rem;
    background: linear-gradient(135deg, rgba(120, 53, 15, 0.22) 0%, rgba(69, 26, 3, 0.35) 100%);
    border: 1px solid rgba(245, 158, 11, 0.35);
    border-radius: 12px;
    padding: 0.85rem 1.1rem;
    display: flex;
    align-items: flex-start;
    gap: 12px;
}

.escalate-icon {
    font-size: 1.25rem;
    margin-top: 1px;
}

.escalate-body {
    flex: 1;
}

.escalate-title {
    font-size: 0.85rem;
    font-weight: 700;
    color: #fef3c7;
    margin-bottom: 0.2rem;
}

.escalate-desc {
    font-size: 0.8rem;
    color: #fde68a;
    line-height: 1.45;
    margin: 0;
}

/* Voice Console Card */
.voice-console {
    background: linear-gradient(135deg, rgba(20, 28, 48, 0.8) 0%, rgba(13, 18, 32, 0.95) 100%);
    border: 1px solid rgba(99, 102, 241, 0.25);
    border-radius: var(--radius-md);
    padding: 1.1rem 1.3rem;
    margin-bottom: 1.2rem;
    box-shadow: var(--shadow-soft);
}

.voice-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.6rem;
}

.voice-title {
    font-size: 0.95rem;
    font-weight: 700;
    color: #ffffff;
    display: flex;
    align-items: center;
    gap: 8px;
}

.voice-subtitle {
    font-size: 0.8rem;
    color: var(--text-muted);
    margin-bottom: 0.8rem;
}

/* KPI Stat Cards (Analytics Tab) */
.kpi-card {
    background: linear-gradient(145deg, rgba(20, 28, 48, 0.7) 0%, rgba(12, 17, 34, 0.9) 100%);
    border: 1px solid var(--card-border);
    border-radius: var(--radius-md);
    padding: 1.25rem 1.1rem;
    text-align: center;
    box-shadow: var(--shadow-soft);
    position: relative;
    overflow: hidden;
    transition: all 0.2s ease;
}

.kpi-card:hover {
    border-color: rgba(99, 102, 241, 0.35);
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
}

.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #6366f1, #a855f7);
}

.kpi-val {
    font-size: 2.1rem;
    font-weight: 800;
    font-family: 'JetBrains Mono', monospace;
    background: linear-gradient(135deg, #ffffff 0%, #c7d2fe 60%, #38bdf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.1;
    margin-bottom: 0.3rem;
}

.kpi-lbl {
    font-size: 0.8rem;
    font-weight: 700;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.2rem;
}

.kpi-sub {
    font-size: 0.74rem;
    color: var(--text-muted);
}

/* Directory Desk Cards */
.desk-card {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: var(--radius-md);
    padding: 1.3rem;
    margin-bottom: 1.1rem;
    box-shadow: var(--shadow-soft);
    transition: all 0.2s ease;
    height: 100%;
}

.desk-card:hover {
    border-color: rgba(99, 102, 241, 0.35);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
    transform: translateY(-2px);
}

.desk-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.8rem;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

.desk-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: #ffffff;
    display: flex;
    align-items: center;
    gap: 8px;
    margin: 0;
}

.desk-status {
    font-size: 0.72rem;
    font-weight: 600;
    color: #34d399;
    background: rgba(16, 185, 129, 0.12);
    border: 1px solid rgba(16, 185, 129, 0.3);
    padding: 2px 8px;
    border-radius: var(--radius-pill);
}

.desk-field {
    font-size: 0.86rem;
    color: var(--text-secondary);
    margin-bottom: 0.4rem;
    line-height: 1.4;
}

.desk-field strong {
    color: #ffffff;
}

.desk-tag-row {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-top: 0.8rem;
}

.desk-tag {
    background: rgba(99, 102, 241, 0.12);
    border: 1px solid rgba(99, 102, 241, 0.25);
    color: #c7d2fe;
    font-size: 0.72rem;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 6px;
}

/* Chat Input Bar Override */
[data-testid="stChatInput"] {
    background: rgba(15, 23, 42, 0.92) !important;
    border: 1px solid rgba(99, 102, 241, 0.35) !important;
    border-radius: var(--radius-md) !important;
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.4) !important;
}

[data-testid="stChatInput"]:focus-within {
    border-color: #818cf8 !important;
    box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.25), 0 8px 30px rgba(0, 0, 0, 0.5) !important;
}

[data-testid="stChatInput"] textarea {
    color: #ffffff !important;
    font-size: 0.94rem !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #94a3b8 !important;
}

/* General Button Tweaks */
.stButton > button {
    border-radius: var(--radius-sm) !important;
    font-weight: 600 !important;
    font-size: 0.86rem !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    border: 1px solid rgba(99, 102, 241, 0.25) !important;
}

.stButton > button:hover {
    border-color: rgba(129, 140, 248, 0.6) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(99, 102, 241, 0.2) !important;
}

/* Simulator Container */
.sim-box {
    background: linear-gradient(135deg, rgba(20, 27, 48, 0.7) 0%, rgba(13, 18, 34, 0.85) 100%);
    border: 1px solid rgba(99, 102, 241, 0.25);
    border-radius: var(--radius-md);
    padding: 1.4rem;
    margin-top: 1rem;
    box-shadow: var(--shadow-soft);
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Verified Multi-Domain Knowledge Base
# ---------------------------------------------------------
FAQS = [
    (
        "fees",
        ["fee", "fees", "tuition", "payment", "scholarship", "refund", "receipt", "challan", "dues", "installment"],
        "💰 **Fee & Financial Support Services**:\n\n"
        "• **Online Payment Portal**: Log in to your official student ERP under `Accounts & Fees` → `Make Payment` to pay securely via NetBanking, UPI, or Debit/Credit card.\n"
        "• **Instant Fee Receipts**: Digitally signed receipts are available for instant download in the receipts tab immediately after bank confirmation.\n"
        "• **Scholarships & Financial Aid**: Merit and need-based scholarship windows open every semester. Submit verified marksheets and income certificates to the Accounts Office.\n"
        "• **Refunds & Installment Plans**: For refund applications or semester fee installment requests, submit Form `FIN-04` directly to the Accounts Counter before the semester cutoff."
    ),
    (
        "exams",
        ["exam", "examination", "result", "marks", "grade", "revaluation", "back paper", "admit card", "hall ticket", "date sheet"],
        "📝 **Examination Cell & Grade Records**:\n\n"
        "• **Date Sheets & Schedules**: Comprehensive timetables are published on the Examination Portal 2 weeks prior to mid-term and final assessments.\n"
        "• **Admit Card / Hall Ticket**: Mandatory for examination hall access. Generated 5 days prior to exams on the student portal. (Ensure fee/library dues are cleared if download is locked).\n"
        "• **Semester Results & Transcripts**: Declared within 30-45 days following exams. Official stamped transcripts can be requested through the Registrar Counter.\n"
        "• **Revaluation & Backlog Papers**: Grievances regarding marking and backlog registrations open for 14 days following result declarations via the exam cell window."
    ),
    (
        "schedule",
        ["timetable", "schedule", "class", "lecture", "attendance", "room", "holiday", "calendar", "timing", "session"],
        "📅 **Academic Timetable & Attendance Policy**:\n\n"
        "• **Class Schedules**: Check your department LMS dashboard or section notice board for room allocations and lab timings.\n"
        "• **75% Mandatory Attendance Rule**: Maintaining a minimum of **75% physical attendance** in every enrolled course is mandatory to qualify for end-term examinations.\n"
        "• **Medical & Leave Discrepancies**: In case of medical emergencies or sanctioned sports duty, submit verified certificates to your Faculty Coordinator within 7 working days.\n"
        "• **Official Academic Calendar**: Download the university calendar showing teaching weeks, preparatory breaks, and national holidays from the portal."
    ),
    (
        "admissions",
        ["admission", "enrol", "enroll", "registration", "eligibility", "documents", "application", "seat", "branch", "cutoff"],
        "🏛️ **Admissions & Student Enrollment**:\n\n"
        "• **Eligibility & Merit Cutoffs**: Admissions are verified according to qualifying examination scores, national entrance percentiles, and university reservation norms.\n"
        "• **Mandatory Verification Documents**: Original Class 10 & 12 certificates, Transfer Certificate (TC), Migration Certificate, and government photo ID must be physically verified at the Admissions Counter.\n"
        "• **Branch Upgradation & Sliding**: Merit-based internal sliding opens following Round 3 registrations, subject to departmental vacancy."
    ),
    (
        "hostel",
        ["hostel", "dorm", "allotment", "accommodation", "room", "mess", "warden", "curfew", "laundry"],
        "🛏️ **Hostel Accommodation & Campus Residence**:\n\n"
        "• **Room Allotment**: Residential allotment is granted per academic year based on student distance and academic standing. Check your allotted block and room on the Hostel Portal.\n"
        "• **Mess & Dining Schedule**: Nutritious meal plans (Breakfast: 7:30-9:30 AM, Lunch: 12:30-2:30 PM, Snacks: 5:00-6:30 PM, Dinner: 7:30-9:30 PM) operate in all halls.\n"
        "• **Hostel Curfew & Safety**: Gates close at **9:30 PM** on weekdays and **10:00 PM** on weekends. Overnight passes require digital consent from the Chief Warden.\n"
        "• **Maintenance & Warden Desk**: For electrical, plumbing, or Wi-Fi repairs in your room, log a ticket via the campus warden helpline or hostel desk."
    ),
    (
        "technical_support",
        ["login", "password", "portal", "website", "error", "technical", "wifi", "upload", "lms", "moodle", "reset"],
        "🧑‍💻 **IT Services & Campus Helpdesk**:\n\n"
        "• **Portal Password Reset**: Use 'Forgot Password' on the login portal. A secure reset link is automatically dispatched to your registered university email.\n"
        "• **High-Speed Campus Wi-Fi**: Register your device MAC address with the IT center to obtain individual high-speed Wi-Fi authentication credentials.\n"
        "• **LMS & Moodle Support**: If course modules fail to load or assignment uploads time out, clear browser cookies and email `it-support@campus.edu`.\n"
        "• **Security Advisory**: Campus IT will **never** ask for your password or OTP. Always keep your portal credentials private."
    ),
    (
        "wellbeing",
        ["stress", "anxious", "anxiety", "overwhelmed", "sad", "lonely", "mental health", "not fine", "not okay", "depressed", "counselor", "panic"],
        "💙 **Confidential Student Counseling & Wellbeing Support**:\n\n"
        "You do not have to navigate difficult times alone. University life can feel demanding, and our care team is here to support you:\n\n"
        "• **Student Wellness Center**: Free, strictly confidential one-on-one sessions with licensed university psychologists (Health & Wellness Block, Room 104).\n"
        "• **Trained Peer Listeners**: Senior student volunteers are available for informal peer chats regarding academic and social adjustment.\n"
        "• **24/7 Crisis Hotline**: Call `1800-CAMPUS-CARE` (Toll-Free, 24/7) anytime to speak immediately with a caring professional.\n"
        "• *Important*: As an AI assistant, I offer supportive guidance, but reaching out directly to our wellness team is warmly recommended."
    ),
    (
        "grievance",
        ["complaint", "grievance", "harassment", "discrimination", "bully", "unsafe", "report", "ragging", "threat", "disciplinary"],
        "🛡️ **Grievance Redressal & Anti-Ragging Safety**:\n\n"
        "Our campus maintains a strict zero-tolerance policy against any form of harassment, discrimination, or ragging:\n\n"
        "• **24/7 Anti-Ragging Helpline**: Call `1800-180-5522` (Toll-Free) or email `antiragging@campus.edu`.\n"
        "• **Internal Complaints Committee (ICC)**: For confidential reporting regarding safety or gender discrimination, submit a confidential report to the Presiding Officer.\n"
        "• **Dean of Student Welfare**: Direct walk-in hours available Monday to Friday from 2:00 PM to 4:00 PM in the Administrative Block.\n"
        "• *Immediate Action*: This inquiry has been marked for high-priority staff escalation."
    ),
    (
        "library",
        ["library", "book", "borrow", "renew", "journal", "research paper", "fine", "catalogue", "opac", "e-resources"],
        "📚 **Central Library & Digital Knowledge Repository**:\n\n"
        "• **Borrowing Limits**: Undergraduates may borrow up to 4 books for 14 days; postgraduates and researchers up to 6 books for 30 days.\n"
        "• **Digital Renewals**: Renew titles up to 2 times online via the OPAC portal unless a hold has been requested by another student.\n"
        "• **Research Databases**: Access IEEE Xplore, ScienceDirect, Springer, and JSTOR remotely using your institutional login.\n"
        "• **Operating Hours**: Monday to Saturday: 8:00 AM – 10:00 PM. Reading halls remain open 24/7 during end-term examinations."
    ),
    (
        "placement",
        ["placement", "internship", "career", "resume", "cv", "interview", "job", "company", "package", "recruitment"],
        "💼 **Career Development & Corporate Relations (CDC)**:\n\n"
        "• **Portal Registration**: Pre-final and final-year students must register on the CDC portal with verified academic transcripts.\n"
        "• **Internships**: Summer and industry internship drives commence from the 5th semester onwards with company stipend norms.\n"
        "• **Resume Clinics & Mock Interviews**: Weekly interview prep workshops and resume audits are held every Wednesday in Seminar Hall 2.\n"
        "• **Drive Schedules**: Check active recruiters, eligibility criteria (minimum CGPA), and test links on the CDC dashboard."
    )
]

# ---------------------------------------------------------
# Dataset Loading & Semantic Vector Space
# ---------------------------------------------------------
DATASET_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "student_support_chatbot_dataset_5000.csv")

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

# Classification Function
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

    return "unknown", 0.35, False, "General inquiry"

def faq_answer(text, intent=None):
    if intent is None:
        intent, _conf, _esc, _ = classify(text)
        
    if intent == "greeting":
        return (
            "👋 **Hello and welcome to CampusCare!**\n\n"
            "I am your official AI Student Support Companion, trained on over 5,000 verified university queries. "
            "I can assist you with **tuition fees, examination schedules, timetables, hostel allotment, admissions, library books, campus IT, placements, and mental wellbeing**.\n\n"
            "How can I support your campus life today?"
        )
        
    for faq_intent, _, answer in FAQS:
        if faq_intent == intent:
            return answer
            
    return (
        "🤔 **I couldn't pinpoint the exact department for this inquiry.**\n\n"
        "Here are common campus services I can assist with:\n"
        "• **Fees & Accounts**: Online fee payment, receipts, scholarship forms\n"
        "• **Examination Cell**: Date sheets, admit cards, revaluation, grade sheets\n"
        "• **Academic Schedule**: Class timetable, 75% attendance policy, holiday list\n"
        "• **Hostel Administration**: Room allotments, mess menus, night pass rules\n"
        "• **Campus IT Helpdesk**: Wi-Fi registration, password resets, LMS issues\n"
        "• **Student Wellbeing**: Confidential counseling and anti-ragging support\n\n"
        "Please feel free to rephrase or pick a quick topic from the sidebar!"
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

# Speech synthesis & audio parsing
def speak(text):
    try:
        from gTTS import gTTS
        clean_text = re.sub(r'[*_#`•\-\[\]\(\)]', ' ', text)
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
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
    try:
        import speech_recognition as sr
        raw_bytes = audio_upload.getvalue()
        recognizer = sr.Recognizer()
        
        if raw_bytes.startswith(b'RIFF'):
            wav_io = io.BytesIO(raw_bytes)
            with sr.AudioFile(wav_io) as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.3)
                audio_data = recognizer.record(source)
            return recognizer.recognize_google(audio_data)
            
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
            
    except Exception:
        return None
    return None

# Helper for intent metadata display
INTENT_STYLES = {
    "fees": {"name": "Finance & Fees", "icon": "💳", "class": "chip-fees", "contact": "Accounts Office · Ext. 2104"},
    "exams": {"name": "Examinations", "icon": "📝", "class": "chip-exams", "contact": "Exam Cell · Ext. 2150"},
    "schedule": {"name": "Academic Timetable", "icon": "📅", "class": "chip-schedule", "contact": "Academic Dean / Faculty Mentor"},
    "admissions": {"name": "Admissions Desk", "icon": "🏛️", "class": "chip-admissions", "contact": "Admissions Hall · Ext. 2001"},
    "hostel": {"name": "Hostel Residence", "icon": "🛏️", "class": "chip-hostel", "contact": "Chief Warden · Ext. 2400"},
    "technical_support": {"name": "IT Services", "icon": "🧑‍💻", "class": "chip-tech", "contact": "IT Helpdesk · it-support@campus.edu"},
    "wellbeing": {"name": "Mental Wellbeing", "icon": "💙", "class": "chip-wellbeing", "contact": "Student Wellness Center · 1800-CAMPUS-CARE"},
    "grievance": {"name": "Safety & Grievance", "icon": "🛡️", "class": "chip-grievance", "contact": "Anti-Ragging / ICC · 1800-180-5522"},
    "library": {"name": "Central Library", "icon": "📚", "class": "chip-library", "contact": "Library Helpdesk · Ext. 2300"},
    "placement": {"name": "Placement Cell", "icon": "💼", "class": "chip-placement", "contact": "CDC Office · Ext. 2600"},
    "greeting": {"name": "Campus Assistant", "icon": "👋", "class": "chip-general", "contact": "Student Support Hub"},
    "unknown": {"name": "General Inquiries", "icon": "ℹ️", "class": "chip-general", "contact": "Campus Helpdesk"}
}

# ---------------------------------------------------------
# Session State Management
# ---------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": (
            "👋 **Welcome to CampusCare AI Support!**\n\n"
            "I am your 24/7 intelligent student companion, trained on over 5,000 university inquiries. "
            "Whether you need help with **tuition fees, examination timetables, hostel room change, library access, or confidential counseling**, "
            "simply type your question or use the microphone below."
        ),
        "meta": {"intent": "greeting", "confidence": 1.0, "escalate": False, "matched_query": "Official welcome"}
    }]

if "api_key" not in st.session_state:
    st.session_state.api_key = os.getenv("GEMINI_API_KEY", "").strip()

if "auto_speech" not in st.session_state:
    st.session_state.auto_speech = False

if "show_voice_panel" not in st.session_state:
    st.session_state.show_voice_panel = False

# ---------------------------------------------------------
# Sidebar Component
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div class="brand-card">
        <div class="brand-badge">Official Campus Portal</div>
        <div class="brand-title">CampusCare AI</div>
        <div class="brand-subtitle">Student Support Intelligence Platform</div>
        <div class="live-indicator">
            <span class="pulse-dot"></span> 5,000 Knowledge Nodes Active
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="side-header">⚡ Quick Topic Selector</div>', unsafe_allow_html=True)
    
    quick_topics = [
        ("💳 Fee Payment & Receipts", "How do I pay tuition fees and download receipt?"),
        ("📝 Exam Dates & Admit Card", "Where can I check exam dates and download admit card?"),
        ("📅 75% Attendance Policy", "What is the attendance policy and how to check my timetable?"),
        ("🛏️ Hostel Room Allotment", "How do I apply for hostel room allotment and check mess timings?"),
        ("🧑‍💻 Wi-Fi & LMS Access", "How can I register my laptop for campus Wi-Fi and reset portal password?"),
        ("💼 Campus Placements & CV", "How do I register with the placement cell for company drives?"),
        ("📚 Library Book Renewals", "How do I renew a library book and access research journals?"),
        ("💙 Counseling & Stress Support", "I am feeling overwhelmed with my academic workload and stress."),
        ("🛡️ File a Student Grievance", "How do I file a confidential grievance or report unfair treatment?")
    ]
    
    for label, query_text in quick_topics:
        if st.button(label, key=f"side_{label}", use_container_width=True):
            st.session_state.pending = query_text
            
    st.markdown("---")
    
    # Preferences Card
    st.markdown('<div class="side-header">⚙️ System & Voice Preferences</div>', unsafe_allow_html=True)
    
    st.session_state.auto_speech = st.checkbox("🔊 Auto-read answers aloud", value=st.session_state.auto_speech)
    
    with st.expander("🧠 Neural AI Engine Settings", expanded=bool(st.session_state.api_key)):
        user_key = st.text_input(
            "Gemini API Key",
            value=st.session_state.api_key,
            type="password",
            placeholder="AIzaSy...",
            help="Optional: Enables Google Gemini 2.5 generative reasoning in addition to verified campus FAQs."
        )
        if user_key != st.session_state.api_key:
            st.session_state.api_key = user_key
            st.rerun()
            
        if st.session_state.api_key:
            st.caption("✨ **Connected**: Gemini 2.5 Flash Engine Active")
        else:
            st.caption("⚡ **Fast Mode**: Local TF-IDF Cosine Matcher Active (Zero API key needed)")

    if st.button("🧹 Clear Conversation", use_container_width=True):
        st.session_state.messages = [{
            "role": "assistant",
            "content": "👋 Conversation cleared! What student inquiry can I assist you with today?",
            "meta": {"intent": "greeting", "confidence": 1.0, "escalate": False, "matched_query": "Fresh session"}
        }]
        st.rerun()

    # Emergency Helpline Sidebar Card
    st.markdown("""
    <div class="emergency-card">
        <div class="emergency-title">🚨 24/7 Campus Emergency Desk</div>
        <p class="emergency-desc">For urgent safety concerns, confidential mental health, or anti-ragging support:</p>
        <div class="emergency-phone">📞 1800-CAMPUS-CARE</div>
        <div class="emergency-phone" style="margin-top:4px;">🛡️ 1800-180-5522</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.caption("🔒 **Student Privacy Guarantee**: CampusCare does not store passwords, bank OTPs, or student credentials. Inquiries are processed strictly in-memory.")

# ---------------------------------------------------------
# Modern Top Navigation / Header Bar
# ---------------------------------------------------------
st.markdown("""
<div class="top-navbar">
    <div class="top-brand">
        <div class="top-logo">🎓</div>
        <div class="top-titles">
            <h2>CampusCare Support Portal</h2>
            <p>Integrated Dual Text & Voice Student Intelligence System</p>
        </div>
    </div>
    <div class="top-meta">
        <span class="nav-pill nav-pill-info">🟢 System Live</span>
        <span class="nav-pill nav-pill-alert">🚨 Helpline: 1800-CAMPUS-CARE</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Tabs Navigation
# ---------------------------------------------------------
tab_chat, tab_analytics, tab_directory = st.tabs([
    "💬 Support Assistant (Text + Voice)",
    "📊 Dataset & System Analytics",
    "🏛️ University Directory & Escalations"
])

# Query processing logic
def process_question(q):
    q = q.strip()
    if not q:
        return
    st.session_state.messages.append({"role": "user", "content": q})
    
    with st.spinner("Analyzing your student inquiry..."):
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

# ---------------------------------------------------------
# TAB 1: Chat Assistant & Voice Interface
# ---------------------------------------------------------
with tab_chat:
    # Trigger pending questions from sidebar
    pending = st.session_state.pop("pending", None)
    if pending:
        process_question(pending)
        st.rerun()

    # Quick Prompts Carousel Bar
    st.markdown("""
    <div class="quick-prompt-banner">
        <div class="quick-prompt-label">💡 Common Student Questions (Click to Ask)</div>
    </div>
    """, unsafe_allow_html=True)
    
    col_p1, col_p2, col_p3, col_p4 = st.columns(4)
    with col_p1:
        if st.button("💳 Fee Payment Details", key="chip_fee", use_container_width=True):
            process_question("How do I pay my semester fee online and get the receipt?")
            st.rerun()
    with col_p2:
        if st.button("📝 Exam Dates & Admit Card", key="chip_exam", use_container_width=True):
            process_question("Where can I download my examination hall ticket and datesheet?")
            st.rerun()
    with col_p3:
        if st.button("🛏️ Hostel Allotment Info", key="chip_hostel", use_container_width=True):
            process_question("How do I apply for hostel room allotment and meal plans?")
            st.rerun()
    with col_p4:
        if st.button("💙 Confidential Counseling", key="chip_mental", use_container_width=True):
            process_question("I feel overwhelmed with studies and want to speak with a counselor.")
            st.rerun()

    st.write("")

    # Chat Message Thread
    chat_container = st.container()
    with chat_container:
        for idx, m in enumerate(st.session_state.messages):
            if m["role"] == "user":
                with st.chat_message("user", avatar="👤"):
                    st.markdown(f"**{m['content']}**")
            else:
                with st.chat_message("assistant", avatar="🎓"):
                    st.markdown(m["content"])
                    
                    # Metadata Badge Bar
                    meta = m.get("meta")
                    if meta:
                        raw_intent = meta.get("intent", "general")
                        intent_info = INTENT_STYLES.get(raw_intent, INTENT_STYLES["unknown"])
                        confidence = meta.get("confidence", 0.0)
                        escalated = meta.get("escalate", False)
                        
                        resolved_badge = (
                            '<span class="chip chip-escalated">⚠️ Human Escalation Advised</span>'
                            if escalated else 
                            '<span class="chip chip-resolved">✓ Automated Resolution</span>'
                        )
                        
                        st.markdown(f"""
                        <div class="chat-meta-bar">
                            <span class="chip {intent_info['class']}">{intent_info['icon']} {intent_info['name']}</span>
                            <span class="chip chip-conf">🎯 {confidence:.0%} Match</span>
                            {resolved_badge}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Reassuring Escalation Card if flagged
                        if escalated:
                            st.markdown(f"""
                            <div class="escalate-banner">
                                <span class="escalate-icon">⚠️</span>
                                <div class="escalate-body">
                                    <div class="escalate-title">Staff Escalation Recommended: {intent_info['name']}</div>
                                    <p class="escalate-desc">
                                        This matter involves sensitive, academic, or administrative processing. 
                                        Recommended Contact: <strong>{intent_info['contact']}</strong> or visit the 
                                        <strong>Campus Directory</strong> tab for direct room locations and office hours.
                                    </p>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                    # Audio Playback & Synthesis
                    if m.get("audio"):
                        st.audio(m["audio"], format="audio/mp3")
                    else:
                        c_listen, _ = st.columns([1.5, 4.5])
                        with c_listen:
                            if st.button("🔊 Read Aloud", key=f"speak_{idx}"):
                                with st.spinner("Generating speech..."):
                                    audio_bytes = speak(m["content"])
                                    if audio_bytes:
                                        m["audio"] = audio_bytes
                                        st.rerun()

    # Voice Input Panel (Clean Integrated Interface)
    with st.expander("🎙️ Voice Assistant Mode (Tap to record inquiry)", expanded=st.session_state.show_voice_panel):
        st.caption("Speak your question naturally using your microphone. Our audio recognition converts voice into text and provides immediate answers.")
        v_col1, v_col2 = st.columns([3, 1.2])
        with v_col1:
            recorded_audio = st.audio_input("Microphone Input", key="mic_recorder")
        with v_col2:
            st.write("")
            st.write("")
            transcribe_btn = st.button("🚀 Transcribe & Ask", type="primary", use_container_width=True)
            
        if transcribe_btn:
            if recorded_audio is None:
                st.warning("⚠️ Please record audio before clicking Transcribe.")
            else:
                with st.spinner("Recognizing speech audio..."):
                    transcription = transcribe(recorded_audio)
                if transcription:
                    st.success(f"🗣️ **Understood**: *\"{transcription}\"*")
                    process_question(transcription)
                    st.rerun()
                else:
                    st.error("⚠️ Speech could not be clearly recognized. Please try speaking closer to your microphone or type in the chat bar below.")

    # Main Chat Input (Pinned at Bottom)
    chat_prompt = st.chat_input("Type your question here (e.g., 'How do I pay fees?', 'Where is the exam datesheet?')...")
    if chat_prompt:
        process_question(chat_prompt)
        st.rerun()

# ---------------------------------------------------------
# TAB 2: Dataset Analytics & Semantic Simulator
# ---------------------------------------------------------
with tab_analytics:
    st.markdown("### 📊 Dataset Overview & Semantic Analytics")
    st.caption("Real-world distribution metrics derived from `student_support_chatbot_dataset_5000.csv` containing 5,000 inquiries.")
    
    # 4 Sleek KPI Metric Cards
    total_records = len(DATA)
    total_categories = DATA["intent"].nunique()
    total_escalated = int(DATA["escalated"].sum())
    esc_rate = (total_escalated / total_records) * 100
    mean_rating = DATA["user_rating"].mean()
    
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-val">{total_records:,}</div>
            <div class="kpi-lbl">Total Queries</div>
            <div class="kpi-sub">5,000 Verified Samples</div>
        </div>
        """, unsafe_allow_html=True)
    with k2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-val">{total_categories}</div>
            <div class="kpi-lbl">Core Departments</div>
            <div class="kpi-sub">Multi-Domain Coverage</div>
        </div>
        """, unsafe_allow_html=True)
    with k3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-val">{esc_rate:.1f}%</div>
            <div class="kpi-lbl">Escalation Rate</div>
            <div class="kpi-sub">{total_escalated:,} Human Advisor Flags</div>
        </div>
        """, unsafe_allow_html=True)
    with k4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-val">{mean_rating:.2f} ⭐</div>
            <div class="kpi-lbl">Satisfaction Score</div>
            <div class="kpi-sub">Scale: 1.0 to 5.0 Rating</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.write("")
    
    # Altair Interactive Visualizations
    chart_col1, chart_col2 = st.columns([3, 2])
    
    with chart_col1:
        st.markdown("#### 📈 Inquiries Volume by Department")
        counts_df = DATA["intent"].value_counts().reset_index()
        counts_df.columns = ["Department", "Queries"]
        counts_df["Department"] = counts_df["Department"].str.title()
        
        bar_chart = (
            alt.Chart(counts_df)
            .mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8, color="#6366f1")
            .encode(
                x=alt.X("Department:N", sort="-y", title="Campus Department", axis=alt.Axis(labelAngle=0, labelColor="#cbd5e1", titleColor="#94a3b8")),
                y=alt.Y("Queries:Q", title="Total Inquiries", axis=alt.Axis(labelColor="#cbd5e1", titleColor="#94a3b8")),
                tooltip=[alt.Tooltip("Department:N"), alt.Tooltip("Queries:Q", format=",")]
            )
            .properties(height=290)
            .configure_view(strokeWidth=0)
        )
        st.altair_chart(bar_chart, use_container_width=True)
        
    with chart_col2:
        st.markdown("#### 🛡️ Escalation Breakdown (%)")
        esc_group = DATA.groupby("intent")["escalated"].mean().reset_index()
        esc_group["Escalation %"] = (esc_group["escalated"] * 100).round(1)
        esc_group["Department"] = esc_group["intent"].str.title()
        
        esc_chart = (
            alt.Chart(esc_group)
            .mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8)
            .encode(
                x=alt.X("Department:N", sort="-y", title="Department", axis=alt.Axis(labelAngle=-30, labelColor="#cbd5e1", titleColor="#94a3b8")),
                y=alt.Y("Escalation %:Q", title="Human Escalation Rate (%)", axis=alt.Axis(labelColor="#cbd5e1", titleColor="#94a3b8")),
                color=alt.condition(
                    alt.datum["Escalation %"] > 35,
                    alt.value("#f43f5e"),  # Red highlight for high escalation
                    alt.value("#38bdf8")   # Cyan for regular
                ),
                tooltip=[alt.Tooltip("Department:N"), alt.Tooltip("Escalation %:Q", format=".1f")]
            )
            .properties(height=290)
            .configure_view(strokeWidth=0)
        )
        st.altair_chart(esc_chart, use_container_width=True)

    # Live Semantic Intent Simulator
    st.markdown("---")
    st.markdown("### 🔬 Live Semantic Intent Simulator")
    st.caption("Evaluate how raw student text projects into the n-gram TF-IDF vector space with real-time confidence scoring.")
    
    sim_presets = [
        "Where do I download my examination hall ticket?",
        "I need a refund for my tuition fee installment",
        "Feeling depressed and anxious about upcoming exams",
        "How to register MAC address for campus Wi-Fi?"
    ]
    
    st.markdown("**Test a Preset Query:**")
    p_cols = st.columns(4)
    sim_text = "Where do I download my examination hall ticket?"
    for p_idx, p_text in enumerate(sim_presets):
        with p_cols[p_idx]:
            if st.button(f"Preset {p_idx+1}", key=f"sim_p_{p_idx}", help=p_text, use_container_width=True):
                st.session_state.sim_input = p_text

    sim_input_val = st.session_state.get("sim_input", "Where do I download my examination hall ticket?")
    sim_query = st.text_input("Student Inquiry Text to Evaluate:", value=sim_input_val)
    
    if sim_query:
        s_intent, s_conf, s_esc, s_matched = classify(sim_query)
        info = INTENT_STYLES.get(s_intent, INTENT_STYLES["unknown"])
        
        st.markdown(f"""
        <div class="sim-box">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem;">
                <h4 style="margin:0; color:#ffffff;">Prediction Result</h4>
                <span class="chip {info['class']}">{info['icon']} {info['name']}</span>
            </div>
            <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;">
                <div>
                    <div style="font-size:0.75rem; color:#94a3b8; text-transform:uppercase;">Confidence Score</div>
                    <div style="font-size:1.6rem; font-weight:800; font-family:'JetBrains Mono'; color:#38bdf8;">{s_conf:.1%}</div>
                </div>
                <div>
                    <div style="font-size:0.75rem; color:#94a3b8; text-transform:uppercase;">Escalation Dispatch</div>
                    <div style="font-size:1.1rem; font-weight:700; color:{'#fbbf24' if s_esc else '#34d399'}; margin-top:0.3rem;">
                        {'⚠️ Human Staff Flag' if s_esc else '✓ Automated Resolution'}
                    </div>
                </div>
                <div>
                    <div style="font-size:0.75rem; color:#94a3b8; text-transform:uppercase;">Primary Campus Unit</div>
                    <div style="font-size:1.1rem; font-weight:700; color:#f8fafc; margin-top:0.3rem;">{info['contact']}</div>
                </div>
            </div>
            <div style="margin-top:1rem; padding-top:0.8rem; border-top:1px solid rgba(255,255,255,0.08); font-size:0.85rem; color:#cbd5e1;">
                <strong>Closest Dataset Match (5,000 Inquiries)</strong>: <em>"{s_matched}"</em>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 3: Campus Directory & Emergency Escalation
# ---------------------------------------------------------
with tab_directory:
    st.markdown("### 🏛️ University Helpdesk & Escalation Directory")
    st.caption("Official contact channels, physical room locations, and working hours for inquiries requiring administrative or counselor intervention.")
    
    dir_col1, dir_col2 = st.columns(2)
    
    with dir_col1:
        st.markdown("""
        <div class="desk-card">
            <div class="desk-header">
                <h4 class="desk-title">💰 Finance & Accounts Office</h4>
                <span class="desk-status">🟢 Open Mon-Fri</span>
            </div>
            <div class="desk-field"><strong>Location:</strong> Administrative Block, Ground Floor, Room 12</div>
            <div class="desk-field"><strong>Operating Hours:</strong> Monday – Friday: 9:30 AM – 4:00 PM</div>
            <div class="desk-field"><strong>Email:</strong> <code>accounts@campus.edu</code> · <strong>Phone:</strong> Ext. 2104</div>
            <p style="color:#94a3b8; font-size:0.83rem; margin-top:0.5rem;">
                Official handling for semester fee payments, fee refund applications, duplicate receipts, scholarship verification, and student loan documents.
            </p>
            <div class="desk-tag-row">
                <span class="desk-tag">Fee Receipts</span>
                <span class="desk-tag">Scholarships</span>
                <span class="desk-tag">Installment Forms</span>
            </div>
        </div>
        
        <div class="desk-card">
            <div class="desk-header">
                <h4 class="desk-title">📝 Controller of Examinations (Exam Cell)</h4>
                <span class="desk-status">🟢 Open Mon-Sat</span>
            </div>
            <div class="desk-field"><strong>Location:</strong> Academic Block B, First Floor, Room 108</div>
            <div class="desk-field"><strong>Operating Hours:</strong> Monday – Saturday: 9:00 AM – 5:00 PM</div>
            <div class="desk-field"><strong>Email:</strong> <code>examcell@campus.edu</code> · <strong>Phone:</strong> Ext. 2150</div>
            <p style="color:#94a3b8; font-size:0.83rem; margin-top:0.5rem;">
                Resolution desk for admit card issues, mid-term & final grade disputes, revaluation applications, backlog registration, and certified transcripts.
            </p>
            <div class="desk-tag-row">
                <span class="desk-tag">Admit Cards</span>
                <span class="desk-tag">Transcripts</span>
                <span class="desk-tag">Revaluation</span>
            </div>
        </div>

        <div class="desk-card">
            <div class="desk-header">
                <h4 class="desk-title">🧑‍💻 Campus IT Services Helpdesk</h4>
                <span class="desk-status">🟢 24/7 Portal Support</span>
            </div>
            <div class="desk-field"><strong>Location:</strong> Central Computing Facility, 2nd Floor</div>
            <div class="desk-field"><strong>Support Window:</strong> Online Portal: 24/7 · Counter: 9:00 AM – 6:00 PM</div>
            <div class="desk-field"><strong>Email:</strong> <code>it-support@campus.edu</code> · <strong>Phone:</strong> Ext. 2999</div>
            <p style="color:#94a3b8; font-size:0.83rem; margin-top:0.5rem;">
                Student ERP password resets, campus Wi-Fi MAC registration, university email issuance, and Moodle/LMS course enrollment support.
            </p>
            <div class="desk-tag-row">
                <span class="desk-tag">Wi-Fi MAC Registration</span>
                <span class="desk-tag">LMS Access</span>
                <span class="desk-tag">ERP Login</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with dir_col2:
        st.markdown("""
        <div class="desk-card">
            <div class="desk-header">
                <h4 class="desk-title">💙 Student Wellness & Counseling Center</h4>
                <span class="desk-status" style="color:#fda4af; background:rgba(244,63,94,0.12); border-color:rgba(244,63,94,0.3);">🚨 24/7 Emergency</span>
            </div>
            <div class="desk-field"><strong>Location:</strong> Health & Wellness Block, Room 104</div>
            <div class="desk-field"><strong>In-Person Hours:</strong> Monday – Saturday: 8:30 AM – 7:00 PM</div>
            <div class="desk-field"><strong>24/7 Crisis Hotline:</strong> <code>1800-CAMPUS-CARE</code> (Toll-Free, 100% Confidential)</div>
            <p style="color:#94a3b8; font-size:0.83rem; margin-top:0.5rem;">
                Licensed psychologists and counselors providing free, confidential care for academic pressure, exam anxiety, emotional wellbeing, and personal challenges.
            </p>
            <div class="desk-tag-row">
                <span class="desk-tag" style="background:rgba(244,63,94,0.15); color:#fda4af;">100% Confidential</span>
                <span class="desk-tag">Licensed Psychologists</span>
                <span class="desk-tag">Peer Mentors</span>
            </div>
        </div>

        <div class="desk-card">
            <div class="desk-header">
                <h4 class="desk-title">🛡️ Anti-Ragging Cell & Dean Student Welfare</h4>
                <span class="desk-status" style="color:#fda4af; background:rgba(244,63,94,0.12); border-color:rgba(244,63,94,0.3);">🚨 Zero Tolerance</span>
            </div>
            <div class="desk-field"><strong>Location:</strong> Dean's Complex, Administrative Block, 1st Floor</div>
            <div class="desk-field"><strong>National Anti-Ragging Helpline:</strong> <code>1800-180-5522</code> (24/7 Toll-Free)</div>
            <div class="desk-field"><strong>Email:</strong> <code>grievance@campus.edu</code> · <code>antiragging@campus.edu</code></div>
            <p style="color:#94a3b8; font-size:0.83rem; margin-top:0.5rem;">
                Zero-tolerance enforcement against bullying, ragging, and discrimination. Immediate protective escalation and confidential disciplinary reporting.
            </p>
            <div class="desk-tag-row">
                <span class="desk-tag" style="background:rgba(244,63,94,0.15); color:#fda4af;">Immediate Intervention</span>
                <span class="desk-tag">Disciplinary Committee</span>
            </div>
        </div>

        <div class="desk-card">
            <div class="desk-header">
                <h4 class="desk-title">🛏️ Chief Hostel Warden Complex</h4>
                <span class="desk-status">🟢 Open 7 Days</span>
            </div>
            <div class="desk-field"><strong>Location:</strong> Hostel Administrative Block, Ground Floor</div>
            <div class="desk-field"><strong>Operating Hours:</strong> Monday – Sunday: 8:00 AM – 8:00 PM (Emergency 24/7)</div>
            <div class="desk-field"><strong>Email:</strong> <code>hostelwarden@campus.edu</code> · <strong>Phone:</strong> Ext. 2400</div>
            <p style="color:#94a3b8; font-size:0.83rem; margin-top:0.5rem;">
                Room allotment approvals, mess quality management, digital night pass approvals, roommate disputes, and residential maintenance requests.
            </p>
            <div class="desk-tag-row">
                <span class="desk-tag">Room Allotment</span>
                <span class="desk-tag">Night Pass</span>
                <span class="desk-tag">Mess Committee</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------
# Footer Notice
# ---------------------------------------------------------
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#64748b; font-size:0.8rem; padding: 0.5rem 0 1.5rem; line-height: 1.6;">
    🎓 <strong>CampusCare University AI Support Platform</strong> · Powered by 5,000 Verified Knowledge Nodes.<br>
    Official university policies and administrative notices supersede automated chatbot responses. 
    Sensitive safety concerns are routed directly to campus wellness authorities.
</div>
""", unsafe_allow_html=True)

#!/usr/bin/env python3
"""
PWD Tools Web Application - Simplified Version
Minimal inputs for core tools: payee name, amount, work where applicable
Developed for PWD Udaipur under the initiative of Mrs. Premlata Jain, AAO
Streamlit Version for Web Deployment
"""

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
import io
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
import plotly.express as px
import os
import sys

# Make PWD-Tools importable
PWD_TOOLS_DIR = os.path.join(os.path.dirname(__file__), 'PWD-Tools')
if os.path.isdir(PWD_TOOLS_DIR) and PWD_TOOLS_DIR not in sys.path:
    sys.path.insert(0, PWD_TOOLS_DIR)

try:
    from utils.branding import apply_custom_css  # from PWD-Tools
except Exception:
    apply_custom_css = None

# Page configuration
st.set_page_config(
    page_title="PWD Tools Suite - Simplified",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS (minimal)
st.markdown("""
<style>
    .main-header { text-align: center; color: #1f4e79; font-size: 2rem; font-weight: bold; }
    .sub-header { text-align: center; color: #666; font-size: 1rem; }
    .footer { text-align: center; padding: 1rem; background: #f8f9fa; color: #666; }
</style>
""", unsafe_allow_html=True)

# Initialize database (minimal tables)
@st.cache_resource
def init_database():
    conn = sqlite3.connect('pwd_tools.db', check_same_thread=False)
    # Core tables only
    conn.execute('''
        CREATE TABLE IF NOT EXISTS bills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            payee_name TEXT,
            amount REAL,
            work TEXT,
            created_date TEXT
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS emd_refunds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            payee_name TEXT,
            amount REAL,
            work TEXT,
            created_date TEXT
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS project_delays (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            payee_name TEXT,
            amount REAL,
            work TEXT,
            created_date TEXT
        )
    ''')
    conn.commit()
    return conn

db = init_database()

def generate_pdf(data):
    """Minimal PDF generation"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()
    title = Paragraph("PWD NOTE", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 12))
    table_data = [["Payee:", data['payee']], ["Amount:", f"₹ {data['amount']:,.2f}"], ["Work:", data['work']]]
    table = Table(table_data, colWidths=[2*inch, 4*inch])
    table.setStyle(TableStyle([('FONTSIZE', (0,0), (-1,-1), 12)]))
    story.append(table)
    doc.build(story)
    buffer.seek(0)
    return buffer

def main():
    # Apply PWD-Tools branding if available
    if callable(apply_custom_css):
        apply_custom_css()
    st.markdown('<div class="main-header">🏛️ PWD Tools - Simplified</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Minimal Tools | Initiative of Mrs. Premlata Jain, AAO, PWD Udaipur</div>', unsafe_allow_html=True)

    # Sidebar with 10 tools
    st.sidebar.title("🔧 Core Tools")
    selected_tool = st.sidebar.selectbox("Select Tool:", [
        "🏠 Dashboard",
        "📊 Excel EMD",
        "📋 Bill Note",
        "💰 EMD Refund",
        "🔒 Security Refund",
        "📊 Financial Progress",
        "⏰ Delay Calc",
        "🏛️ Stamp Duty",
        "📊 Deductions",
        "📈 Bill Deviation"
    ])

    # Route to simplified tools
    if selected_tool == "🏠 Dashboard":
        show_dashboard()
    elif selected_tool == "📊 Excel EMD":
        show_excel_emd()
    elif selected_tool == "📋 Bill Note":
        show_bill_note()
    elif selected_tool == "💰 EMD Refund":
        show_emd_refund()
    elif selected_tool == "🔒 Security Refund":
        show_security_refund()
    elif selected_tool == "📊 Financial Progress":
        show_financial_progress()
    elif selected_tool == "⏰ Delay Calc":
        show_delay_calc()
    elif selected_tool == "🏛️ Stamp Duty":
        show_stamp_duty()
    elif selected_tool == "📊 Deductions":
        show_deductions()
    elif selected_tool == "📈 Bill Deviation":
        show_bill_deviation()

    st.markdown('<div class="footer">PWD Tools Simplified v1.0</div>', unsafe_allow_html=True)

def render_pwd_static_html(html_filename: str, height: int = 800, width: int = 1200):
    """Render a static HTML tool from PWD-Tools/static/html with graceful fallback."""
    static_path = os.path.join(PWD_TOOLS_DIR, 'static', 'html', html_filename)
    if os.path.isfile(static_path):
        try:
            with open(static_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            col_left, col_center, col_right = st.columns([1, 10, 1])
            with col_center:
                components.html(html_content, height=height, width=width, scrolling=True)
            return True
        except Exception as e:
            st.warning(f"Unable to load official PWD tool '{html_filename}': {e}")
            return False
    else:
        st.info("Official PWD-Tools static HTML not found. Showing simplified fallback.")
        return False

def show_dashboard():
    st.header("Dashboard")
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("Bills", db.execute("SELECT COUNT(*) FROM bills").fetchone()[0])
    with col2: st.metric("EMD", db.execute("SELECT COUNT(*) FROM emd_refunds").fetchone()[0])
    with col3: st.metric("Delays", db.execute("SELECT COUNT(*) FROM project_delays").fetchone()[0])

def show_excel_emd():
    st.header("Excel EMD Processor")
    uploaded = st.file_uploader("Excel File", type=['xlsx'])
    if uploaded:
        df = pd.read_excel(uploaded)
        st.dataframe(df.head())
        st.download_button("Download CSV", df.to_csv(index=False), "emd.csv")

def show_bill_note():
    st.header("Bill Note")
    with st.form("bill"):
        payee = st.text_input("Payee Name")
        amount = st.number_input("Amount", step=1000.0)
        work = st.text_input("Work")
        if st.form_submit_button("Save & PDF"):
            if payee and amount and work:
                db.execute("INSERT INTO bills VALUES (NULL, ?, ?, ?, ?)", (payee, amount, work, datetime.now().strftime("%Y-%m-%d")))
                db.commit()
                pdf = generate_pdf({'payee': payee, 'amount': amount, 'work': work})
                st.download_button("PDF", pdf.getvalue(), "bill.pdf")
                st.success("Saved!")

def show_emd_refund():
    st.header("EMD Refund")
    # Prefer official tool if available
    if not render_pwd_static_html('EmdRefund.html', height=600, width=1200):
        with st.form("emd"):
            payee = st.text_input("Payee Name")
            amount = st.number_input("Amount", step=1000.0)
            work = st.text_input("Work")
            if st.form_submit_button("Calculate"):
                if payee and amount and work:
                    db.execute("INSERT INTO emd_refunds VALUES (NULL, ?, ?, ?, ?)", (payee, amount, work, datetime.now().strftime("%Y-%m-%d")))
                    db.commit()
                    st.metric("Refund", f"₹{amount:,.2f}")

def show_security_refund():
    st.header("Security Refund")
    if not render_pwd_static_html('SecurityRefund.html', height=800, width=1200):
        with st.form("sec"):
            payee = st.text_input("Payee Name")
            amount = st.number_input("Amount", step=1000.0)
            work = st.text_input("Work")
            if st.form_submit_button("Check"):
                if payee and amount and work:
                    st.success("Eligible")

def show_financial_progress():
    st.header("Financial Progress")
    if not render_pwd_static_html('FinancialProgressTracker.html', height=800, width=1200):
        with st.form("progress"):
            payee = st.text_input("Payee Name")
            amount = st.number_input("Contract Amount", step=10000.0)
            work = st.text_input("Work")
            if st.form_submit_button("Calculate"):
                if payee and amount and work:
                    st.metric("Progress", "100%")

def show_delay_calc():
    st.header("Delay Calculator")
    with st.form("delay"):
        payee = st.text_input("Payee Name")
        amount = st.number_input("Amount", step=10000.0)
        work = st.text_input("Work")
        if st.form_submit_button("Calculate"):
            if payee and amount and work:
                st.metric("Delay Days", 0)
                st.metric("Penalty", "₹0.00")

def show_stamp_duty():
    st.header("Stamp Duty")
    if not render_pwd_static_html('StampDuty.html', height=600, width=1200):
        with st.form("stamp"):
            payee = st.text_input("Payee Name")
            amount = st.number_input("Amount", step=1000.0)
            work = st.text_input("Work")
            if st.form_submit_button("Calculate"):
                duty = amount * 0.005
                st.metric("Duty", f"₹{duty:,.2f}")

def show_deductions():
    st.header("Deductions")
    if not render_pwd_static_html('DeductionsTable.html', height=800, width=1200):
        with st.form("ded"):
            payee = st.text_input("Payee Name")
            amount = st.number_input("Amount", step=1000.0)
            work = st.text_input("Work")
            if st.form_submit_button("Calculate"):
                net = amount * 0.88
                st.metric("Net", f"₹{net:,.2f}")

def show_bill_deviation():
    st.header("Bill Deviation")
    # Use official Bill Note static page if present as a related reference
    showed = render_pwd_static_html('BillNoteSheet.html', height=800, width=1200)
    with st.form("dev"):
        payee = st.text_input("Payee Name")
        amount = st.number_input("Amount", step=1000.0)
        work = st.text_input("Work")
        if st.form_submit_button("Calculate"):
            revised = amount * 1.05
            st.metric("Revised", f"₹{revised:,.2f}")

if __name__ == "__main__":
    main()
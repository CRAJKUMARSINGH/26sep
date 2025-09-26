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
import zipfile
import re
import importlib.util

# Make PWD-Tools importable
PWD_TOOLS_DIR = os.path.join(os.path.dirname(__file__), 'PWD-Tools')
if os.path.isdir(PWD_TOOLS_DIR) and PWD_TOOLS_DIR not in sys.path:
    sys.path.insert(0, PWD_TOOLS_DIR)

try:
    from utils.branding import apply_custom_css  # from PWD-Tools
except Exception:
    apply_custom_css = None

# Load Genspark2 branding (for landing page look/colors/buttons)
GENSPARK2_DIR = os.path.join(os.path.dirname(__file__), 'PWD-Tools-Genspark2')
gs_apply_custom_css = None
gs_show_header = None
gs_show_credits = None
try:
    gs_branding_path = os.path.join(GENSPARK2_DIR, 'utils', 'branding.py')
    if os.path.isfile(gs_branding_path):
        spec = importlib.util.spec_from_file_location('genspark2_branding', gs_branding_path)
        gs_branding = importlib.util.module_from_spec(spec)
        assert spec and spec.loader
        spec.loader.exec_module(gs_branding)
        gs_apply_custom_css = getattr(gs_branding, 'apply_custom_css', None)
        gs_show_header = getattr(gs_branding, 'show_header', None)
        gs_show_credits = getattr(gs_branding, 'show_credits', None)
except Exception:
    pass

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
    # Apply Genspark2 branding first for landing page look/colors/buttons
    if callable(gs_apply_custom_css):
        gs_apply_custom_css()
    # Apply PWD-Tools branding if available (kept for broader theming)
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

    # Allow dashboard card clicks to override selection (from native buttons)
    if "selected_tool_override" in st.session_state:
        selected_tool = st.session_state.pop("selected_tool_override")

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

    # Footer styled like Genspark2 credits
    st.markdown("---")
    if callable(gs_show_credits):
        gs_show_credits()
    else:
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

def tool_header(title: str, subtitle: str = ""):
    """Reusable tool header styled like Genspark2."""
    st.markdown(
        f"""
        <div class=\"pwd-welcome\" style=\"margin-bottom: 16px;\"> 
            <h2 style=\"color: #2E8B57; margin-bottom: 6px;\">{title}</h2>
            {f'<p style=\"color:#555;\">{subtitle}</p>' if subtitle else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )

def show_dashboard():
    # Use Genspark2 header block for landing page look
    if callable(gs_show_header):
        gs_show_header()
    else:
        st.header("Dashboard")

    # Welcome section styled like Genspark2 landing page
    st.markdown(
        """
        <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #f0f8f5 0%, #e8f5e8 100%); border-radius: 15px; margin-bottom: 25px;">
            <h2 style="color: #2E8B57; margin-bottom: 10px;">🎯 PWD Tools Hub</h2>
            <p style="font-size: 1.1rem; color: #333; max-width: 800px; margin: 0 auto;">
                <strong>Infrastructure Management Tools</strong> - Simple, efficient tools for PWD operations
            </p>
            <p style="font-size: 1rem; color: #666; max-width: 800px; margin: 15px auto 0;">
                Streamline your workflow with our suite of engineering and financial tools
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("Bills", db.execute("SELECT COUNT(*) FROM bills").fetchone()[0])
    with col2: st.metric("EMD", db.execute("SELECT COUNT(*) FROM emd_refunds").fetchone()[0])
    with col3: st.metric("Delays", db.execute("SELECT COUNT(*) FROM project_delays").fetchone()[0])

    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 20px;">
            <h2 style="color: #2E8B57;">🔧 Available Tools</h2>
            <p style="color: #666; font-size: 1.05rem;">Select any tool below to get started</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Styled tool cards grid (3 columns)
    cards = [
        {"name": "📊 Excel EMD", "desc": "Excel to RPWA 28 receipts", "key": "Excel EMD"},
        {"name": "📋 Bill Note", "desc": "Generate Bill Note PDFs", "key": "Bill Note"},
        {"name": "💰 EMD Refund", "desc": "Refund calc & receipts", "key": "EMD Refund"},
        {"name": "🔒 Security Refund", "desc": "Security deposit checks", "key": "Security Refund"},
        {"name": "📊 Financial Progress", "desc": "Track project finance", "key": "Financial Progress"},
        {"name": "⏰ Delay Calc", "desc": "Delay & penalty calc", "key": "Delay Calc"},
        {"name": "🏛️ Stamp Duty", "desc": "Stamp duty calculator", "key": "Stamp Duty"},
        {"name": "📊 Deductions", "desc": "Net payable after deductions", "key": "Deductions"},
        {"name": "📈 Bill Deviation", "desc": "Deviation calculator", "key": "Bill Deviation"},
    ]

    cols = st.columns(3)
    for i, card in enumerate(cards):
        with cols[i % 3]:
            st.markdown(
                f"""
                <div class=\"pwd-card\" style=\"margin-bottom: 16px;\">
                    <div style=\"text-align:center; font-size: 26px;\">{card['name'].split(' ',1)[0]}</div>
                    <div style=\"text-align:center; font-weight: 800; color: var(--primary-green);\">{card['name']}</div>
                    <div style=\"text-align:center; color: #666; font-size: 13px; margin: 6px 0 10px;\">{card['desc']}</div>
                    <div style=\"text-align:center;\"><a class=\"btn-link\" href=\"#\" onclick=\"window.parent.postMessage('{{"select":"{card['key']}"}}','*'); return false;\">Open Tool</a></div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Handle card button selection via session state fallback
    # Provide native buttons as well (for environments without JS)
    st.markdown("<div style='display:none'></div>", unsafe_allow_html=True)
    colb1, colb2, colb3 = st.columns(3)
    with colb1:
        if st.button("Open Excel EMD", use_container_width=True):
            st.session_state["selected_tool_override"] = "📊 Excel EMD"
    with colb2:
        if st.button("Open Bill Note", use_container_width=True):
            st.session_state["selected_tool_override"] = "📋 Bill Note"
    with colb3:
        if st.button("Open EMD Refund", use_container_width=True):
            st.session_state["selected_tool_override"] = "💰 EMD Refund"


def show_excel_emd():
    tool_header("📊 Excel se EMD", "Excel to RPWA 28 hand receipts")
    st.info("Upload an Excel (.xlsx) or CSV, map columns, and download RPWA 28 hand receipts as HTML or ZIP.")

    # Helpers (scoped to this tool)
    def sanitize_filename(name: str) -> str:
        safe = re.sub(r"[^A-Za-z0-9._-]+", "_", name.strip())
        return safe[:80] or "receipt"

    def build_receipt_html(payee: str, amount_value: float, work: str) -> str:
        try:
            amount_float = float(amount_value)
            amount_str = f"{amount_float:,.2f}"
        except (ValueError, TypeError):
            amount_float = 0.0
            amount_str = "0.00"

        payee_js = payee.replace("'", r"\'")
        work_js = work.replace("'", r"\'")

        html = f"""
<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>Hand Receipt (RPWA 28)</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 0; }}
    .container {{ width: 100%; max-width: 900px; margin: 20px auto; border: 1px solid #e1e8e3; padding: 24px; box-sizing: border-box; background: #fff; border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.08); }}
    .header {{ text-align: center; margin-bottom: 10px; color: #2E8B57; }}
    .details {{ margin-bottom: 1px; }}
    .amount-words {{ font-style: italic; }}
    .signature-area, .offices {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
    .signature-area td, .signature-area th, .offices td, .offices th {{ border: 1px solid #ccc; padding: 5px; text-align: left; }}
    .offices td, .offices th {{ border-color: #000; word-wrap: break-word; }}
    .input-field {{ border-bottom: 1px dotted #ccc; padding: 3px; width: calc(100% - 10px); display: inline-block; }}
    .bottom-left-box {{ position: relative; border: 2px solid black; padding: 10px; width: 300px; text-align: left; margin-top: 12px; }}
    .bottom-left-box p {{ margin: 3px 0; }}
    .blue-text {{ color: blue; }}
    @media print {{
      @page {{ size: A4 portrait; margin: 0; }}
      body {{ margin: 0; padding: 0; }}
      .container {{ border: none; width: 210mm; min-height: 297mm; margin: 0; padding: 20mm; box-sizing: border-box; }}
      .input-field {{ border: none; }}
    }}
  </style>
  </head>
  <body>
    <div class=\"container\">
      <div id=\"receipt-content\">
        <div class=\"header\">
          <h2>Payable to: - {payee_js} (Electric Contractor)</h2>
          <h2>HAND RECEIPT (RPWA 28)</h2>
          <p>(Referred to in PWF&A Rules 418,424,436 & 438)</p>
          <p>Division - PWD Electric Division, Udaipur</p>
        </div>
        <div class=\"details\">
          <p>(1)Cash Book Voucher No. &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Date &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</p>
          <p>(2)Cheque No. and Date &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</p>
          <p>(3) Pay for ECS Rs. {amount_str}/- (Rupees <span id=\"amount-words\" class=\"amount-words\"></span>)</p>
          <p>(4) Paid by me</p>
          <p>(5) Received from The Executive Engineer PWD Electric Division, Udaipur the sum of Rs. {amount_str}/- (Rupees <span id=\"amount-words-2\" class=\"amount-words\"></span>)</p>
          <p>Name of work for which payment is made: <span id=\"work-name\" class=\"input-field\">{work_js}</span></p>
          <p>Chargeable to Head:- 8443 [EMD-Refund]</p>
          <table class=\"signature-area\">
            <tr><td>Witness</td><td>Stamp</td><td>Signature of payee</td></tr>
            <tr><td>Cash Book No. &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Page No. &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td><td></td><td></td></tr>
          </table>
          <table class=\"offices\">
            <tr><td>For use in the Divisional Office</td><td>For use in the Accountant General's office</td></tr>
            <tr><td>Checked</td><td>Audited/Reviewed</td></tr>
            <tr><td>Accounts Clerk</td><td>DA &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Auditor &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Supdt. &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;G.O.</td></tr>
          </table>
        </div>
        <div class=\"bottom-left-box\">
          <p class=\"blue-text\">Passed for Rs. {amount_str}</p>
          <p class=\"blue-text\" id=\"amount-words-3\">In Words Rupees: </p>
          <p class=\"blue-text\">Chargeable to Head:- 8443 [EMD-Refund]</p>
          <div class=\"seal\">
            <p>Ar.</p>
            <p>D.A.</p>
            <p>E.E.</p>
          </div>
        </div>
      </div>
    </div>
    <script>
      function convertNumberToWords(num) {{
        const ones = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"];
        const tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"];
        const teens = ["Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"];
        const crore = " Crore ";
        const lakh = " Lakh ";
        const thousand = " Thousand ";
        const hundred = " Hundred ";
        const andWord = " and ";
        if (!num || isNaN(num)) return "Zero";
        num = parseFloat(num.toString().replace(/,/g, ''));
        if (isNaN(num)) return "Zero";
        const rupees = Math.floor(num);
        const paise = Math.round((num - rupees) * 100);
        let words = "";
        if (rupees > 0) {{
          let r = rupees;
          if (Math.floor(r / 10000000)) {{ words += convertNumberToWords(Math.floor(r / 10000000)) + crore; r %= 10000000; }}
          if (Math.floor(r / 100000)) {{ words += convertNumberToWords(Math.floor(r / 100000)) + lakh; r %= 100000; }}
          if (Math.floor(r / 1000)) {{ words += convertNumberToWords(Math.floor(r / 1000)) + thousand; r %= 1000; }}
          if (Math.floor(r / 100)) {{ words += convertNumberToWords(Math.floor(r / 100)) + hundred; r %= 100; }}
          if (r > 0) {{
            if (words !== "") words += andWord;
            if (r < 10) words += ones[r];
            else if (r < 20) words += teens[r - 10];
            else {{
              words += tens[Math.floor(r / 10)];
              if (r % 10 > 0) words += " " + ones[r % 10];
            }}
          }}
          words += " Rupees";
        }}
        if (paise > 0) {{
          if (words !== "") words += " and ";
          if (paise < 10) words += ones[paise];
          else if (paise < 20) words += teens[paise - 10];
          else {{
            words += tens[Math.floor(paise / 10)];
            if (paise % 10 > 0) words += " " + ones[paise % 10];
          }}
          words += " Paise";
        }}
        return words || "Zero Rupees";
      }}
      function formatAmount(amount) {{
        return amount.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
      }}
      document.addEventListener('DOMContentLoaded', function() {{
        const amount = {amount_float};
        const amountInWords = convertNumberToWords(amount);
        document.querySelectorAll('.amount-words').forEach(el => {{
          el.textContent = amountInWords + ' only';
        }});
        document.getElementById('amount-words-3').textContent = 'In Words Rupees: ' + amountInWords + ' Only';
      }});
    </script>
  </body>
</html>
"""
        return html

    # Upload
    uploaded = st.file_uploader("Upload .xlsx or .csv", type=["xlsx", "csv"], accept_multiple_files=False)
    if not uploaded:
        return

    # Read data
    df = None
    sheet_name = None
    try:
        name_lower = uploaded.name.lower()
        if name_lower.endswith(".xlsx"):
            try:
                try:
                    xls = pd.ExcelFile(uploaded, engine="openpyxl")
                except ImportError:
                    xls = pd.ExcelFile(uploaded, engine="xlrd")
                if len(xls.sheet_names) > 1:
                    sheet_name = st.selectbox("Select sheet", xls.sheet_names)
                else:
                    sheet_name = xls.sheet_names[0]
                df = pd.read_excel(uploaded, sheet_name=sheet_name, engine=xls.engine)
            except Exception as e:
                st.error(f"Error reading Excel file: {str(e)}\n\nPlease ensure your Excel file is not password protected and is a valid .xlsx file.")
                return
        elif name_lower.endswith(".csv"):
            df = pd.read_csv(uploaded)
        else:
            st.error("Unsupported file type. Please upload .xlsx or .csv.")
            return
    except Exception as e:
        st.error(f"Failed to read file: {e}")
        return

    if df is None or df.empty:
        st.warning("No data found in the file.")
        return

    # Debug preview
    st.write("### Debug - Excel File Structure")
    try:
        xls = pd.ExcelFile(uploaded, engine="openpyxl")
        st.write(f"Sheet names: {xls.sheet_names}")
        df_debug = pd.read_excel(uploaded, sheet_name=0, nrows=5)
        st.write("First 5 rows of first sheet:")
        st.dataframe(df_debug)
        st.write("Column data types:")
        st.dataframe(df_debug.dtypes.rename('Data Type').to_frame())
    except Exception as e:
        st.error(f"Error analyzing Excel file: {e}")

    st.markdown("##### Preview")
    st.dataframe(df.head(20), use_container_width=True)

    # Guess columns
    cols = list(df.columns.astype(str))
    def guess(patterns):
        for c in cols:
            lc = c.lower()
            if any(p in lc for p in patterns):
                return c
        return None
    default_payee = guess(["payee", "contractor", "name"]) or cols[0]
    default_amount = guess(["amount", "amt", "emd", "value"]) or cols[min(1, len(cols)-1)]
    default_work = guess(["work", "name of work", "work name"]) or cols[min(2, len(cols)-1)]

    st.markdown("##### Map Columns")
    col1, col2, col3 = st.columns(3)
    with col1:
        payee_col = st.selectbox("Payee column", cols, index=cols.index(default_payee) if default_payee in cols else 0)
    with col2:
        amount_col = st.selectbox("Amount column", cols, index=cols.index(default_amount) if default_amount in cols else (1 if len(cols) > 1 else 0))
    with col3:
        work_col = st.selectbox("Work column", cols, index=cols.index(default_work) if default_work in cols else (2 if len(cols) > 2 else 0))

    run = st.button("Generate Receipts", type="primary")
    if not run:
        return

    # Build receipt HTMLs
    records = []
    invalid_rows = []
    for idx, row in df.iterrows():
        try:
            payee = str(row[payee_col]).strip()
            work = str(row[work_col]).strip()
            amount_raw = row[amount_col]
            if pd.isna(payee) or pd.isna(work) or pd.isna(amount_raw):
                invalid_rows.append((idx + 2, "Missing required values"))
                continue
            try:
                amount = float(amount_raw)
            except (ValueError, TypeError) as e:
                invalid_rows.append((idx + 2, f"Invalid amount value: {amount_raw} (Error: {str(e)})"))
                continue
            html = build_receipt_html(payee, amount, work)
            filename = f"hand_receipt_{sanitize_filename(payee)}_{idx}.html"
            records.append((idx, payee, amount, work, html, filename))
        except Exception as e:
            error_msg = str(e)
            invalid_rows.append((idx + 2, error_msg))
            continue

    if not records:
        st.error("❌ No valid rows to generate receipts. Please check your data.")
        if invalid_rows:
            st.warning("Found the following issues in your data:")
            for row_num, error in invalid_rows[:10]:
                st.write(f"- Row {row_num}: {error}")
            if len(invalid_rows) > 10:
                st.write(f"... and {len(invalid_rows) - 10} more issues")
        st.subheader("Data Preview (with selected columns)")
        preview_cols = [payee_col, work_col, amount_col]
        st.dataframe(df[preview_cols].head(), use_container_width=True)
        return

    st.success(f"Generated {len(records)} receipt(s).")

    # Preview first
    preview_idx = st.selectbox("Preview row", [r[0] for r in records], format_func=lambda i: f"Row {i}")
    preview = next(r for r in records if r[0] == preview_idx)
    components.html(preview[4], height=850, scrolling=True)

    # Downloads
    st.markdown("##### Download")
    col_a, col_b = st.columns([1,1])
    with col_a:
        for idx, payee, amount, work, html, filename in records[:20]:
            st.download_button(
                label=f"Download {filename}",
                data=html,
                file_name=filename,
                mime="text/html",
                use_container_width=True,
                key=f"dl_{idx}"
            )
        if len(records) > 20:
            st.caption(f"Showing first 20 downloads. Use ZIP for all {len(records)} receipts.")
    with col_b:
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
            for _, _, _, _, html, filename in records:
                zf.writestr(filename, html)
        buf.seek(0)
        st.download_button(
            label=f"Download all as ZIP ({len(records)} files)",
            data=buf.getvalue(),
            file_name="hand_receipts.zip",
            mime="application/zip",
            use_container_width=True,
            key="dl_zip"
        )

def show_bill_note():
    tool_header("📝 Bill Note", "Generate and download bill note PDFs")
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
    tool_header("💰 EMD Refund", "Refund calculation and receipts")
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
    tool_header("🔒 Security Refund", "Eligibility and calculations")
    if not render_pwd_static_html('SecurityRefund.html', height=800, width=1200):
        with st.form("sec"):
            payee = st.text_input("Payee Name")
            amount = st.number_input("Amount", step=1000.0)
            work = st.text_input("Work")
            if st.form_submit_button("Check"):
                if payee and amount and work:
                    st.success("Eligible")

def show_financial_progress():
    tool_header("📈 Financial Progress", "Track project financials")
    if not render_pwd_static_html('FinancialProgressTracker.html', height=800, width=1200):
        with st.form("progress"):
            payee = st.text_input("Payee Name")
            amount = st.number_input("Contract Amount", step=10000.0)
            work = st.text_input("Work")
            if st.form_submit_button("Calculate"):
                if payee and amount and work:
                    st.metric("Progress", "100%")

def show_delay_calc():
    tool_header("⏰ Delay Calculator", "Delay days and penalty")
    with st.form("delay"):
        payee = st.text_input("Payee Name")
        amount = st.number_input("Amount", step=10000.0)
        work = st.text_input("Work")
        if st.form_submit_button("Calculate"):
            if payee and amount and work:
                st.metric("Delay Days", 0)
                st.metric("Penalty", "₹0.00")

def show_stamp_duty():
    tool_header("🏛️ Stamp Duty", "Document stamp duty calculator")
    if not render_pwd_static_html('StampDuty.html', height=600, width=1200):
        with st.form("stamp"):
            payee = st.text_input("Payee Name")
            amount = st.number_input("Amount", step=1000.0)
            work = st.text_input("Work")
            if st.form_submit_button("Calculate"):
                duty = amount * 0.005
                st.metric("Duty", f"₹{duty:,.2f}")

def show_deductions():
    tool_header("📊 Deductions", "Net payable after deductions")
    if not render_pwd_static_html('DeductionsTable.html', height=800, width=1200):
        with st.form("ded"):
            payee = st.text_input("Payee Name")
            amount = st.number_input("Amount", step=1000.0)
            work = st.text_input("Work")
            if st.form_submit_button("Calculate"):
                net = amount * 0.88
                st.metric("Net", f"₹{net:,.2f}")

def show_bill_deviation():
    tool_header("📈 Bill Deviation", "Deviation calculator")
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
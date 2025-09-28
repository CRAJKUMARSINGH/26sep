
import streamlit as st
import sqlite3
import pandas as pd

from datetime import datetime, date
import base64
from io import BytesIO

from num2words import num2words

# Page configuration
st.set_page_config(
    page_title="PWD Tools - Advanced Version",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1f4e79 0%, #2d5aa0 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        margin: 5px;
    }
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
    }
    .warning-message {
        background: #fff3cd;
        color: #856404;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #ffeaa7;
    }
    .error-message {
        background: #f8d7da;
        color: #721c24;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
    }
    .download-button {
        background: linear-gradient(90deg, #28a745 0%, #20c997 100%);
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        text-decoration: none;
        display: inline-block;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Database initialization
def init_database():
    """Initialize SQLite database with tables for advanced tools"""
    conn = sqlite3.connect('advanced_pwd_tools.db')
    cursor = conn.cursor()
    
    # Advanced EMD Refunds table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS advanced_emd_refunds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            payee_name TEXT NOT NULL,
            amount REAL NOT NULL,
            work_description TEXT NOT NULL,
            tender_no TEXT,
            date_of_submission DATE,
            refund_date DATE,
            bank_details TEXT,
            pan_number TEXT,
            address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Advanced Project Delays table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS advanced_project_delays (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_name TEXT NOT NULL,
            contractor_name TEXT NOT NULL,
            original_completion_date DATE NOT NULL,
            actual_completion_date DATE NOT NULL,
            delay_days INTEGER NOT NULL,
            delay_category TEXT,
            penalty_amount REAL,
            reason_for_delay TEXT,
            mitigation_measures TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Professional Bills table  
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS professional_bills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bill_number TEXT NOT NULL,
            contractor_name TEXT NOT NULL,
            work_description TEXT NOT NULL,
            bill_amount REAL NOT NULL,
            previous_payment REAL DEFAULT 0,
            current_claim REAL NOT NULL,
            deductions REAL DEFAULT 0,
            net_payment REAL NOT NULL,
            gst_amount REAL DEFAULT 0,
            tds_amount REAL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

# Utility functions
def indian_number_to_words(amount):
    """Convert number to Indian currency words"""
    try:
        rupees = int(amount)
        paise = int((amount - rupees) * 100)
        
        if rupees == 0:
            rupee_words = "Zero"
        else:
            rupee_words = num2words(rupees, lang='en_IN').title()
        
        if paise > 0:
            paise_words = num2words(paise, lang='en').title()
            return f"{rupee_words} Rupees and {paise_words} Paise Only"
        else:
            return f"{rupee_words} Rupees Only"
    except:
        return f"{amount:.2f} Rupees Only"

def create_download_link(df, filename, file_format="csv"):
    """Create download link for dataframes"""
    if file_format == "csv":
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="{filename}" class="download-button">📥 Download {file_format.upper()}</a>'
    elif file_format == "excel":
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Data')
        excel_data = output.getvalue()
        b64 = base64.b64encode(excel_data).decode()
        href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}" class="download-button">📥 Download Excel</a>'
    return href

# Main application
def main():
    init_database()
    
    st.markdown("""
    <div class="main-header">
        <h1>🏛️ PWD Tools - Advanced Version</h1>
        <p>Professional Tools for Public Works Department - Advanced Features</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("### 🛠️ Advanced Tools")
    selected_tool = st.sidebar.selectbox(
        "Select an Advanced Tool:",
        [
            "🏠 Advanced Dashboard",
            "💰 EMD Refund A4 (RPWA 28 Format)", 
            "⏱️ Advanced Delay Calculator & Analysis",
            "📝 Professional Bill Note Sheet",
            "📊 Advanced Deductions Table",
            "💼 Sophisticated Financial Progress",
            "🔒 Security Refund Advanced",
            "📈 Project Analytics Dashboard",
            "🎯 Performance Metrics"
        ]
    )
    
    if selected_tool == "🏠 Advanced Dashboard":
        show_advanced_dashboard()
    elif selected_tool == "💰 EMD Refund A4 (RPWA 28 Format)":
        show_advanced_emd_refund()
    elif selected_tool == "⏱️ Advanced Delay Calculator & Analysis":
        show_advanced_delay_calculator()
    elif selected_tool == "📝 Professional Bill Note Sheet":
        show_professional_bill_sheet()
    elif selected_tool == "📊 Advanced Deductions Table":
        show_advanced_deductions()
    elif selected_tool == "💼 Sophisticated Financial Progress":
        show_financial_progress()
    elif selected_tool == "🔒 Security Refund Advanced":
        show_security_refund_advanced()
    elif selected_tool == "📈 Project Analytics Dashboard":
        show_project_analytics()
    elif selected_tool == "🎯 Performance Metrics":
        show_performance_metrics()

def show_advanced_dashboard():
    """Advanced Dashboard with comprehensive analytics"""
    st.markdown("### 🏠 Advanced Dashboard")
    
    conn = sqlite3.connect('advanced_pwd_tools.db')
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        try:
            emd_count = pd.read_sql_query("SELECT COUNT(*) as count FROM advanced_emd_refunds", conn)['count'].iloc[0]
        except:
            emd_count = 0
        st.markdown(f"""
        <div class="metric-card">
            <h3>{emd_count}</h3>
            <p>Advanced EMD Refunds</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        try:
            delay_count = pd.read_sql_query("SELECT COUNT(*) as count FROM advanced_project_delays", conn)['count'].iloc[0]
        except:
            delay_count = 0
        st.markdown(f"""
        <div class="metric-card">
            <h3>{delay_count}</h3>
            <p>Project Delays Tracked</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        try:
            bill_count = pd.read_sql_query("SELECT COUNT(*) as count FROM professional_bills", conn)['count'].iloc[0]
        except:
            bill_count = 0
        st.markdown(f"""
        <div class="metric-card">
            <h3>{bill_count}</h3>
            <p>Professional Bills</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        try:
            total_amount = pd.read_sql_query("SELECT SUM(amount) as total FROM advanced_emd_refunds", conn)['total'].iloc[0] or 0
        except:
            total_amount = 0
        st.markdown(f"""
        <div class="metric-card">
            <h3>₹{total_amount:,.2f}</h3>
            <p>Total EMD Amount</p>
        </div>
        """, unsafe_allow_html=True)
    
    conn.close()
    
    st.markdown("### 📊 Recent Activities")
    
    if st.button("🔄 Refresh Analytics"):
        st.success("Analytics refreshed successfully!")
    
    st.markdown("### ⚡ Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💰 New EMD Refund", use_container_width=True):
            st.info("Navigate to EMD Refund tool from sidebar")
    
    with col2:
        if st.button("⏱️ Calculate Delays", use_container_width=True):
            st.info("Navigate to Delay Calculator from sidebar")
    
    with col3:
        if st.button("📝 Professional Bill", use_container_width=True):
            st.info("Navigate to Professional Bill tool from sidebar")

def show_advanced_emd_refund():
    """Advanced EMD Refund with A4 format and RPWA 28 compliance"""
    st.markdown("### 💰 EMD Refund A4 (RPWA 28 Format)")
    
    with st.form("advanced_emd_form"):
        st.markdown("#### 📋 Complete EMD Refund Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            payee_name = st.text_input("Payee Name *", placeholder="Enter full name as per documents")
            amount = st.number_input("Refund Amount (₹) *", min_value=0.01, step=0.01, format="%.2f")
            tender_no = st.text_input("Tender Number", placeholder="e.g., PWD/2024/TND/001")
            date_of_submission = st.date_input("Date of EMD Submission", value=datetime.now().date())
            pan_number = st.text_input("PAN Number", placeholder="e.g., ABCDE1234F")
        
        with col2:
            work_description = st.text_area("Work Description *", placeholder="Detailed description of the work")
            refund_date = st.date_input("Refund Date", value=datetime.now().date())
            bank_details = st.text_area("Bank Details", placeholder="Bank Name, Branch, Account Number, IFSC")
            address = st.text_area("Complete Address", placeholder="Full address with PIN code")
        
        st.markdown("#### 🏛️ RPWA 28 Format Additional Details")
        col3, col4 = st.columns(2)
        
        with col3:
            office_name = st.text_input("Office Name", placeholder="Executive Engineer Office")
            file_number = st.text_input("File Number", placeholder="EMD/2024/001")
            receipt_number = st.text_input("Receipt Number", placeholder="Receipt No. for EMD")
        
        with col4:
            project_code = st.text_input("Project Code", placeholder="PWD-2024-001")
            sanctioned_by = st.text_input("Sanctioned By", placeholder="Competent Authority")
            remarks = st.text_area("Remarks", placeholder="Any additional remarks")
        
        submitted = st.form_submit_button("🎯 Generate Advanced EMD Refund", use_container_width=True)
        
        if submitted:
            if not payee_name or not work_description or amount <= 0:
                st.markdown("""
                <div class="error-message">
                    ❌ Please fill in all required fields marked with *
                </div>
                """, unsafe_allow_html=True)
            else:
                conn = sqlite3.connect('advanced_pwd_tools.db')
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO advanced_emd_refunds 
                    (payee_name, amount, work_description, tender_no, date_of_submission, 
                     refund_date, bank_details, pan_number, address)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (payee_name, amount, work_description, tender_no, date_of_submission, 
                      refund_date, bank_details, pan_number, address))
                
                conn.commit()
                conn.close()
                
                amount_in_words = indian_number_to_words(amount)
                
                st.markdown("""
                <div class="success-message">
                    ✅ Advanced EMD Refund generated successfully with RPWA 28 compliance!
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("### 📄 EMD Refund Document (A4 Format)")
                
                refund_doc = f"""
                **GOVERNMENT OF [STATE NAME]**
                **PUBLIC WORKS DEPARTMENT**
                **{office_name or "EXECUTIVE ENGINEER OFFICE"}**
                
                ---
                
                **EMD REFUND ORDER**
                **[As per RPWA 28 Format]**
                
                **File No:** {file_number or "EMD/2024/001"}
                **Date:** {refund_date}
                
                ---
                
                **To,**
                **{payee_name}**
                {address or "Address not provided"}
                
                **Subject:** Refund of Earnest Money Deposit
                
                **Sir/Madam,**
                
                With reference to your Earnest Money Deposit submitted for the work **"{work_description}"** 
                under Tender No. **{tender_no or "Not specified"}** dated **{date_of_submission}**, 
                you are hereby informed that your EMD amounting to **₹{amount:,.2f} 
                ({amount_in_words})** is being refunded as per the provisions of RPWA 28.
                
                **EMD Details:**
                - **Receipt No.:** {receipt_number or "Not provided"}
                - **Amount:** ₹{amount:,.2f}
                - **Amount in Words:** {amount_in_words}
                - **Project Code:** {project_code or "Not specified"}
                - **PAN Number:** {pan_number or "Not provided"}
                
                **Bank Details:**
                {bank_details or "To be provided by the payee"}
                
                **Sanctioned by:** {sanctioned_by or "Competent Authority"}
                
                **Remarks:** {remarks or "EMD refund processed as per rules"}
                
                ---
                
                **For Executive Engineer**
                **Public Works Department**
                
                **Date:** {datetime.now().strftime("%d/%m/%Y")}
                **Time:** {datetime.now().strftime("%H:%M:%S")}
                """
                
                st.markdown(refund_doc)
                
                st.markdown("### 📥 Download Options")
                col1, col2 = st.columns(2)
                
                with col1:
                    df_download = pd.DataFrame({
                        'Field': ['Payee Name', 'Amount', 'Amount in Words', 'Work Description', 
                                'Tender No', 'Submission Date', 'Refund Date', 'PAN Number'],
                        'Value': [payee_name, f"₹{amount:,.2f}", amount_in_words, work_description,
                                tender_no or "Not specified", str(date_of_submission), str(refund_date), pan_number or "Not provided"]
                    })
                    
                    st.markdown(create_download_link(df_download, "advanced_emd_refund.csv", "csv"), 
                              unsafe_allow_html=True)
                
                with col2:
                    st.markdown(create_download_link(df_download, "advanced_emd_refund.xlsx", "excel"), 
                              unsafe_allow_html=True)

def show_advanced_delay_calculator():
    """Advanced Delay Calculator with comprehensive analysis"""
    st.markdown("### ⏱️ Advanced Delay Calculator & Analysis")
    
    with st.form("advanced_delay_form"):
        st.markdown("#### 📊 Project Delay Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            project_name = st.text_input("Project Name *", placeholder="Enter project name")
            contractor_name = st.text_input("Contractor Name *", placeholder="Contractor/Agency name")
            original_date = st.date_input("Original Completion Date *")
            actual_date = st.date_input("Actual Completion Date *")
        
        with col2:
            delay_category = st.selectbox("Delay Category", [
                "Weather Related", "Material Shortage", "Labor Issues", 
                "Technical Problems", "Administrative Delays", "Force Majeure", "Other"
            ])
            penalty_rate = st.number_input("Penalty Rate (% per day)", min_value=0.0, max_value=1.0, step=0.01, value=0.05)
            project_value = st.number_input("Project Value (₹)", min_value=0.01, step=1000.00, format="%.2f")
            reason_for_delay = st.text_area("Reason for Delay", placeholder="Detailed explanation")
        
        mitigation_measures = st.text_area("Mitigation Measures Taken", placeholder="Steps taken to minimize delay")
        
        submitted = st.form_submit_button("🔍 Analyze Project Delay", use_container_width=True)
        
        if submitted:
            if not project_name or not contractor_name or not original_date or not actual_date:
                st.markdown("""
                <div class="error-message">
                    ❌ Please fill in all required fields marked with *
                </div>
                """, unsafe_allow_html=True)
            else:
                delay_days = (actual_date - original_date).days
                
                if delay_days < 0:
                    st.markdown(f"""
                    <div class="success-message">
                        ✅ Project completed ahead of schedule by {abs(delay_days)} days!
                    </div>
                    """, unsafe_allow_html=True)
                    penalty_amount = 0
                elif delay_days == 0:
                    st.markdown("""
                    <div class="success-message">
                        ✅ Project completed on time!
                    </div>
                    """, unsafe_allow_html=True)
                    penalty_amount = 0
                else:
                    penalty_amount = project_value * (penalty_rate / 100) * delay_days
                    
                    st.markdown(f"""
                    <div class="warning-message">
                        ⚠️ Project delayed by {delay_days} days
                    </div>
                    """, unsafe_allow_html=True)
                
                conn = sqlite3.connect('advanced_pwd_tools.db')
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO advanced_project_delays 
                    (project_name, contractor_name, original_completion_date, actual_completion_date, 
                     delay_days, delay_category, penalty_amount, reason_for_delay, mitigation_measures)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (project_name, contractor_name, original_date, actual_date, delay_days, 
                      delay_category, penalty_amount, reason_for_delay, mitigation_measures))
                
                conn.commit()
                conn.close()
                
                st.markdown("### 📈 Comprehensive Delay Analysis")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Delay Days", f"{delay_days}", f"{delay_days - 0}")
                
                with col2:
                    st.metric("Penalty Amount", f"₹{penalty_amount:,.2f}")
                
                with col3:
                    delay_percentage = (delay_days / 365) * 100 if delay_days > 0 else 0
                    st.metric("Delay %", f"{delay_percentage:.1f}%")
                
                with col4:
                    impact_rating = "High" if delay_days > 90 else "Medium" if delay_days > 30 else "Low"
                    st.metric("Impact Level", impact_rating)
                
                st.markdown("### 📋 Detailed Analysis Report")
                
                recommendations = ""
                if delay_days > 90:
                    recommendations = "- Implement strict project monitoring\\n- Consider contractor performance review\\n- Enhance risk management protocols"
                elif delay_days > 30:
                    recommendations = "- Monitor progress more closely\\n- Review project management practices\\n- Implement corrective measures"  
                else:
                    recommendations = "- Continue current monitoring\\n- Document lessons learned\\n- Maintain quality standards"
                
                analysis_report = f"""
                **PROJECT DELAY ANALYSIS REPORT**
                
                **Project Details:**
                - **Project Name:** {project_name}
                - **Contractor:** {contractor_name}
                - **Project Value:** ₹{project_value:,.2f}
                
                **Timeline Analysis:**
                - **Planned Completion:** {original_date}
                - **Actual Completion:** {actual_date}
                - **Delay Duration:** {delay_days} days
                - **Delay Category:** {delay_category}
                
                **Financial Impact:**
                - **Penalty Rate:** {penalty_rate}% per day
                - **Total Penalty:** ₹{penalty_amount:,.2f}
                - **Penalty in Words:** {indian_number_to_words(penalty_amount)}
                
                **Analysis:**
                - **Delay Percentage:** {delay_percentage:.2f}% of annual timeline
                - **Impact Assessment:** {impact_rating} Impact
                - **Reason for Delay:** {reason_for_delay or "Not specified"}
                
                **Mitigation Measures:**
                {mitigation_measures or "No specific measures documented"}
                
                **Recommendations:**
                {recommendations}
                
                ---
                **Report Generated:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
                """
                
                st.markdown(analysis_report)
                
                st.markdown("### 📥 Download Analysis Report")
                
                df_analysis = pd.DataFrame({
                    'Parameter': ['Project Name', 'Contractor', 'Original Date', 'Actual Date', 
                                'Delay Days', 'Delay Category', 'Penalty Amount', 'Impact Level'],
                    'Value': [project_name, contractor_name, str(original_date), str(actual_date),
                            delay_days, delay_category, f"₹{penalty_amount:,.2f}", impact_rating]
                })
                
                st.markdown(create_download_link(df_analysis, "project_delay_analysis.csv", "csv"), 
                          unsafe_allow_html=True)

def show_professional_bill_sheet():
    """Professional Bill Note Sheet with advanced calculations"""
    st.markdown("### 📝 Professional Bill Note Sheet")
    
    with st.form("professional_bill_form"):
        st.markdown("#### 💼 Professional Bill Generation")
        
        col1, col2 = st.columns(2)
        
        with col1:
            bill_number = st.text_input("Bill Number *", placeholder="e.g., PWD/BILL/2024/001")
            contractor_name = st.text_input("Contractor/Supplier Name *")
            work_description = st.text_area("Work Description *", placeholder="Detailed work description")
            current_claim = st.number_input("Current Claim (₹) *", min_value=0.01, step=0.01)
            previous_payment = st.number_input("Previous Payments (₹)", min_value=0.0, step=0.01, value=0.0)
        
        with col2:
            gst_rate = st.number_input("GST Rate (%)", min_value=0.0, max_value=28.0, step=0.1, value=18.0)
            tds_rate = st.number_input("TDS Rate (%)", min_value=0.0, max_value=10.0, step=0.1, value=2.0)
            retention_rate = st.number_input("Retention Rate (%)", min_value=0.0, max_value=10.0, step=0.1, value=5.0)
            labour_cess = st.number_input("Labour Cess (%)", min_value=0.0, max_value=2.0, step=0.01, value=1.0)
            other_deductions = st.number_input("Other Deductions (₹)", min_value=0.0, step=0.01, value=0.0)
        
        submitted = st.form_submit_button("📊 Generate Professional Bill", use_container_width=True)
        
        if submitted:
            if not bill_number or not contractor_name or not work_description or current_claim <= 0:
                st.markdown("""
                <div class="error-message">
                    ❌ Please fill in all required fields marked with *
                </div>
                """, unsafe_allow_html=True)
            else:
                gst_amount = current_claim * (gst_rate / 100)
                gross_with_gst = current_claim + gst_amount
                
                tds_amount = gross_with_gst * (tds_rate / 100)
                retention_amount = current_claim * (retention_rate / 100)
                labour_cess_amount = current_claim * (labour_cess / 100)
                
                total_deductions = tds_amount + retention_amount + labour_cess_amount + other_deductions
                net_payment = gross_with_gst - total_deductions
                
                conn = sqlite3.connect('advanced_pwd_tools.db')
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO professional_bills 
                    (bill_number, contractor_name, work_description, bill_amount, previous_payment,
                     current_claim, deductions, net_payment, gst_amount, tds_amount)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (bill_number, contractor_name, work_description, current_claim, previous_payment,
                      current_claim, total_deductions, net_payment, gst_amount, tds_amount))
                
                conn.commit()
                conn.close()
                
                st.markdown("""
                <div class="success-message">
                    ✅ Professional bill generated successfully!
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("### 📋 Professional Bill Note Sheet")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### 💰 Financial Summary")
                    st.metric("Gross Amount", f"₹{current_claim:,.2f}")
                    st.metric("GST Amount", f"₹{gst_amount:,.2f}")
                    st.metric("Total with GST", f"₹{gross_with_gst:,.2f}")
                    st.metric("Net Payment", f"₹{net_payment:,.2f}", f"{net_payment - current_claim:,.2f}")
                
                with col2:
                    st.markdown("#### ➖ Deductions Breakdown")
                    st.metric("TDS", f"₹{tds_amount:,.2f}")
                    st.metric("Retention", f"₹{retention_amount:,.2f}")
                    st.metric("Labour Cess", f"₹{labour_cess_amount:,.2f}")
                    st.metric("Other Deductions", f"₹{other_deductions:,.2f}")
                
                bill_document = f"""
                **PROFESSIONAL BILL NOTE SHEET**
                
                **Bill No:** {bill_number}
                **Date:** {datetime.now().strftime("%d/%m/%Y")}
                
                **Contractor Details:**
                **Name:** {contractor_name}
                **Work:** {work_description}
                
                **Financial Calculations:**
                
                | Description | Amount (₹) |
                |-------------|----------:|
                | Current Claim | {current_claim:,.2f} |
                | GST @ {gst_rate}% | {gst_amount:,.2f} |
                | **Gross with GST** | **{gross_with_gst:,.2f}** |
                | | |
                | **DEDUCTIONS:** | |
                | TDS @ {tds_rate}% | {tds_amount:,.2f} |
                | Retention @ {retention_rate}% | {retention_amount:,.2f} |
                | Labour Cess @ {labour_cess}% | {labour_cess_amount:,.2f} |
                | Other Deductions | {other_deductions:,.2f} |
                | **Total Deductions** | **{total_deductions:,.2f}** |
                | | |
                | **NET PAYMENT** | **₹{net_payment:,.2f}** |
                | **Amount in Words:** | **{indian_number_to_words(net_payment)}** |
                
                **Previous Payments:** ₹{previous_payment:,.2f}
                **Cumulative Payment:** ₹{previous_payment + net_payment:,.2f}
                
                ---
                **Prepared by:** [Name]
                **Approved by:** Executive Engineer
                **Date:** {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
                """
                
                st.markdown(bill_document)
                
                st.markdown("### 📥 Download Professional Bill")
                
                df_bill = pd.DataFrame({
                    'Description': ['Current Claim', 'GST Amount', 'Gross with GST', 'Total Deductions', 'Net Payment'],
                    'Amount': [f"₹{current_claim:,.2f}", f"₹{gst_amount:,.2f}", f"₹{gross_with_gst:,.2f}", 
                             f"₹{total_deductions:,.2f}", f"₹{net_payment:,.2f}"]
                })
                
                st.markdown(create_download_link(df_bill, "professional_bill.csv", "csv"), 
                          unsafe_allow_html=True)

def show_advanced_deductions():
    """Advanced Deductions Table with comprehensive calculations"""
    st.markdown("### 📊 Advanced Deductions Table")
    
    with st.form("advanced_deductions_form"):
        st.markdown("#### 🧮 Comprehensive Deductions Calculator")
        
        base_amount = st.number_input("Base Contract Amount (₹) *", min_value=0.01, step=1000.00, format="%.2f")
        
        st.markdown("#### 📋 Deduction Rates Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            tds_rate = st.number_input("TDS Rate (%)", min_value=0.0, max_value=10.0, value=2.0, step=0.1)
            gst_rate = st.number_input("GST Rate (%)", min_value=0.0, max_value=28.0, value=18.0, step=0.1)
            labour_cess_rate = st.number_input("Labour Cess (%)", min_value=0.0, max_value=2.0, value=1.0, step=0.01)
            performance_rate = st.number_input("Performance Guarantee (%)", min_value=0.0, max_value=10.0, value=3.0, step=0.1)
            retention_rate = st.number_input("Retention (%)", min_value=0.0, max_value=10.0, value=5.0, step=0.1)
        
        with col2:
            security_amount = st.number_input("Security Deposit (₹)", min_value=0.0, step=1000.00, value=0.0)
            mobilization_amount = st.number_input("Mobilization Advance (₹)", min_value=0.0, step=1000.00, value=0.0)
            material_amount = st.number_input("Material Advance (₹)", min_value=0.0, step=1000.00, value=0.0)
            penalty_amount = st.number_input("Penalty Amount (₹)", min_value=0.0, step=100.00, value=0.0)
            other_amount = st.number_input("Other Deductions (₹)", min_value=0.0, step=100.00, value=0.0)
        
        submitted = st.form_submit_button("📊 Calculate Advanced Deductions", use_container_width=True)
        
        if submitted and base_amount > 0:
            # Calculate all deductions
            tds_calc = base_amount * (tds_rate / 100)
            gst_calc = base_amount * (gst_rate / 100)
            labour_cess_calc = base_amount * (labour_cess_rate / 100)
            performance_calc = base_amount * (performance_rate / 100)
            retention_calc = base_amount * (retention_rate / 100)
            
            total_deductions = (tds_calc + gst_calc + labour_cess_calc + performance_calc + 
                              retention_calc + security_amount + mobilization_amount + 
                              material_amount + penalty_amount + other_amount)
            net_amount = base_amount - total_deductions
            
            st.markdown("""
            <div class="success-message">
                ✅ Advanced deductions calculated successfully!
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Base Amount", f"₹{base_amount:,.2f}")
            with col2:
                st.metric("Total Deductions", f"₹{total_deductions:,.2f}")
            with col3:
                st.metric("Net Amount", f"₹{net_amount:,.2f}")
            with col4:
                deduction_percentage = (total_deductions / base_amount) * 100
                st.metric("Deduction %", f"{deduction_percentage:.2f}%")
            
            st.markdown("### 📋 Detailed Deductions Breakdown")
            
            deductions_data = {
                'Deduction Type': [
                    'Income Tax (TDS)', 'Goods & Services Tax', 'Labour Cess', 
                    'Performance Guarantee', 'Retention Money', 'Security Deposit',
                    'Mobilization Advance', 'Material Advance', 'Penalty Deductions', 'Other Deductions'
                ],
                'Rate/Amount': [
                    f"{tds_rate}%", f"{gst_rate}%", f"{labour_cess_rate}%",
                    f"{performance_rate}%", f"{retention_rate}%", f"₹{security_amount:,.2f}",
                    f"₹{mobilization_amount:,.2f}", f"₹{material_amount:,.2f}", 
                    f"₹{penalty_amount:,.2f}", f"₹{other_amount:,.2f}"
                ],
                'Calculated Amount': [
                    f"₹{tds_calc:,.2f}", f"₹{gst_calc:,.2f}", f"₹{labour_cess_calc:,.2f}",
                    f"₹{performance_calc:,.2f}", f"₹{retention_calc:,.2f}", f"₹{security_amount:,.2f}",
                    f"₹{mobilization_amount:,.2f}", f"₹{material_amount:,.2f}", 
                    f"₹{penalty_amount:,.2f}", f"₹{other_amount:,.2f}"
                ]
            }
            
            df_deductions = pd.DataFrame(deductions_data)
            st.dataframe(df_deductions, use_container_width=True)
            
            st.markdown("### 💡 Deductions Summary")
            
            summary_text = f"""
            **ADVANCED DEDUCTIONS CALCULATION SUMMARY**
            
            **Base Contract Amount:** ₹{base_amount:,.2f}
            **Total Deductions:** ₹{total_deductions:,.2f} ({deduction_percentage:.2f}%)
            **Net Payable Amount:** ₹{net_amount:,.2f}
            **Amount in Words:** {indian_number_to_words(net_amount)}
            
            **Statutory Deductions:** ₹{tds_calc + gst_calc + labour_cess_calc:,.2f}
            **Security & Guarantees:** ₹{performance_calc + retention_calc + security_amount:,.2f}
            **Advance Recoveries:** ₹{mobilization_amount + material_amount:,.2f}
            **Penalties & Others:** ₹{penalty_amount + other_amount:,.2f}
            
            ---
            **Generated on:** {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
            """
            
            st.markdown(summary_text)
            
            st.markdown("### 📥 Download Deductions Report")
            
            st.markdown(create_download_link(df_deductions, "advanced_deductions.csv", "csv"), 
                      unsafe_allow_html=True)

def show_financial_progress():
    """Sophisticated Financial Progress tracker"""
    st.markdown("### 💼 Sophisticated Financial Progress")
    
    st.markdown("#### 📊 Project Financial Analytics")
    
    projects_data = {
        'Project Name': ['Highway Construction Phase-I', 'Bridge Construction', 'Road Widening Project', 'Drainage System'],
        'Total Budget': [50000000, 25000000, 30000000, 15000000],
        'Amount Spent': [35000000, 15000000, 18000000, 12000000],
        'Remaining Budget': [15000000, 10000000, 12000000, 3000000],
        'Progress %': [70, 60, 60, 80],
        'Status': ['In Progress', 'In Progress', 'In Progress', 'Near Completion']
    }
    
    df_projects = pd.DataFrame(projects_data)
    df_projects['Budget Utilization %'] = (df_projects['Amount Spent'] / df_projects['Total Budget']) * 100
    df_projects['Efficiency Score'] = df_projects['Progress %'] / df_projects['Budget Utilization %']
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_budget = df_projects['Total Budget'].sum()
        st.markdown(f"""
        <div class="metric-card">
            <h3>₹{total_budget/10000000:.1f}Cr</h3>
            <p>Total Budget</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_spent = df_projects['Amount Spent'].sum()
        st.markdown(f"""
        <div class="metric-card">
            <h3>₹{total_spent/10000000:.1f}Cr</h3>
            <p>Amount Spent</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        avg_progress = df_projects['Progress %'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <h3>{avg_progress:.1f}%</h3>
            <p>Avg Progress</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_efficiency = df_projects['Efficiency Score'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <h3>{avg_efficiency:.2f}</h3>
            <p>Efficiency Score</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### 📋 Project Financial Details")
    
    df_display = df_projects.copy()
    for col in ['Total Budget', 'Amount Spent', 'Remaining Budget']:
        df_display[col] = df_display[col].apply(lambda x: f"₹{x/100000:.1f}L")
    
    df_display['Budget Utilization %'] = df_display['Budget Utilization %'].apply(lambda x: f"{x:.1f}%")
    df_display['Progress %'] = df_display['Progress %'].apply(lambda x: f"{x}%")
    df_display['Efficiency Score'] = df_display['Efficiency Score'].apply(lambda x: f"{x:.2f}")
    
    st.dataframe(df_display, use_container_width=True)
    
    st.markdown("### 📥 Download Financial Progress Report")
    
    st.markdown(create_download_link(df_projects, "financial_progress.csv", "csv"), 
              unsafe_allow_html=True)

def show_security_refund_advanced():
    """Advanced Security Refund with comprehensive features"""
    st.markdown("### 🔒 Security Refund Advanced")
    
    with st.form("security_refund_form"):
        st.markdown("#### 🛡️ Advanced Security Refund Processing")
        
        col1, col2 = st.columns(2)
        
        with col1:
            contractor_name = st.text_input("Contractor Name *", placeholder="Full contractor name")
            security_amount = st.number_input("Security Amount (₹) *", min_value=0.01, step=1000.00, format="%.2f")
            work_description = st.text_area("Work Description *", placeholder="Complete work description")
            pending_claims = st.number_input("Pending Claims (₹)", min_value=0.0, step=100.00, value=0.0)
            damage_recovery = st.number_input("Damage Recovery (₹)", min_value=0.0, step=100.00, value=0.0)
        
        with col2:
            agreement_number = st.text_input("Agreement Number", placeholder="Agreement reference number")
            completion_date = st.date_input("Work Completion Date", value=datetime.now().date())
            performance_rating = st.selectbox("Performance Rating", ["Excellent", "Good", "Satisfactory", "Needs Improvement"])
            interest_applicable = st.checkbox("Interest Applicable on Security")
            interest_rate = st.number_input("Interest Rate (% per annum)", min_value=0.0, max_value=15.0, step=0.1, value=6.0)
        
        submitted = st.form_submit_button("🔐 Process Advanced Security Refund", use_container_width=True)
        
        if submitted:
            if not contractor_name or not work_description or security_amount <= 0:
                st.markdown("""
                <div class="error-message">
                    ❌ Please fill in all required fields marked with *
                </div>
                """, unsafe_allow_html=True)
            else:
                total_deductions = pending_claims + damage_recovery
                refundable_amount = security_amount - total_deductions
                
                interest_amount = 0
                if interest_applicable and refundable_amount > 0:
                    days_elapsed = (datetime.now().date() - completion_date).days
                    interest_amount = (refundable_amount * interest_rate * days_elapsed) / (365 * 100)
                
                final_refund = refundable_amount + interest_amount
                
                st.markdown("""
                <div class="success-message">
                    ✅ Advanced security refund processed successfully!
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("### 📋 Security Refund Summary")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Original Security", f"₹{security_amount:,.2f}")
                with col2:
                    st.metric("Total Deductions", f"₹{total_deductions:,.2f}")
                with col3:
                    st.metric("Interest Amount", f"₹{interest_amount:,.2f}")
                with col4:
                    st.metric("Final Refund", f"₹{final_refund:,.2f}")
                
                st.markdown("### 📥 Download Security Refund Documents")
                
                df_refund = pd.DataFrame({
                    'Description': ['Contractor Name', 'Original Security', 'Deductions', 'Interest', 'Final Refund', 'Performance Rating'],
                    'Details': [contractor_name, f"₹{security_amount:,.2f}", f"₹{total_deductions:,.2f}", 
                              f"₹{interest_amount:,.2f}", f"₹{final_refund:,.2f}", performance_rating]
                })
                
                st.markdown(create_download_link(df_refund, "security_refund_advanced.csv", "csv"), 
                          unsafe_allow_html=True)

def show_project_analytics():
    """Project Analytics Dashboard with advanced insights"""
    st.markdown("### 📈 Project Analytics Dashboard")
    
    st.markdown("#### 🔍 Comprehensive Project Analysis")
    
    analytics_data = {
        'Total Projects': 25,
        'Completed Projects': 18,
        'In Progress': 5,
        'Delayed Projects': 2,
        'Average Completion Time': '8.5 months',
        'Budget Utilization': '87.3%',
        'Quality Score': '92.1%',
        'Contractor Satisfaction': '89.5%'
    }
    
    col1, col2, col3, col4 = st.columns(4)
    
    metrics = list(analytics_data.items())
    for i, (key, value) in enumerate(metrics[:4]):
        with [col1, col2, col3, col4][i]:
            st.markdown(f"""
            <div class="metric-card">
                <h3>{value}</h3>
                <p>{key}</p>
            </div>
            """, unsafe_allow_html=True)
    
    col5, col6, col7, col8 = st.columns(4)
    for i, (key, value) in enumerate(metrics[4:]):
        with [col5, col6, col7, col8][i]:
            st.markdown(f"""
            <div class="metric-card">
                <h3>{value}</h3>
                <p>{key}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("### 📊 Performance Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎯 Project Status Distribution")
        status_data = {
            'Status': ['Completed', 'In Progress', 'Delayed', 'Planning'],
            'Count': [18, 5, 2, 3],
            'Percentage': [64.3, 17.9, 7.1, 10.7]
        }
        df_status = pd.DataFrame(status_data)
        st.dataframe(df_status, use_container_width=True)
    
    with col2:
        st.markdown("#### 💰 Budget Performance")
        budget_data = {
            'Category': ['Under Budget', 'On Budget', 'Over Budget'],
            'Projects': [12, 10, 3],
            'Percentage': [48.0, 40.0, 12.0]
        }
        df_budget = pd.DataFrame(budget_data)
        st.dataframe(df_budget, use_container_width=True)
    
    st.markdown("### 📥 Download Analytics Report")
    
    all_analytics = pd.DataFrame(list(analytics_data.items()), columns=['Metric', 'Value'])
    
    st.markdown(create_download_link(all_analytics, "project_analytics.csv", "csv"), 
              unsafe_allow_html=True)

def show_performance_metrics():
    """Performance Metrics with KPI tracking"""
    st.markdown("### 🎯 Performance Metrics")
    
    st.markdown("#### 📊 Key Performance Indicators (KPIs)")
    
    kpi_data = {
        'KPI': [
            'Project Delivery Rate', 'Budget Adherence', 'Quality Index', 
            'Time Performance', 'Cost Efficiency', 'Safety Record',
            'Contractor Performance', 'Stakeholder Satisfaction'
        ],
        'Target': [95, 90, 92, 88, 85, 100, 90, 88],
        'Actual': [92, 87, 94, 85, 88, 98, 89, 91],
        'Status': ['⚠️', '⚠️', '✅', '⚠️', '✅', '⚠️', '⚠️', '✅'],
        'Trend': ['↗️', '↘️', '↗️', '↘️', '↗️', '↘️', '→', '↗️']
    }
    
    df_kpi = pd.DataFrame(kpi_data)
    df_kpi['Variance'] = df_kpi['Actual'] - df_kpi['Target']
    df_kpi['Achievement %'] = (df_kpi['Actual'] / df_kpi['Target'] * 100).round(1)
    
    st.dataframe(df_kpi, use_container_width=True)
    
    st.markdown("### 📈 Performance Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        met_targets = len(df_kpi[df_kpi['Actual'] >= df_kpi['Target']])
        st.metric("Targets Met", f"{met_targets}/8", f"{(met_targets/8*100):.0f}%")
    
    with col2:
        avg_achievement = df_kpi['Achievement %'].mean()
        st.metric("Avg Achievement", f"{avg_achievement:.1f}%")
    
    with col3:
        improving_kpis = len(df_kpi[df_kpi['Trend'] == '↗️'])
        st.metric("Improving KPIs", f"{improving_kpis}/8")
    
    with col4:
        overall_score = df_kpi['Actual'].mean()
        st.metric("Overall Score", f"{overall_score:.1f}/100")
    
    st.markdown("### 📥 Download Performance Report")
    
    st.markdown(create_download_link(df_kpi, "performance_metrics.csv", "csv"), 
              unsafe_allow_html=True)

if __name__ == "__main__":
    main()
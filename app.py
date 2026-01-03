import streamlit as st
import pandas as pd
from datetime import datetime, date
import database as db
import io

# Page configuration
st.set_page_config(
    page_title="Monthly Budget Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None
)

# Initialize database
db.init_db()

# Initialize session state for login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Load Credentials from Streamlit Secrets
try:
    VALID_USERNAME = st.secrets["auth"]["username"]
    VALID_PASSWORD = st.secrets["auth"]["password"]
except KeyError:
    # Fallback for local development
    VALID_USERNAME = "koushik"
    VALID_PASSWORD = "Kk123@004"

# Login page function
def show_login_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
            <div style="text-align: center; padding: 40px 0;">
                <h1 style="color: #667eea; font-size: 2.5em; margin-bottom: 10px;">💰 Budget Tracker</h1>
                <p style="color: #666; font-size: 1.1em;">Smart Financial Management</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<h2 style='text-align: center; color: #333;'>Login</h2>", unsafe_allow_html=True)
        
        username = st.text_input(
            "Username",
            placeholder="Enter your username",
            label_visibility="collapsed"
        )
        
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            label_visibility="collapsed"
        )
        
        if st.button("🔐 Login", use_container_width=True, key="login_button"):
            if username == VALID_USERNAME and password == VALID_PASSWORD:
                st.session_state.logged_in = True
                st.success("✅ Login successful!")
                st.rerun()
            else:
                st.error("❌ Invalid username or password")

# Check if user is logged in
if not st.session_state.logged_in:
    show_login_page()
    st.stop()

# Custom CSS for modern and attractive UI
st.markdown("""
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        :root {
            --primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --primary-light: #f0f4ff;
            --secondary: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            --success: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            --warning: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
            --danger: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
        }
        
        html, body, [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #f5f7ff 0%, #f0f4ff 100%) !important;
        }
        
        [data-testid="stHeader"] {
            background: transparent !important;
        }
        
        /* Custom Styling */
        .header-container {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px 20px;
            border-radius: 20px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.2);
            text-align: center;
            animation: slideDown 0.6s ease-out;
        }
        
        .header-title {
            font-size: 2.5em;
            color: white;
            font-weight: 800;
            margin-bottom: 5px;
            text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .header-subtitle {
            font-size: 1.1em;
            color: rgba(255,255,255,0.9);
            font-weight: 300;
        }
        
        .metric-card {
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.08);
            border: 1px solid rgba(255,255,255,0.8);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            backdrop-filter: blur(10px);
        }
        
        .metric-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.15);
        }
        
        .income-card {
            background: linear-gradient(135deg, rgba(17, 153, 142, 0.05) 0%, rgba(56, 239, 125, 0.05) 100%);
            border-top: 3px solid #11998e;
        }
        
        .savings-card {
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.05) 0%, rgba(139, 92, 246, 0.05) 100%);
            border-top: 3px solid #3b82f6;
        }
        
        .balance-card {
            background: linear-gradient(135deg, rgba(168, 85, 247, 0.05) 0%, rgba(236, 72, 153, 0.05) 100%);
            border-top: 3px solid #a855f7;
        }
        
        .expenses-card {
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.05) 0%, rgba(244, 114, 124, 0.05) 100%);
            border-top: 3px solid #ef4444;
        }
        
        .remaining-positive {
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.05) 0%, rgba(52, 211, 153, 0.05) 100%);
            border-top: 3px solid #10b981;
        }
        
        .remaining-negative {
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.05) 0%, rgba(244, 114, 124, 0.05) 100%);
            border-top: 3px solid #ef4444;
        }
        
        .card-label {
            font-size: 0.9em;
            font-weight: 600;
            color: #6b7280;
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .card-value {
            font-size: 2em;
            font-weight: 800;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .income-value { 
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .savings-value { 
            background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .expenses-value { 
            background: linear-gradient(135deg, #ef4444 0%, #f45c74 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .positive-value {
            background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .negative-value {
            background: linear-gradient(135deg, #ef4444 0%, #f45c74 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .section-header {
            font-size: 1.3em;
            font-weight: 700;
            color: #1f2937;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .section-divider {
            margin: 30px 0;
            border: none;
            height: 2px;
            background: linear-gradient(90deg, transparent, #e5e7eb 20%, #e5e7eb 80%, transparent);
        }
        
        .expense-row {
            background: white;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 10px;
            border-left: 3px solid #667eea;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            transition: all 0.3s ease;
        }
        
        .expense-row:hover {
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transform: translateX(5px);
        }
        
        .button-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            border: none !important;
            padding: 12px 24px !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
        }
        
        .button-primary:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
        }
        
        .button-danger {
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%) !important;
            color: white !important;
            border: none !important;
            padding: 12px 24px !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(239, 68, 68, 0.3) !important;
        }
        
        .button-danger:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(239, 68, 68, 0.4) !important;
        }
        
        .input-group {
            position: relative;
            margin-bottom: 15px;
        }
        
        input[type="number"], input[type="text"], input[type="date"] {
            background: white !important;
            border: 1px solid #e5e7eb !important;
            border-radius: 10px !important;
            padding: 12px 16px !important;
            font-size: 1em !important;
            transition: all 0.3s ease !important;
        }
        
        input[type="number"]:focus, input[type="text"]:focus, input[type="date"]:focus {
            border-color: #667eea !important;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
        }
        
        /* Remove number input spinner */
        input[type="number"]::-webkit-outer-spin-button,
        input[type="number"]::-webkit-inner-spin-button {
            -webkit-appearance: none;
            margin: 0;
        }
        
        input[type="number"] {
            -moz-appearance: textfield;
        }
        
        .footer {
            text-align: center;
            color: #9ca3af;
            font-size: 0.9em;
            margin-top: 40px;
            padding: 20px;
            border-top: 1px solid #e5e7eb;
            animation: fadeIn 1s ease-in;
        }
        
        .footer-text {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 8px;
        }
        
        .success-message {
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(52, 211, 153, 0.1) 100%);
            border-left: 3px solid #10b981;
            padding: 12px 16px;
            border-radius: 8px;
            color: #047857;
            font-weight: 500;
        }
        
        .info-message {
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(147, 197, 253, 0.1) 100%);
            border-left: 3px solid #3b82f6;
            padding: 12px 16px;
            border-radius: 8px;
            color: #1e40af;
            font-weight: 500;
        }
        
        @keyframes slideDown {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes fadeIn {
            from {
                opacity: 0;
            }
            to {
                opacity: 1;
            }
        }
        
        .stMetric {
            background: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        }
        
        /* Remove default Streamlit styling */
        .stButton>button {
            width: 100%;
            border-radius: 10px;
            font-weight: 600;
            padding: 12px !important;
        }
        
        /* Smooth scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f5f9;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #cbd5e1;
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #94a3b8;
        }
    </style>
""", unsafe_allow_html=True)

# Add logout button in sidebar
with st.sidebar:
    st.markdown("---")
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.clear()
        st.rerun()

# Load FRESH data from database EVERY time app reruns
budget_data = db.get_budget()
expenses_data = db.get_expenses()

income = budget_data['income']
savings = budget_data['savings']

# Title and Header
st.markdown("""
    <div class="header-container">
        <div class="header-title">💰 Monthly Budget Tracker</div>
        <div class="header-subtitle">Smart Financial Management & Expense Tracking</div>
    </div>
""", unsafe_allow_html=True)

# Income and Savings Section
st.markdown('<div class="section-header">💵 Income & Savings</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<div class="card-label">💵 Monthly Income</div>', unsafe_allow_html=True)
    income_input = st.text_input(
        "Income",
        value=str(float(income)),
        key="income_input",
        label_visibility="collapsed",
        placeholder="Enter income"
    )
    try:
        new_income = float(income_input) if income_input else 0.0
        new_income = max(0.0, new_income)
        if new_income != income:
            db.update_income(new_income)
    except ValueError:
        st.error("❌ Please enter a valid number")
        new_income = income
    st.markdown(f'<div class="card-value income-value">₹{new_income:,.2f}</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card-label">🏦 Monthly Savings</div>', unsafe_allow_html=True)
    savings_input = st.text_input(
        "Savings",
        value=str(float(savings)),
        key="savings_input",
        label_visibility="collapsed",
        placeholder="Enter savings"
    )
    try:
        new_savings = float(savings_input) if savings_input else 0.0
        new_savings = max(0.0, new_savings)
        if new_savings != savings:
            db.update_savings(new_savings)
    except ValueError:
        st.error("❌ Please enter a valid number")
        new_savings = savings
    st.markdown(f'<div class="card-value savings-value">₹{new_savings:,.2f}</div>', unsafe_allow_html=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# Calculate values using fresh data
available_balance = new_income - new_savings
total_expenses = sum(float(exp['amount']) for exp in expenses_data)
remaining = available_balance - total_expenses

# Expenses Section
st.markdown('<div class="section-header">📝 Daily Expense Log</div>', unsafe_allow_html=True)

col_add = st.columns([6, 1])[1]
with col_add:
    if st.button("➕ Add Expense", use_container_width=True, help="Add a new expense entry"):
        today = datetime.now().strftime('%Y-%m-%d')
        db.add_expense(today, '', 0)
        st.rerun()

st.markdown("")

# Display expenses as editable rows
if expenses_data:
    for idx, expense in enumerate(expenses_data):
        with st.container():
            col1, col2, col3, col4 = st.columns([2, 3, 2, 1], gap="small")
            
            with col1:
                new_date = st.date_input(
                    "Date",
                    value=datetime.strptime(expense['date'], '%Y-%m-%d').date(),
                    key=f"date_{expense['id']}",
                    label_visibility="collapsed"
                )
            
            with col2:
                new_desc = st.text_input(
                    "Description",
                    value=expense['description'],
                    key=f"desc_{expense['id']}",
                    label_visibility="collapsed",
                    placeholder="What did you spend on?"
                )
            
            with col3:
                amount_input = st.text_input(
                    "Amount (₹)",
                    value=str(float(expense['amount'])),
                    key=f"amount_{expense['id']}",
                    label_visibility="collapsed",
                    placeholder="0.00"
                )
                try:
                    new_amount = float(amount_input) if amount_input else 0.0
                    new_amount = max(0.0, new_amount)
                except ValueError:
                    new_amount = float(expense['amount'])
            
            with col4:
                if st.button("🗑️", key=f"delete_{expense['id']}", help="Delete this expense"):
                    db.delete_expense(expense['id'])
                    st.rerun()
            
            # Update expense if any value changed
            if (new_date.strftime('%Y-%m-%d') != expense['date'] or 
                new_desc != expense['description'] or 
                new_amount != float(expense['amount'])):
                db.update_expense(
                    expense['id'],
                    new_date.strftime('%Y-%m-%d'),
                    new_desc,
                    new_amount
                )
                st.rerun()

else:
    st.markdown("""
        <div class="info-message">
            📊 No expenses added yet. Click <strong>'➕ Add Expense'</strong> to start tracking your spending!
        </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# Summary Section
st.markdown('<div class="section-header">📊 Budget Summary</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown(f"""
    <div class="metric-card balance-card">
        <div class="card-label">💜 Available Balance</div>
        <div class="card-value">₹{available_balance:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card expenses-card">
        <div class="card-label">📊 Total Expenses</div>
        <div class="card-value expenses-value">₹{total_expenses:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    remaining_class = "positive-value" if remaining >= 0 else "negative-value"
    card_class = "metric-card remaining-positive" if remaining >= 0 else "metric-card remaining-negative"
    st.markdown(f"""
    <div class="{card_class}">
        <div class="card-label">🎯 Remaining Balance</div>
        <div class="card-value {remaining_class}">₹{remaining:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# Action Buttons
st.markdown('<div class="section-header">⚙️ Actions</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    # Export as Excel
    if expenses_data:
        df = pd.DataFrame(expenses_data)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date', ascending=False)
        
        # Create summary
        summary_df = pd.DataFrame({
            'Category': ['Monthly Income', 'Monthly Savings', 'Available Balance', 'Total Expenses', 'Remaining Balance'],
            'Amount': [new_income, new_savings, available_balance, total_expenses, remaining]
        })
        
        # Create Excel export with multiple sheets
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            summary_df.to_excel(writer, index=False, sheet_name='Summary')
            df.to_excel(writer, index=False, sheet_name='Expenses')
        excel_data = buffer.getvalue()
        
        st.download_button(
            label="📊 Download as Excel",
            data=excel_data,
            file_name="budget_tracker.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
            key="excel_download"
        )
    else:
        st.info("No expenses to export yet")

with col2:
    if st.button("🗑️ Clear All Data", use_container_width=True, type="secondary"):
        # Clear all data from database
        db.delete_all_data()
        st.success("✅ All data has been permanently deleted!")
        st.rerun()

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class="footer">
        <div class="footer-text">
            <span>💡</span>
            <span>Your data is saved locally in the database. No cloud storage needed.</span>
        </div>
        <div style='margin-top: 10px; font-size: 0.8em; color: #d1d5db;'>
            Version 1.0 • Powered by Streamlit & SQLite
        </div>
    </div>
""", unsafe_allow_html=True)

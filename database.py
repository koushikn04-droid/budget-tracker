import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional

DB_FILE = 'budget_tracker.db'

def init_db():
    """Initialize the database with required tables"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Create expenses table
    c.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            description TEXT,
            amount REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create budget table to store income and savings
    c.execute('''
        CREATE TABLE IF NOT EXISTS budget (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            income REAL DEFAULT 0,
            savings REAL DEFAULT 0,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Check if default budget record exists
    c.execute('SELECT * FROM budget WHERE id = 1')
    if c.fetchone() is None:
        c.execute('INSERT INTO budget (id, income, savings) VALUES (1, 0, 0)')
    
    conn.commit()
    conn.close()

def get_budget() -> Dict[str, float]:
    """Get current income and savings"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT income, savings FROM budget WHERE id = 1')
    result = c.fetchone()
    conn.close()
    
    if result:
        return {'income': result[0], 'savings': result[1]}
    return {'income': 0, 'savings': 0}

def update_income(amount: float):
    """Update monthly income"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('UPDATE budget SET income = ?, updated_at = CURRENT_TIMESTAMP WHERE id = 1', (amount,))
    conn.commit()
    conn.close()

def update_savings(amount: float):
    """Update monthly savings"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('UPDATE budget SET savings = ?, updated_at = CURRENT_TIMESTAMP WHERE id = 1', (amount,))
    conn.commit()
    conn.close()

def add_expense(date: str, description: str, amount: float) -> int:
    """Add a new expense and return its ID"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        INSERT INTO expenses (date, description, amount)
        VALUES (?, ?, ?)
    ''', (date, description, amount))
    conn.commit()
    expense_id = c.lastrowid
    conn.close()
    return expense_id

def get_expenses() -> List[Dict]:
    """Get all expenses"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT id, date, description, amount FROM expenses ORDER BY date DESC')
    expenses = []
    for row in c.fetchall():
        expenses.append({
            'id': row[0],
            'date': row[1],
            'description': row[2],
            'amount': row[3]
        })
    conn.close()
    return expenses

def update_expense(expense_id: int, date: str, description: str, amount: float):
    """Update an existing expense"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        UPDATE expenses 
        SET date = ?, description = ?, amount = ?
        WHERE id = ?
    ''', (date, description, amount, expense_id))
    conn.commit()
    conn.close()

def delete_expense(expense_id: int):
    """Delete an expense"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
    conn.commit()
    conn.close()

def delete_all_data():
    """Clear all data"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('DELETE FROM expenses')
    c.execute('UPDATE budget SET income = 0, savings = 0 WHERE id = 1')
    conn.commit()
    conn.close()

def get_csv_export(income: float, savings: float, available_balance: float, expenses: List[Dict], total_expenses: float, remaining: float) -> str:
    """Generate CSV export string"""
    csv = 'Monthly Budget Tracker\n\n'
    csv += f'Income,{income}\n'
    csv += f'Savings,{savings}\n'
    csv += f'Available Balance,{available_balance}\n\n'
    csv += 'Date,Description,Amount\n'
    
    for exp in expenses:
        csv += f'{exp["date"]},"{exp["description"]}",{exp["amount"]}\n'
    
    csv += f'\nTotal Expenses,{total_expenses}\n'
    csv += f'Remaining Balance,{remaining}\n'
    
    return csv

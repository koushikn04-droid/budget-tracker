# 💰 Monthly Budget Tracker - Streamlit Edition

A simple, elegant, and free budget tracking application built with Streamlit and Python. Track your income, savings, and daily expenses with automatic data persistence using SQLite.

## ✨ Features

- 📊 Track monthly income and savings
- 📝 Add, edit, and delete daily expenses
- 💾 Automatic data persistence with SQLite database
- 📥 Download data as CSV or Excel
- 🎨 Beautiful, responsive UI
- 🔄 Real-time updates
- 🗑️ Clear all data with confirmation
- 📱 Mobile-friendly interface

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Extract/Navigate to the project folder:**
   ```bash
   cd path/to/project
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   streamlit run app.py
   ```

5. **Open in browser:**
   The app will automatically open in your default browser at `http://localhost:8501`

## 📁 Project Structure

```
project/
├── app.py                 # Main Streamlit application
├── database.py            # Database operations (SQLite)
├── requirements.txt       # Python dependencies
├── .streamlit/
│   └── config.toml        # Streamlit configuration
└── README.md              # This file
```

## 💾 Database Information

The app uses **SQLite**, which is:
- ✅ Built into Python (no external installation needed)
- ✅ File-based (no database server required)
- ✅ Perfect for local data persistence
- ✅ Completely free

**Database file:** `budget_tracker.db` (created automatically in the project root)

### Database Schema

**Expenses Table:**
- `id` - Unique identifier
- `date` - Expense date (YYYY-MM-DD)
- `description` - Expense description
- `amount` - Expense amount
- `created_at` - Timestamp

**Budget Table:**
- `id` - Single record (id=1)
- `income` - Monthly income
- `savings` - Monthly savings
- `updated_at` - Last update timestamp

## 🎯 Usage Guide

### Adding Income/Savings
1. Enter your monthly income in the "Monthly Income" field
2. Enter your monthly savings in the "Monthly Savings" field
3. Data is automatically saved

### Managing Expenses
1. Click "➕ Add Expense" to create a new expense entry
2. Enter the date, description, and amount
3. Changes are automatically saved
4. Click the "🗑️" button to delete an expense

### Downloading Data
- **CSV Export:** Click "📥 Download as CSV" to export data as a spreadsheet
- **Excel Export:** Click "📊 Download as Excel" for a formatted Excel file

### Clearing Data
1. Click "🗑️ Clear All Data"
2. Check the confirmation box
3. All data will be permanently deleted

## 🌐 Free Deployment Options

### Option 1: Streamlit Community Cloud (Recommended & FREE)

1. **Push your code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/budget-tracker.git
   git branch -M main
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign up with GitHub
   - Click "New app"
   - Select your repository, branch, and main file (`app.py`)
   - Click "Deploy"

**Features:**
- ✅ Completely free
- ✅ Automatic deployment from GitHub
- ✅ Always available online
- ✅ Shared with a public link

### Option 2: Heroku (Limited free tier)

1. **Install Heroku CLI**

2. **Create a `Procfile` in the project root:**
   ```
   web: streamlit run --server.port=$PORT --server.address=0.0.0.0 app.py
   ```

3. **Create a `setup.sh` in the project root:**
   ```bash
   mkdir -p ~/.streamlit/
   echo "[theme]
   primaryColor = \"#667eea\"
   backgroundColor = \"#ffffff\"
   secondaryBackgroundColor = \"#f0f2f6\"
   textColor = \"#262730\"
   
   [client]
   showErrorDetails = true" > ~/.streamlit/config.toml
   ```

4. **Deploy:**
   ```bash
   heroku login
   heroku create your-app-name
   git push heroku main
   ```

### Option 3: PythonAnywhere (FREE tier available)

1. Go to [pythonanywhere.com](https://www.pythonanywhere.com)
2. Create a free account
3. Upload your project files
4. Create a web app with Streamlit

### Option 4: Local Network Sharing

Run on your local machine and access from other devices on the network:

```bash
streamlit run app.py --server.address=0.0.0.0 --server.port=8501
```

Then access from other devices using: `http://your-computer-ip:8501`

## 🔧 Troubleshooting

### Database Already Exists Error
The database is created automatically. If you want to reset:
```bash
# Delete the database file
# On Windows:
del budget_tracker.db

# On macOS/Linux:
rm budget_tracker.db

# Then restart the app
streamlit run app.py
```

### Port Already in Use
```bash
streamlit run app.py --server.port 8502
```

### Module Not Found Error
Make sure all requirements are installed:
```bash
pip install -r requirements.txt
```

## 📝 Features Comparison

| Feature | Streamlit Version | Original React Version |
|---------|-------------------|----------------------|
| Add/Edit/Delete Expenses | ✅ | ✅ |
| Income & Savings Tracking | ✅ | ✅ |
| Budget Summary | ✅ | ✅ |
| Download CSV | ✅ | ✅ |
| Download Excel | ✅ | ❌ |
| Data Persistence | ✅ SQLite | ✅ Browser Storage |
| Free Deployment | ✅ | Requires Hosting |
| No Server Needed | ✅ | ✅ |
| Mobile Friendly | ✅ | ✅ |

## 🛡️ Security Notes

- All data is stored locally on your device/server
- No data is sent to external servers (except when deployed on Streamlit Cloud)
- Use HTTPS when deploying online
- Backup your `budget_tracker.db` file regularly

## 💡 Tips & Tricks

1. **Backup your data:**
   ```bash
   # Copy the database file to a safe location
   cp budget_tracker.db budget_tracker_backup.db
   ```

2. **Use the CSV export:**
   - Open in Excel or Google Sheets for advanced analysis
   - Create charts and pivot tables

3. **Sync across devices:**
   - Deploy on Streamlit Cloud to access from anywhere
   - Or set up file sync (Dropbox, OneDrive) with the database file

## 📄 License

This project is free to use and modify for personal or commercial purposes.

## 🤝 Support

For issues or questions:
1. Check the Streamlit documentation: [docs.streamlit.io](https://docs.streamlit.io)
2. Review the troubleshooting section above
3. Check Python and Streamlit version compatibility

## 🎉 Enjoy Tracking Your Budget!

Happy budgeting! If you find this helpful, consider sharing it with friends.

---

**Last Updated:** January 2, 2026

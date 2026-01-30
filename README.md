# Student Performance Management System

A Streamlit web app to manage and analyze student performance data using MySQL.

## Features
- Add student details (Name, Age, Subject, Marks)
- Store data in MySQL
- View all students in table format
- Update marks
- Delete student record
- Show Pass/Fail status
- Show average marks per subject
- Calculate:
  - Average marks
  - Pass percentage
  - Top scorer
- Visualize:
  - Bar chart of subject vs average marks
  - Pie chart of pass/fail ratio

## Tech Stack
- Frontend: Streamlit
- Backend: Python
- Database: MySQL
- Libraries: pandas, mysql-connector-python, matplotlib

## Setup Instructions
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set up MySQL and create the database and table using `db.sql`.
3. Update MySQL credentials in `app.py` (`get_connection()` function).
4. Run the app:
   ```bash
   streamlit run app.py
   ```


## Files
- `app.py`: Streamlit app source code
- `db.sql`: MySQL table creation script
- `requirements.txt`: Python dependencies
- `README.md`: Project explanation
- `Screenshots/`: App screenshots

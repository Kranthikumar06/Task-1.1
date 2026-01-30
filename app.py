import streamlit as st
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

# Database connection function
def get_connection():
	return mysql.connector.connect(
		host=os.getenv('host'),
		user=os.getenv('user'),
		password=os.getenv('AIVEN_MYSQL_PASS'),
		database=os.getenv('data'),
		port=int(os.getenv('port'))
	)

# Main app navigation
def main():
	st.markdown("<h3 style='color: red;'>STUDENT PERFORMANCE MANAGEMENT SYSTEM</h3>", unsafe_allow_html=True)
	menu = ['Add Student', 'View Students', 'Update Marks', 'Delete Student', 'Analytics', 'Visualizations']
	choice = st.sidebar.selectbox('Menu', menu)

	if choice == 'Add Student':
		add_student()
	elif choice == 'View Students':
		view_students()
	elif choice == 'Update Marks':
		update_marks()
	elif choice == 'Delete Student':
		delete_student()
	elif choice == 'Analytics':
		show_analytics()
	elif choice == 'Visualizations':
		show_visualizations()

# Placeholder functions for each feature
def add_student():
	st.subheader('Add Student')
	name = st.text_input('Name')
	age = st.slider('Age', min_value=1, max_value=120, value=18)
	subjects = ['Telugu', 'Hindi', 'English', 'Maths', 'Science', 'Social']
	subject = st.selectbox('Subject', subjects)
	marks = st.number_input('Marks', min_value=0, max_value=100)
	st.markdown("""
		<style>
		div.stButton > button:first-child {
			background-color: #4CAF50;
			color: white;
		}
		</style>
	""", unsafe_allow_html=True)
	if st.button('Add',width=100):
		if not name.strip():
			st.error('Please enter a name.')
			return
		if marks is None or marks == '' or (isinstance(marks, float) and pd.isna(marks)):
			st.error('Please enter marks.')
			return
		try:
			status = 'Pass' if marks >= 40 else 'Fail'
			conn = get_connection()
			cursor = conn.cursor()
			cursor.execute('INSERT INTO students (name, age, subject, marks, status) VALUES (%s, %s, %s, %s, %s)', (name, age, subject, marks, status))
			conn.commit()
			cursor.close()
			conn.close()
			st.success('Student added successfully!')
		except Exception as e:
			st.error(f'Error adding student: {e}')

def view_students():
	st.subheader('View Students')
	conn = get_connection()
	df = pd.read_sql('SELECT * FROM students', conn)
	conn.close()
	st.dataframe(df)

def update_marks():
	st.subheader('Update Marks')
	conn = get_connection()
	df = pd.read_sql('SELECT * FROM students', conn)
	conn.close()
	student_id = st.selectbox('Select Student ID', df['id'] if not df.empty else [])
	new_marks = st.number_input('New Marks', min_value=0.0, max_value=100.0)
	st.markdown("""
		<style>
		.stButton>button:nth-child(1) {
			background-color: #2196F3;
			color: white;
		}
		</style>
	""", unsafe_allow_html=True)
	if st.button('Update',width=100):
		try:
			conn = get_connection()
			cursor = conn.cursor()
			cursor.execute('UPDATE students SET marks=%s WHERE id=%s', (new_marks, student_id))
			conn.commit()
			cursor.close()
			conn.close()
			st.success('Marks updated successfully!')
		except Exception as e:
			st.error(f'Error updating marks: {e}')

def delete_student():
	st.subheader('Delete Student')
	conn = get_connection()
	df = pd.read_sql('SELECT * FROM students', conn)
	conn.close()
	student_id = st.selectbox('Select Student ID', df['id'] if not df.empty else [])
	st.markdown("""
		<style>
		.stButton>button:nth-child(1) {
			background-color: #f44336;
			color: white;
		}
		</style>
	""", unsafe_allow_html=True)
	if st.button('Delete',width=100):
		try:
			conn = get_connection()
			cursor = conn.cursor()
			cursor.execute('DELETE FROM students WHERE id=%s', (student_id,))
			conn.commit()
			cursor.close()
			conn.close()
			st.success('Student deleted successfully!')
		except Exception as e:
			st.error(f'Error deleting student: {e}')

def show_analytics():
	st.subheader('Analytics')
	conn = get_connection()
	df = pd.read_sql('SELECT * FROM students', conn)
	conn.close()
	if df.empty:
		st.info('No student data available.')
		return

	# Pass/Fail status (assuming pass if marks >= 40)
	df['Status'] = df['marks'].apply(lambda x: 'Pass' if x >= 40 else 'Fail')
	st.dataframe(df[['id', 'name', 'subject', 'marks', 'Status']])

	# Average marks per subject
	avg_per_subject = df.groupby('subject')['marks'].mean()
	st.write('Average Marks per Subject:')
	st.table(avg_per_subject)

	# Overall average marks
	avg_marks = df['marks'].mean()
	st.write(f'Overall Average Marks: {avg_marks:.2f}')

	# Pass percentage
	pass_count = (df['Status'] == 'Pass').sum()
	total_count = len(df)
	pass_percentage = (pass_count / total_count) * 100 if total_count > 0 else 0
	st.write(f'Pass Percentage: {pass_percentage:.2f}%')

	# Top scorer
	top_scorer = df.loc[df['marks'].idxmax()]
	st.write(f'Top Scorer: {top_scorer["name"]} ({top_scorer["marks"]} marks in {top_scorer["subject"]})')

def show_visualizations():
	st.subheader('Visualizations')
	conn = get_connection()
	df = pd.read_sql('SELECT * FROM students', conn)
	conn.close()
	if df.empty:
		st.info('No student data available.')
		return

	col1, col2 = st.columns(2)

	# Bar chart: Subject vs Average Marks
	avg_per_subject = df.groupby('subject')['marks'].mean()
	fig1, ax1 = plt.subplots(figsize=(5, 4.5))
	colors = plt.cm.Set2(range(len(avg_per_subject)))
	avg_per_subject.plot(kind='bar', ax=ax1, color=colors)
	ax1.set_ylabel('Avg Marks', color='red')
	ax1.set_xlabel('Subject',color='blue')
	ax1.set_title('Subject vs Avg')
	with col1:
		st.pyplot(fig1)

	# Pie chart: Pass/Fail Ratio
	df['Status'] = df['marks'].apply(lambda x: 'Pass' if x >= 40 else 'Fail')
	status_counts = df['Status'].value_counts()
	fig2, ax2 = plt.subplots(figsize=(5, 5))
	ax2.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', startangle=90)
	ax2.set_title('Pass/Fail Ratio')
	with col2:
		st.pyplot(fig2)
if __name__ == '__main__':
	main()

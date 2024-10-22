import os
import openai
import logging
import matplotlib.pyplot as plt
import pandas as pd
from flask import Flask, redirect, url_for, session, request, render_template, flash, send_file, jsonify
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
# Ensure PyPDF2 is installed by running: pip install PyPDF2
from PyPDF2 import PdfReader
from docx import Document
import io
from datetime import datetime
from math import ceil
from markupsafe import Markup
import json

# Setup
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Load environment variables
load_dotenv()

# Configuration
BASE_DIR = os.path.dirname(__file__)
DOCUMENTS_FOLDER = os.path.join(BASE_DIR, 'documents')
CHARTS_FOLDER = os.path.join(BASE_DIR, 'static', 'images')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx', 'csv', 'xls', 'xlsx'}
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

# Ensure DOCUMENTS_FOLDER and CHARTS_FOLDER exist
if not os.path.exists(DOCUMENTS_FOLDER):
    os.makedirs(DOCUMENTS_FOLDER)
if not os.path.exists(CHARTS_FOLDER):
    os.makedirs(CHARTS_FOLDER)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Helper Functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text(filepath, extension):
    text = ""
    try:
        if extension == 'txt':
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    text = file.read()
            except UnicodeDecodeError:
                with open(filepath, 'r', encoding='ISO-8859-1') as file:
                    text = file.read()
        elif extension == 'pdf':
            reader = PdfReader(filepath)
            for page in reader.pages:
                try:
                    text += page.extract_text() + "\n"
                except TypeError:
                    logging.error(f"Error extracting text from a PDF page in {filepath}")
                    flash(f"Error extracting text from a page in {filepath}. Some text might be missing.")
        elif extension == 'docx':
            doc = Document(filepath)
            for para in doc.paragraphs:
                text += para.text + "\n"
        elif extension in {'csv', 'xls', 'xlsx'}:
            try:
                df = pd.read_excel(filepath) if extension in {'xls', 'xlsx'} else pd.read_csv(filepath)
                text = df.to_markdown(index=False)
            except UnicodeDecodeError:
                df = pd.read_excel(filepath, encoding='ISO-8859-1') if extension in {'xls', 'xlsx'} else pd.read_csv(filepath, encoding='ISO-8859-1')
                text = df.to_markdown(index=False)
    except Exception as e:
        logging.error(f"Error extracting text from {filepath}: {e}")
        flash(f"Error extracting text from {filepath}: {e}")
    return text

def generate_chart_from_dataframe(df, chart_type):
    chart_path = os.path.join(CHARTS_FOLDER, 'chart.png')

    try:
        if chart_type == 'bmi_histogram':
            plt.figure()
            df['BMI'].plot(kind='hist', bins=10, color='skyblue', edgecolor='black')
            plt.title('BMI Distribution')
            plt.xlabel('BMI')
            plt.ylabel('Frequency')
            plt.tight_layout()
            plt.savefig(chart_path)
        elif chart_type == 'height_weight_scatter':
            plt.figure()
            plt.scatter(df['Height'], df['Weight'], color='blue')
            plt.title('Height vs. Weight')
            plt.xlabel('Height (cm)')
            plt.ylabel('Weight (kg)')
            plt.tight_layout()
            plt.savefig(chart_path)
        elif chart_type == 'gender_distribution':
            plt.figure()
            gender_counts = df['Gender'].value_counts()
            gender_counts.plot(kind='bar', color='lightgreen', edgecolor='black')
            plt.title('Gender Distribution')
            plt.xlabel('Gender')
            plt.ylabel('Count')
            plt.tight_layout()
            plt.savefig(chart_path)
        elif chart_type == 'bmi_boxplot':
            plt.figure()
            df.boxplot(column='BMI', by='Gender')
            plt.title('BMI by Gender')
            plt.suptitle('')  # Remove the default title
            plt.xlabel('Gender')
            plt.ylabel('BMI')
            plt.tight_layout()
            plt.savefig(chart_path)
        plt.close()
    except Exception as e:
        logging.error(f"Error generating chart: {e}")
        flash(f"Error generating chart: {e}")

    return chart_path

def generate_report(data):
    report = f"Report Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    report += data.describe().to_string() if isinstance(data, pd.DataFrame) else "No tabular data available for report generation."
    report_path = os.path.join(BASE_DIR, 'static', 'report.txt')
    with open(report_path, 'w') as file:
        file.write(report)
    return report_path

# Routes
@app.route('/')
def homepage():
    documents = session.get('documents', [])
    response = session.get('response', '')
    history = session.get('history', [])
    chart_path = session.get('chart_path', '')
    report_path = session.get('report_path', '')
    current_year = datetime.now().year
    logging.debug(f"Homepage loaded. Documents in session: {documents}")
    return render_template('index.html', documents=documents, response=response, history=history, chart_path=chart_path, report_path=report_path, datetime=datetime, current_year=current_year)

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('homepage'))

    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('homepage'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(DOCUMENTS_FOLDER, filename)
        file.save(filepath)
        documents = session.get('documents', [])
        documents.append({'name': filename, 'path': filepath})
        session['documents'] = documents

        logging.debug(f"Uploaded document: {filename}, path: {filepath}")
        flash(f"Loaded document: {filename}")
    else:
        flash("Unsupported file type.")

    return redirect(url_for('homepage'))

@app.route('/chat', methods=['POST'])
def chat():
    question = request.form.get('question', '').strip()
    documents = session.get('documents', [])

    if not documents:
        flash("No documents loaded. Please load document content first.")
        return redirect(url_for('homepage'))

    if not question:
        flash("Please enter a question.")
        return redirect(url_for('homepage'))

    context = ""
    for doc in documents:
        filepath = doc['path']
        extension = filepath.rsplit('.', 1)[1].lower()
        context += extract_text(filepath, extension) + "\n\n"

    prompt = f"Use the following context to answer the question. You may provide tabular data or generate a chart if needed.\n\nContext:\n{context}\n\nQuestion: {question}\nAnswer:"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant capable of generating charts, tables, and reports."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.5,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        answer = response.choices[0].message['content'].strip()
        formatted_answer = Markup(answer.replace('|', '&#124;').replace('\n', '<br>'))  # Format response for better UI display, escaping pipe characters for tables
        session['response'] = formatted_answer

        # Generate charts based on user prompt
        df = pd.read_csv(documents[0]['path'])
        if 'bmi distribution' in question.lower():
            chart_path = generate_chart_from_dataframe(df, 'bmi_histogram')
            session['chart_path'] = chart_path
        elif 'height vs weight' in question.lower():
            chart_path = generate_chart_from_dataframe(df, 'height_weight_scatter')
            session['chart_path'] = chart_path
        elif 'gender distribution' in question.lower():
            chart_path = generate_chart_from_dataframe(df, 'gender_distribution')
            session['chart_path'] = chart_path
        elif 'bmi by gender' in question.lower():
            chart_path = generate_chart_from_dataframe(df, 'bmi_boxplot')
            session['chart_path'] = chart_path

    except Exception as e:
        logging.error(f"OpenAI API error: {e}")
        formatted_answer = "Sorry, I couldn't process your request."
        session['response'] = formatted_answer

    history = session.get('history', [])
    history.append({'question': question, 'response': formatted_answer})
    session['history'] = history

    logging.debug(f"Chat question: {question}, response: {formatted_answer}")
    return redirect(url_for('homepage'))

@app.route('/get_file/<filename>')
def get_file(filename):
    filepath = os.path.join(DOCUMENTS_FOLDER, filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    else:
        flash("File not found.")
        return redirect(url_for('homepage'))

@app.route('/download_response')
def download_response():
    response = session.get('response', '')
    if response:
        response_path = os.path.join(BASE_DIR, 'static', 'response.txt')
        with open(response_path, 'w') as file:
            file.write(response)
        return send_file(response_path, as_attachment=True)
    else:
        flash("No response available to download.")
        return redirect(url_for('homepage'))

@app.route('/copy_response', methods=['POST'])
def copy_response():
    response = session.get('response', '')
    if response:
        flash("Response copied to clipboard.")
    else:
        flash("No response available to copy.")
    return redirect(url_for('homepage'))

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.')
    logging.debug("User logged out.")
    return redirect(url_for('homepage'))

# Run the Application
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5001)

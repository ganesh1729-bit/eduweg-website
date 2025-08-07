from flask import Flask, request, jsonify
import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import pytz

# Initialize the Flask App
app = Flask(__name__)

# --- Function to send data to Google Sheets ---
def send_to_google_sheets(data):
    try:
        # Load credentials from Vercel Environment Variable
        creds_json = os.environ.get('GOOGLE_CREDENTIALS')
        creds_dict = json.loads(creds_json)
        scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
                 "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)

        # Open the sheet and append the row
        sheet = client.open("EduWeg Leads").sheet1 # Assumes your sheet is named "EduWeg Leads"

        # Get current time in India Standard Time
        IST = pytz.timezone('Asia/Kolkata')
        timestamp = datetime.now(IST).strftime('%Y-%m-%d %H:%M:%S')

        row = [timestamp, data.get('name'), data.get('email'), data.get('phone'), data.get('purpose')]
        sheet.append_row(row)
        print("Successfully appended to Google Sheet.")
        return True
    except Exception as e:
        print(f"Error sending to Google Sheets: {e}")
        return False

# --- Main Backend Routes ---
@app.route('/submit-form', methods=['POST'])
def submit_form():
    try:
        # Get data from the form
        form_data = request.get_json()
        submission_data = {
            'name': form_data.get('name'),
            'email': form_data.get('email'),
            'phone': form_data.get('country_code', '') + form_data.get('phone', ''),
            'purpose': form_data.get('purpose')
        }

        # Send data to Google Sheets
        send_to_google_sheets(submission_data)

        return jsonify({'message': 'Form submitted successfully!'}), 200

    except Exception as e:
        print(f"Error in submit_form: {e}")
        return jsonify({'message': 'An error occurred.'}), 500

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/<path:path>')
def all_routes(path):
     return app.send_static_file(path)
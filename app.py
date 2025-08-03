from flask import Flask, request, jsonify
import sqlite3
import os

# Initialize the Flask App
app = Flask(__name__)

# --- Database Setup ---
def init_db():
    # Check if the database file exists
    if not os.path.exists('leads.db'):
        print("Creating database...")
        conn = sqlite3.connect('leads.db')
        c = conn.cursor()
        # Create a table to store the contact form submissions
        c.execute('''
            CREATE TABLE leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                purpose TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
        print("Database 'leads.db' and table 'leads' created.")

# --- Backend Routes ---
# This route will handle the form submission
@app.route('/submit-form', methods=['POST'])
def submit_form():
    try:
        # Get data from the form
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        phone = data.get('country_code') + data.get('phone') # Combine country code and phone
        purpose = data.get('purpose')

        # Connect to the database and insert the data
        conn = sqlite3.connect('leads.db')
        c = conn.cursor()
        c.execute("INSERT INTO leads (name, email, phone, purpose) VALUES (?, ?, ?, ?)",
                  (name, email, phone, purpose))
        conn.commit()
        conn.close()

        # Return a success message
        return jsonify({'message': 'Form submitted successfully!'}), 200

    except Exception as e:
        # Return an error message if something goes wrong
        print(f"Error: {e}")
        return jsonify({'message': 'An error occurred.'}), 500

# This route serves your main webpage
@app.route('/')
def home():
    return app.send_static_file('index.html')

# --- Run the App ---
if __name__ == '__main__':
    init_db() # Create the database on first run
    app.run(debug=True) # Run the development server
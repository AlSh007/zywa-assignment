from flask import Flask, request, jsonify, g
import sqlite3
import csv
import os
from enum import Enum

app = Flask(__name__)

# Enum to represent different card statuses
class CardStatus(Enum):
    GENERATED = "Generated"
    PICKED_UP = "Picked up"
    DELIVERED = "Delivered"
    DELIVERY_EXCEPTION = "Delivery exception"
    RETURNED = "Returned"

# Create SQLite database and table
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('card_status.db')
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.teardown_appcontext
def teardown_db(e=None):
    close_db(e)

# Initialize the database
def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS card_status (
                id TEXT ,
                card_id TEXT,
                phone_number TEXT,
                timestamp TEXT,
                status TEXT,
                PRIMARY KEY (id)
            )
        ''')
        db.commit()

# Function to read CSV file and insert/update data into the table
def populate_database(file_path):
    with app.app_context():
        db = get_db()
        cursor = db.cursor()

        # Check if the table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='card_status'")
        table_exists = cursor.fetchone()

        # If the table does not exist, create it
        if not table_exists:
            init_db()

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                id_value = row.get("ID")
                card_id_value = row.get("Card ID")
                phone_number_value = row.get("User contact", row.get("User Mobile"))
                timestamp_value = row.get("Timestamp")
                comment_value = row.get("Comment", "")

                cursor.execute('SELECT id FROM card_status WHERE id = ?', (id_value,))
                existing_record = cursor.fetchone()

                if existing_record:
                    cursor.execute('''
                        UPDATE card_status
                        SET status = ?
                        WHERE id = ?
                    ''', (comment_value, id_value))
                else:
                    cursor.execute('''
                        INSERT INTO card_status (id, card_id, phone_number, timestamp, status)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (id_value, card_id_value, phone_number_value, timestamp_value, comment_value))

        db.commit()

# Initialize the database
init_db()

# Populate the database with CSV data
for file in os.listdir("data"):
    populate_database(os.path.join("data", file))

# Function to get card status based on phone number or card ID
def get_card_status(identifier):
    with app.app_context():
        cursor = get_db().cursor()

        # Use the LIKE operator for case-insensitive string matching
        cursor.execute('''
            SELECT status FROM card_status
            WHERE id LIKE ? OR phone_number LIKE ?
        ''', (f'%{identifier}%', f'%{identifier}%'))

        result = cursor.fetchone()
        return result[0] if result else None

# Define the API endpoint
@app.route('/get_card_status', methods=['GET'])
def get_card_status_api():
    identifier = request.args.get('identifier')
    if not identifier:
        return jsonify({"error": "Identifier is required"}), 400

    card_status = get_card_status(identifier)
    if card_status is not None:
        return jsonify({"status": card_status})
    else:
        return jsonify({"error": "Card not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
    


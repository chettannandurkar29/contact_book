from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)  # Allow frontend to communicate with backend

def init_db():
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            phone TEXT,
            email TEXT
        )
    """)
    conn.commit()
    conn.close()

@app.route("/contacts", methods=["GET"])
def get_contacts():
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, phone, email FROM contacts")
    contacts = cursor.fetchall()
    conn.close()
    return jsonify([{"name": c[0], "phone": c[1], "email": c[2]} for c in contacts])

@app.route("/add", methods=["POST"])
def add_contact():
    data = request.json
    try:
        conn = sqlite3.connect("contacts.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)",
                       (data["name"], data["phone"], data["email"]))
        conn.commit()
        conn.close()
        return jsonify({"message": "Contact added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/search", methods=["GET"])
def search_contact():
    name = request.args.get("name")
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, phone, email FROM contacts WHERE name = ?", (name,))
    contact = cursor.fetchone()
    conn.close()
    if contact:
        return jsonify({"name": contact[0], "phone": contact[1], "email": contact[2]})
    return jsonify({"error": "Contact not found"}), 404

@app.route("/delete", methods=["DELETE"])
def delete_contact():
    name = request.args.get("name")
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contacts WHERE name = ?", (name,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Contact deleted successfully"})

if __name__ == "__main__":
    init_db()
    app.run(debug=True)

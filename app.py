from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Initialize SQLite database
def init_db():
    with sqlite3.connect('panther_hotel.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS reservations (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            check_in_date TEXT NOT NULL,
                            check_out_date TEXT NOT NULL,
                            room_type TEXT NOT NULL)''')
        conn.commit()

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# Rooms list page
@app.route('/rooms')
def rooms():
    with sqlite3.connect('panther_hotel.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM reservations")
        reservations = cursor.fetchall()
    return render_template('rooms.html', reservations=reservations)

# Reservation page
@app.route('/reserve', methods=['GET', 'POST'])
def reserve():
    if request.method == 'POST':
        name = request.form['name']
        check_in_date = request.form['check_in_date']
        check_out_date = request.form['check_out_date']
        room_type = request.form['room_type']

        # Insert the reservation into the database
        with sqlite3.connect('panther_hotel.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO reservations (name, check_in_date, check_out_date, room_type) VALUES (?, ?, ?, ?)",
                    (name, check_in_date, check_out_date, room_type))
            conn.commit()

        # Redirect to the success page
        return redirect(url_for('success'))

    return render_template('reservation.html')

# Success page
@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
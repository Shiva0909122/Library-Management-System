from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database connection
def get_db():
    conn = sqlite3.connect('library.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Library")
    records = cursor.fetchall()
    return render_template('index.html', records=records)

@app.route('/add', methods=['POST'])
def add_record():
    if request.method == 'POST':
        bk_name = request.form['bk_name']
        bk_id = request.form['bk_id']
        author_name = request.form['author_name']
        bk_status = request.form['bk_status']
        card_id = request.form['card_id']

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Library (BK_NAME, BK_ID, AUTHOR_NAME, BK_STATUS, CARD_ID) VALUES (?, ?, ?, ?, ?)",
                       (bk_name, bk_id, author_name, bk_status, card_id))
        conn.commit()

        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

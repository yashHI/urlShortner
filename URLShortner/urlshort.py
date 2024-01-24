from flask import Flask, render_template, request, redirect
import sqlite3
import random
import string

app = Flask(__name__)

# Create a SQLite database to store URL mappings
conn = sqlite3.connect('url_shortener.db')
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS urls (id INTEGER PRIMARY KEY AUTOINCREMENT, long_url TEXT, short_url TEXT);')
conn.commit()
conn.close()

def generate_short_url():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten():
    long_url = request.form.get('long_url')

    # Check if the URL is already in the database
    conn = sqlite3.connect('url_shortener.db')
    cursor = conn.cursor()
    cursor.execute('SELECT short_url FROM urls WHERE long_url = ?', (long_url,))
    existing_short_url = cursor.fetchone()
    conn.close()

    if existing_short_url:
        return render_template('result.html', short_url=existing_short_url[0])

    # Generate a new short URL
    short_url = generate_short_url()

    # Save the mapping in the database
    conn = sqlite3.connect('url_shortener.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO urls (long_url, short_url) VALUES (?, ?)', (long_url, short_url))
    conn.commit()
    conn.close()

    return render_template('result.html', short_url=short_url)

@app.route('/<short_url>')
def redirect_to_long_url(short_url):
    conn = sqlite3.connect('url_shortener.db')
    cursor = conn.cursor()
    cursor.execute('SELECT long_url FROM urls WHERE short_url = ?', (short_url,))
    long_url = cursor.fetchone()
    conn.close()

    if long_url:
        return redirect(long_url[0])
    else:
        return 'URL not found.'

if __name__ == '__main__':
    app.run(debug=True)

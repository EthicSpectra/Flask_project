from flask import Flask, request, redirect, render_template
import mysql.connector
import hashlib

app = Flask(__name__)

# MySQL connection setup
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',          # or '127.0.0.1' if localhost doesn't work
        user='root',               # replace with your MySQL username
        password='Akashrajk@2629',  # replace with your MySQL password
        database='url_shortener'   # the database we created in MySQL Workbench
    )
    return connection

# Function to generate short URL
def generate_short_url(original_url):
    hash_object = hashlib.md5(original_url.encode())
    short_url = hash_object.hexdigest()[:6]  # Take the first 6 characters of the hash
    return short_url

@app.route('/')
def index():
    return render_template('index.html')  # Flask will automatically search for this in the templates folder

@app.route('/shorten', methods=['POST'])
def shorten():
    original_url = request.form['url']
    short_url = generate_short_url(original_url)

    # Insert the original URL and short URL into the database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO urls (original_url, short_url) VALUES (%s, %s)", (original_url, short_url))
    conn.commit()
    cursor.close()
    conn.close()

    return f"Short URL is: <a href='/{short_url}'>/{short_url}</a>"

@app.route('/<short_url>')
def redirect_to_url(short_url):
    # Look up the short URL in the database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT original_url FROM urls WHERE short_url = %s", (short_url,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result:
        return redirect(result[0])  # Redirect to the original URL
    else:
        return "Short URL not found", 404

if __name__ == '__main__':
    app.run(debug=True)

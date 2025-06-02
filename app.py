from flask import Flask, jsonify, request
import mysql.connector
from dotenv import load_dotenv
import os


load_dotenv()
app = Flask(__name__)


def db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )


@app.route('/categories', methods=['GET'])
def get_categories():
    conn = db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name FROM categories ORDER BY id ASC")
    categories = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(categories)


@app.route("/books", methods=["GET"])
def get_books():
    conn = db_connection()
    cursor = conn.cursor(dictionary=True)

    category_id = request.args.get("category_id")
    if category_id:
        cursor.execute(
            "SELECT * FROM books WHERE category_id = %s", (category_id,))
    else:
        cursor.execute("SELECT * FROM books")

    books = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(books)


if __name__ == "__main__":
    app.run()

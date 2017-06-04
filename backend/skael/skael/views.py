from flask import jsonify
import psycopg2

from skael.app import app


@app.route("/api/hello")
def hello():
    conn = psycopg2.connect("host=postgres user=postgres dbname=postgres")
    cur = conn.cursor()
    cur.execute("SELECT version()")
    postgres_version = cur.fetchone()[0]
    cur.close()
    conn.close()

    return jsonify(response="Hello, World!", postgres_version=postgres_version)

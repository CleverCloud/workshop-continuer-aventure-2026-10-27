"""Clever Cloud workshop — demo app (version v2).

Classic Python runtime: requirements.txt + CC_PYTHON_MODULE=app:app.

Endpoints:
  GET  /        -> version and which instance answered
  GET  /health  -> 200 OK, health check target
  GET  /db      -> records a visit in PostgreSQL (needs a linked PostgreSQL add-on)
  GET  /files   -> lists the uploaded files
  POST /files   -> stores the request body as a new file (curl -X POST --data "hello" .../files)
"""
import os
import platform
from datetime import datetime, timezone

import psycopg
from flask import Flask, jsonify, request

VERSION = "v2"

app = Flask(__name__)
app.url_map.strict_slashes = False  # /db and /db/ both work

APP_HOME = os.environ.get("APP_HOME", os.getcwd())
UPLOAD_DIR = os.path.join(APP_HOME, os.environ.get("UPLOAD_DIR", "uploads"))


def instance_info():
    return {
        "number": os.environ.get("INSTANCE_NUMBER", "local"),
        "id": os.environ.get("INSTANCE_ID", "local"),
        "commit": os.environ.get("COMMIT_ID", os.environ.get("CC_COMMIT_ID", "local")),
    }


def connect():
    return psycopg.connect(
        host=os.environ["POSTGRESQL_ADDON_HOST"],
        port=int(os.environ.get("POSTGRESQL_ADDON_PORT", "5432")),
        dbname=os.environ["POSTGRESQL_ADDON_DB"],
        user=os.environ["POSTGRESQL_ADDON_USER"],
        password=os.environ["POSTGRESQL_ADDON_PASSWORD"],
        autocommit=True,
    )


@app.get("/")
def index():
    return jsonify(version=VERSION, instance=instance_info(), python=platform.python_version())


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/db")
def db():
    if not os.environ.get("POSTGRESQL_ADDON_HOST"):
        return jsonify(error="No database configured: POSTGRESQL_ADDON_HOST is not set. "
                             "Is a PostgreSQL add-on linked, and was the app restarted?"), 503
    with connect() as conn:  # closed at the end of the block
        conn.execute("CREATE TABLE IF NOT EXISTS visits (id SERIAL PRIMARY KEY, "
                     "at TIMESTAMPTZ NOT NULL DEFAULT now(), instance TEXT)")
        conn.execute("INSERT INTO visits (instance) VALUES (%s)", (instance_info()["number"],))
        count = conn.execute("SELECT count(*) FROM visits").fetchone()[0]
        return jsonify(visits=count, instance=instance_info()["number"])


@app.get("/files")
def list_files():
    names = sorted(os.listdir(UPLOAD_DIR)) if os.path.isdir(UPLOAD_DIR) else []
    return jsonify(upload_dir=UPLOAD_DIR, instance=instance_info()["number"], files=names)


@app.post("/files")
def upload_file():
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    name = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ") + ".txt"
    with open(os.path.join(UPLOAD_DIR, name), "wb") as f:
        f.write(request.get_data() or b"(empty)")
    return jsonify(saved=name, upload_dir=UPLOAD_DIR), 201


if __name__ == "__main__":
    # Local run only. On Clever Cloud, uWSGI serves `app` (CC_PYTHON_MODULE=app:app).
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8080")))

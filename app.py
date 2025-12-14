from flask import Flask, request, abort, render_template, redirect, session, url_for
import pymysql
from pymysql.cursors import DictCursor
from werkzeug.security import generate_password_hash, check_password_hash
from config import SECRET_KEY, DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, ENV

app = Flask(__name__)
app.secret_key = SECRET_KEY

def get_db_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=DictCursor,
        autocommit=True
    )

@app.get("/")
def index():
    # si ya está logueado, manda al dashboard
    if session.get("user_id"):
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/init-admin")
def init_admin():
    if ENV != "development":
        abort(404)   #ruta desaparece en produccion

    name = "Admin"
    email = "admin@helpdesk.com"
    plain_password = "Admin1234!"
    role = "ADMIN"

    password_hash = generate_password_hash(plain_password)

    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM users WHERE email=%s", (email,))
        if cur.fetchone():
            conn.close()
            return "Admin ya existe ✅"

        cur.execute(
            "INSERT INTO users (name, email, password_hash, role) VALUES (%s, %s, %s, %s)",
            (name, email, password_hash, role)
        )

    conn.close()
    return "Admin creado ✅"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", error=None)

    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT id, name, email, password_hash, role FROM users WHERE email=%s", (email,))
        user = cur.fetchone()
    conn.close()

    if not user or not check_password_hash(user["password_hash"], password):
        return render_template("login.html", error="Credenciales inválidas")

    session["user_id"] = user["id"]
    session["user_name"] = user["name"]
    session["user_role"] = user["role"]
    return redirect(url_for("dashboard"))

@app.get("/dashboard")
def dashboard():
    if not session.get("user_id"):
        return redirect(url_for("login"))
    return render_template(
        "dashboard.html",
        user_name=session.get("user_name"),
        user_role=session.get("user_role")
    )

@app.get("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)

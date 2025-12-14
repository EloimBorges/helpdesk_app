from flask import Flask, request, abort, render_template, redirect, session, url_for, jsonify
import pymysql
from pymysql.cursors import DictCursor
from werkzeug.security import generate_password_hash, check_password_hash
from config import SECRET_KEY, DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, ENV
from auth import login_required, role_required

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
    next_url = request.args.get("next", "")
    if next_url and not next_url.startswith("/"):
        next_url = ""
    return redirect(next_url or url_for("dashboard"))



@app.get("/dashboard")
@login_required
def dashboard():
    role = session.get("user_role")
    user_id = session.get("user_id")

    # Base: conteo por status
    # Ajustamos el WHERE según rol
    where = ""
    params = []

    if role == "USER":
        where = "WHERE created_by = %s"
        params = [user_id]
    elif role == "AGENT":
        # agente ve: asignados a él o sin asignar (igual que tu listado)
        where = "WHERE (assigned_to = %s OR assigned_to IS NULL)"
        params = [user_id]
    else:
        # ADMIN ve todo
        where = ""
        params = []

    stats = {"total": 0, "OPEN": 0, "IN_PROGRESS": 0, "RESOLVED": 0}

    conn = get_db_connection()
    with conn.cursor() as cur:
        # total
        cur.execute(f"SELECT COUNT(*) AS c FROM tickets {where};", tuple(params))
        stats["total"] = cur.fetchone()["c"]

        # por status
        cur.execute(
            f"""
            SELECT status, COUNT(*) AS c
            FROM tickets
            {where}
            GROUP BY status;
            """,
            tuple(params)
        )
        rows = cur.fetchall()
    conn.close()

    for r in rows:
        stats[r["status"]] = r["c"]

    return render_template(
        "dashboard.html",
        user_name=session.get("user_name"),
        user_role=role,
        stats=stats
    )


@app.get("/admin-only")
@role_required("ADMIN")
def admin_only():
    return "Solo ADMIN ✅"

@app.get("/tickets")
@login_required
def tickets_list():
    user_id = session["user_id"]
    role = session.get("user_role")

    base_sql = """
        SELECT
          t.id, t.title, t.status, t.priority, t.created_at,
          u2.name AS assigned_to_name
        FROM tickets t
        LEFT JOIN users u2 ON t.assigned_to = u2.id
    """

    params = []
    where = ""

    if role == "USER":
        where = " WHERE t.created_by = %s "
        params.append(user_id)
    elif role == "AGENT":
        where = " WHERE (t.assigned_to = %s OR t.assigned_to IS NULL) "
        params.append(user_id)
    else:
        # ADMIN ve todo
        where = ""

    sql = base_sql + where + " ORDER BY t.created_at DESC;"

    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute(sql, tuple(params))
        tickets = cur.fetchall()
    conn.close()

    return render_template(
        "tickets_list.html",
        tickets=tickets,
        user_name=session.get("user_name"),
        user_role=role
    )

@app.route("/tickets/new", methods=["GET", "POST"])
@login_required
def ticket_new():
    if request.method == "GET":
        return render_template("ticket_new.html", error=None)

    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    priority = request.form.get("priority", "MEDIUM").strip().upper()

    if priority not in ("LOW", "MEDIUM", "HIGH"):
        return render_template("ticket_new.html", error="Prioridad inválida")

    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO tickets (title, description, priority, created_by)
            VALUES (%s, %s, %s, %s)
            """,
            (title, description, priority, session["user_id"])
        )
        cur.execute("SELECT LAST_INSERT_ID() AS id;")
        new_id = cur.fetchone()["id"]
    conn.close()

    return redirect(url_for("ticket_detail", ticket_id=new_id))

@app.get("/tickets/<int:ticket_id>")
@login_required
def ticket_detail(ticket_id):
    role = session.get("user_role")
    user_id = session["user_id"]

    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT t.*, u2.name AS assigned_to_name
            FROM tickets t
            LEFT JOIN users u2 ON t.assigned_to = u2.id
            WHERE t.id = %s
            """,
            (ticket_id,)
        )
        ticket = cur.fetchone()

        if not ticket:
            conn.close()
            abort(404)

        # Permisos básicos: USER solo ve los suyos
        if role == "USER" and ticket["created_by"] != user_id:
            conn.close()
            abort(403)

        cur.execute(
            """
            SELECT c.id, c.comment, c.created_at, u.name AS user_name
            FROM ticket_comments c
            JOIN users u ON c.user_id = u.id
            WHERE c.ticket_id = %s
            ORDER BY c.created_at ASC
            """,
            (ticket_id,)
        )
        comments = cur.fetchall()

        agents = []
        if role in ("ADMIN", "AGENT"):
            cur.execute("SELECT id, name, role FROM users WHERE role IN ('ADMIN','AGENT') ORDER BY name;")
            agents = cur.fetchall()
    conn.close()
   
    return render_template(
            "ticket_detail.html",
            ticket=ticket,
            comments=comments,
            user_role=role,
            agents=agents)

@app.post("/api/tickets/<int:ticket_id>/comments")
@login_required
def api_add_comment(ticket_id):
    data = request.get_json(silent=True) or {}
    comment = (data.get("comment") or "").strip()

    if not comment:
        return jsonify({"error": "Comentario vacío"}), 400

    conn = get_db_connection()
    with conn.cursor() as cur:
        # validar ticket exista
        cur.execute("SELECT id, created_by FROM tickets WHERE id=%s", (ticket_id,))
        ticket = cur.fetchone()
        if not ticket:
            conn.close()
            return jsonify({"error": "Ticket no existe"}), 404

        # USER solo comenta en los suyos
        if session.get("user_role") == "USER" and ticket["created_by"] != session["user_id"]:
            conn.close()
            return jsonify({"error": "No autorizado"}), 403

        # insertar comentario
        cur.execute(
            "INSERT INTO ticket_comments (ticket_id, user_id, comment) VALUES (%s, %s, %s)",
            (ticket_id, session["user_id"], comment)
        )

        # devuelve info para pintar en UI
        cur.execute("SELECT NOW() AS created_at;")
        created_at = cur.fetchone()["created_at"]

    conn.close()

    return jsonify({
        "user_name": session.get("user_name"),
        "created_at": str(created_at),
        "comment": comment
    }), 201


@app.post("/tickets/<int:ticket_id>/update")
@role_required("ADMIN", "AGENT")
def ticket_update(ticket_id):
    status = request.form.get("status", "").strip().upper()
    assigned_to = request.form.get("assigned_to", "").strip()

    if status not in ("OPEN", "IN_PROGRESS", "RESOLVED"):
        abort(400)

    # assigned_to puede ser "" (sin asignar)
    assigned_to_id = None
    if assigned_to != "":
        try:
            assigned_to_id = int(assigned_to)
        except ValueError:
            abort(400)

    conn = get_db_connection()
    with conn.cursor() as cur:
        # validar ticket exista
        cur.execute("SELECT id FROM tickets WHERE id=%s", (ticket_id,))
        if not cur.fetchone():
            conn.close()
            abort(404)

        # si viene assigned_to_id, validar que sea ADMIN/AGENT
        if assigned_to_id is not None:
            cur.execute("SELECT id FROM users WHERE id=%s AND role IN ('ADMIN','AGENT')", (assigned_to_id,))
            if not cur.fetchone():
                conn.close()
                abort(400)

        cur.execute(
            "UPDATE tickets SET status=%s, assigned_to=%s WHERE id=%s",
            (status, assigned_to_id, ticket_id)
        )
    conn.close()

    return redirect(url_for("ticket_detail", ticket_id=ticket_id))

@app.get("/users")
@role_required("ADMIN")
def users_list():
    msg = request.args.get("msg")

    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT id, name, email, role, created_at FROM users ORDER BY id ASC;")
        users = cur.fetchall()
    conn.close()

    return render_template("users_list.html", users=users, msg=msg)

@app.post("/users/<int:user_id>/role")
@role_required("ADMIN")
def user_change_role(user_id):
    new_role = request.form.get("role", "").strip().upper()

    if new_role not in ("USER", "AGENT", "ADMIN"):
        abort(400)

    # Evitar que el admin se quite el rol a sí mismo por accidente
    if user_id == session.get("user_id") and new_role != "ADMIN":
        return redirect(url_for("users_list", msg="No puedes quitarte ADMIN a ti mismo."))

    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM users WHERE id=%s", (user_id,))
        if not cur.fetchone():
            conn.close()
            abort(404)

        cur.execute("UPDATE users SET role=%s WHERE id=%s", (new_role, user_id))
    conn.close()

    return redirect(url_for("users_list", msg="Rol actualizado ✅"))



@app.get("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)

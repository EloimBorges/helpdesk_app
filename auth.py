from functools import wraps
from flask import session, redirect, url_for, abort, request



def login_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if not session.get("user_id"):
            next_url = request.path
            return redirect(url_for("login", next=next_url))
        return view_func(*args, **kwargs)
    return wrapper

def role_required(*roles):
    roles_set = set(roles)

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            if not session.get("user_id"):
                next_url = request.path
                return redirect(url_for("login", next=next_url))

            user_role = session.get("user_role")
            if user_role not in roles_set:
                abort(403)  # Forbidden
            return view_func(*args, **kwargs)
        return wrapper
    return decorator
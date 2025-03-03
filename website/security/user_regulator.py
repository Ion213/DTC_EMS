from functools import wraps
from flask import redirect, url_for
from flask_login import current_user

def role_required(required_role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role != required_role:
                return redirect(url_for('admin_auth.admin_login_render_template'))  # Redirect to login or custom "access denied" page
            return func(*args, **kwargs)
        return wrapper
    return decorator


def role_required_multiple(*required_roles):  # Accepts multiple roles as arguments
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if current_user.role not in required_roles:  # Check if role is allowed
                return redirect(url_for('admin_auth.admin_login_render_template'))  # Redirect if role is not allowed
            return func(*args, **kwargs)
        return wrapper
    return decorator


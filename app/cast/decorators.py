from functools import wraps
from flask import redirect, flash, url_for
from flask.ext.login import current_user

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('That requires admin.')
            return redirect(url_for('cast.index'))
        return f(*args, **kwargs)
    return decorated_function
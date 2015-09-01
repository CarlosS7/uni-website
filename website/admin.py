from flask.ext.login import current_user
from functools import wraps
from website import login_man, db
from website.models import User

def login_required(role):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated():
              return login_man.unauthorized()
            if current_user.role != role:
                return login_man.unauthorized()
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

def add_admin(username, password, fullname):
    """Add an admin user to the database."""
    user = User(username=username, role='admin', fullname=fullname)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()

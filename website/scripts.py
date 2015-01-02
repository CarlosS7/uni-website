from flask.ext.login import current_user
from functools import wraps
from website import login_man

def login_required(role='any'):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated():
              return login_man.unauthorized()
            if ((current_user.role != role) and (role != 'any')):
                return login_man.unauthorized()
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

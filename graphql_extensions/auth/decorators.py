from functools import wraps

from .. import exceptions

__all__ = [
    'login_required',
    'staff_member_required',
    'permission_required',
]


def context(f):
    def _context(func):
        def wrapper(*args, **kwargs):
            info = args[f.__code__.co_varnames.index('info')]
            return func(info.context, *args, **kwargs)
        return wrapper
    return _context


def login_required(f):
    @wraps(f)
    @context(f)
    def wrapper(context, *args, **kwargs):
        if context.user.is_anonymous:
            raise exceptions.PermissionDenied()
        return f(*args, **kwargs)
    return wrapper


def staff_member_required(f):
    @wraps(f)
    @context(f)
    def wrapper(context, *args, **kwargs):
        user = context.user
        if user.is_active and user.is_staff:
            return f(*args, **kwargs)
        raise exceptions.PermissionDenied()
    return wrapper


def permission_required(perm):
    def check_perms(f):
        @wraps(f)
        @context(f)
        def wrapper(context, *args, **kwargs):
            if isinstance(perm, str):
                perms = (perm,)
            else:
                perms = perm

            if not context.user.has_perms(perms):
                raise exceptions.PermissionDenied()
            return f(*args, **kwargs)
        return wrapper
    return check_perms

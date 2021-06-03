from functools import wraps

from . import exceptions

__all__ = [
    'user_passes_test',
    'login_required',
    'staff_member_required',
    'superuser_required',
    'permission_required',
]


def context(f):
    def decorator(func):
        def wrapper(*args, **kwargs):
            info = args[f.__code__.co_varnames.index('info')]
            return func(info.context, *args, **kwargs)
        return wrapper
    return decorator


def user_passes_test(test_func, exc=exceptions.PermissionDenied):
    def decorator(f):
        @wraps(f)
        @context(f)
        def wrapper(context, *args, **kwargs):
            if test_func(context.user):
                return f(*args, **kwargs)
            raise exc
        return wrapper
    return decorator


login_required = user_passes_test(lambda u: u.is_authenticated)
staff_member_required = user_passes_test(lambda u: u.is_active and u.is_staff)
superuser_required = user_passes_test(lambda u: u.is_superuser)


def permission_required(perm):
    def check_perms(user):
        if isinstance(perm, str):
            perms = (perm,)
        else:
            perms = perm

        if user.has_perms(perms):
            return True
        return False
    return user_passes_test(check_perms)

from django.utils.decorators import available_attrs

try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps  # Python 2.4 fallback.

def login_not_required(view_func):
    """
    Marks a view function as not requiring login (LoginRequiredMiddleware).
    """
    # We could just do view_func.login_exempt = True, but decorators
    # are nicer if they don't have side-effects, so we return a new
    # function.
    def wrapped_view(*args, **kwargs):
        return view_func(*args, **kwargs)
    wrapped_view.login_exempt = True
    return wraps(view_func, assigned=available_attrs(view_func))(wrapped_view)


from functools import wraps
from server.settings import AUTHENTICATION_REQUIRED_ACTIONS
from protocol.server import Response
from protocol.codes import UNAUTHORIZED


def authentication_required(func):
    """Декоратор для проверки аутентификации. Если action находится в AUTHENTICATION_REQUIRED_ACTIONS,
    и пользователь не авторизован, то декоратор вернет код 401 вместо любого другого кода"""
    @wraps(func)
    def inner_function(server_obj, request):
        if request.action in AUTHENTICATION_REQUIRED_ACTIONS:  # actions must be in authorized tuple
            if not server_obj.user.is_authenticated:
                return Response(code=UNAUTHORIZED, action=request.action,
                                body=f'Action {request.action} denied until unauthorized')
            else:
                return func(server_obj, request)
        else:
            return func(server_obj, request)

    return inner_function

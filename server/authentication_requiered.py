from functools import wraps
from server.settings import AUTHENTICATION_REQUIRED_ACTIONS
from protocol.server import Response
from protocol.codes import UNAUTHORIZED


def authentication_required(func):  # actions must be authorized tuple

    @wraps(func)
    def inner_function(server_obj, request, user_obj):
        if request.action in AUTHENTICATION_REQUIRED_ACTIONS:
            if not user_obj.is_authenticated:
                return Response(code=UNAUTHORIZED, action=request.action,
                                body=f'Action {request.action} denied until unauthorized')
        else:
            return func(server_obj, request, user_obj)

    return inner_function

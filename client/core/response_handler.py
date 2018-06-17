from client.core.actions.presence_response import presence_response_processing
from client.core.actions.registration_response import registration_response_processing
from client.core.actions.authenticate_response import authenticate_response_processing
from client.core.actions.join_response import join_response_processing
from client.core.actions.msg_response import msg_response_processing

response_handler = {
    'presence': presence_response_processing,
    'registration': registration_response_processing,
    'authenticate': authenticate_response_processing,
    'join': join_response_processing,
    'msg': msg_response_processing,
}

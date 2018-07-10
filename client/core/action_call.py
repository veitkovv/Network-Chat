from client.core.actions.presence import presence_request, presence_response
from client.core.actions.registration import registration_response
from client.core.actions.authenticate import authenticate_request, authenticate_response
from client.core.actions.join import join_response
from client.core.actions.msg import msg_response
from client.core.actions.get_contacts import get_contacts_response

request = {
    'presence': presence_request,
    # 'registration': registration_request,
    'authenticate': authenticate_request,
    # 'join': join_request,
    # 'msg': msg_request,
    # 'get_contacts': get_contacts_request,
}

response = {
    'presence': presence_response,
    'registration': registration_response,
    'authenticate': authenticate_response,
    'join': join_response,
    'msg': msg_response,
    'get_contacts': get_contacts_response,
}

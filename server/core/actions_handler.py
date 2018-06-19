from server.core.actions.presence import presence_processing
from server.core.actions.registration import registration_processing
from server.core.actions.authenticate import authenticate_processing
from server.core.actions.join import join_processing
from server.core.actions.msg import msg_processing
from server.core.actions.add_contact import add_contact_processing
from server.core.actions.del_contact import del_contact_processing
from server.core.actions.leave import leave_processing

actions_handler = {
    'presence': presence_processing,
    'registration': registration_processing,
    'authenticate': authenticate_processing,
    'join': join_processing,
    'msg': msg_processing,
    'add_contact': add_contact_processing,
    'del_contact': del_contact_processing,
    'leave': leave_processing,
}

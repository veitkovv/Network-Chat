from server.core.actions.presence import presence_processing
from server.core.actions.registration import registration_processing
from server.core.actions.authenticate import authenticate_processing

actions_handler = {
    'presence': presence_processing,
    'registration': registration_processing,
    'authenticate': authenticate_processing,
}

from server.core.actions.presence import presence_processing
from server.core.actions.authenticate import authenticate_processing

action_handler = {
    'presence': presence_processing,
    'authenticate': authenticate_processing,
}

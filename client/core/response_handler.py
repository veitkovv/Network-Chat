from client.core.actions.presence_response import presence_response_processing
from client.core.actions.registration_response import registration_response_processing

response_handler = {
    'presence': presence_response_processing,
    'registration': registration_response_processing,
}

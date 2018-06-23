from protocol.codes import IMPORTANT_NOTICE


def get_contacts_response_processing(response_message, ui_instance):
    if response_message.code == IMPORTANT_NOTICE:
        ui_instance.display_contact_list(response_message)

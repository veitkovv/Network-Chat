from protocol.settings import MESSAGE_SIZE_NUM, ENCODING


def pick_messages_from_stream(raw_bytes):
    """
    Метод определяет размер сообщения, и из байтовой строки возвращает по одному сообщению
    TCP протокол может склеить данные
    """
    # Первые MESSAGE_SIZE_NUM символов в сообщении будут отданы под размер сообщения.
    # Это нужно для избежания склеивания сообщения
    while raw_bytes:
        # Определим размер сообщения
        message_size = int(raw_bytes[:MESSAGE_SIZE_NUM])
        # Выберем из строки сообщение
        single_message = raw_bytes[MESSAGE_SIZE_NUM:message_size + MESSAGE_SIZE_NUM]
        # Отделим наше сообщение от сырой строки, на случай если сообщений больше одного
        raw_bytes = raw_bytes[message_size + MESSAGE_SIZE_NUM:]
        yield single_message


def append_message_len_to_message(message_bytes):
    """
    Считает длинну сообщения.
    Так как под длинну сообщения задействуется фиксированное количество символов = MESSAGE_SIZE_NUM,
    для чисел меньше четвертого порядка в начало дописываются нули.
    Например 4 = 0004, 23 = 0023, 554 = 0554.
    :return длинна + исходная строка
    """
    message_len = f'{len(message_bytes):0{MESSAGE_SIZE_NUM}d}'
    return message_len.encode(ENCODING) + message_bytes

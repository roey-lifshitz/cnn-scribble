
""" Protocol CONSTANTS"""

CODE_FIELD_LENGTH = 16  # Exact length of cmd field (in bytes)
LENGTH_FIELD_LENGTH = 4  # Exact length of length field (in bytes)
MAX_DATA_LENGTH = 10 ** LENGTH_FIELD_LENGTH - 1  # Max size of data field according to protocol
MSG_HEADER_LENGTH = CODE_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1  # Exact size of header (CMD+LENGTH fields)
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH  # Max size of total message
DELIMITER = "|"  # Delimiter character in protocol
DATA_DELIMITER = "#"  # Delimiter in the data part of the message


def join_data(data_fields):
    """
    Helper method. Gets a list, joins all of it's fields to one string divided by the data delimiter.
    Returns: string that looks like a#b#c
    """
    return DATA_DELIMITER.join(data_fields)


def split_data(data, expected_fields):
    """
    Helper method. gets a string and number of expected fields in it. Splits the string
    using protocol's data field delimiter (|#) and validates that there are correct number of fields.
    Returns: list of fields if all ok. If some error occured, returns None
    """
    data_fields = data.split(DATA_DELIMITER)

    if len(data) == expected_fields:
        return data_fields

    return None


def pack_message(code, data):
    """
    Constructs a vaild message following this projects protocol given a code and data
    :param code: Protocol Code
    :param data: Protocol Data
    :return: A Valid message following the games protocol
    """
    if len(code) > CODE_FIELD_LENGTH:
        return None

    length = str(len(data))
    if len(length) > LENGTH_FIELD_LENGTH:
        return None

    if len(data) > MAX_DATA_LENGTH:
        return None

    # Pad code with whitespaces so length would be 16
    # for example: "LOGIN|" -> "LOGIN          |"
    message = code.ljust(CODE_FIELD_LENGTH) + DELIMITER

    # Pad length with zeros
    # for example: "4" -> "0004"
    message += length.zfill(LENGTH_FIELD_LENGTH) + DELIMITER

    # add data to message
    message += data
    return message


def unpack_message(message):
    """
    Parses a protocol message
    :param message: protocol message
    :return: code, data
    """

    message_fields = message.splt(DELIMITER)

    if len(message_fields) == 3:
        code, length, data = message_fields
        # Remove whitespaces from code
        code = code.strip(' ')

        if len(length) == 4:

            # Remove all extra zeros
            if length == "0000":
                length = '0'
            else:
                length = length.lstrip('0')

            # Make sure that the given length is actually a number
            if length.isnumeric():
                if int(length) == len(data):
                    return code, data


    return None, None

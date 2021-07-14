class Message(object):
    RLGYM_HEADER_END_TOKEN                               = [13771, 83712, 83770]
    RLGYM_BODY_END_TOKEN                                 = [82772, 83273, 83774]
    RLGYM_NULL_MESSAGE_HEADER                            = [83373, 83734, 83775]
    RLGYM_NULL_MESSAGE_BODY                              = [83744, 83774, 83876]
    RLGYM_CONFIG_MESSAGE_HEADER                          = [83775, 53776, 83727]
    RLGYM_STATE_MESSAGE_HEADER                           = [63776, 83777, 83778]
    RLGYM_AGENT_ACTION_MESSAGE_HEADER                    = [87777, 83778, 83779]
    RLGYM_RESET_GAME_STATE_MESSAGE_HEADER                = [83878, 83779, 83780]
    RLGYM_AGENT_ACTION_IMMEDIATE_RESPONSE_MESSAGE_HEADER = [83799, 83780, 83781]
    RLGYM_REQUEST_LAST_BOT_INPUT_MESSAGE_HEADER          = [83781, 83781, 83682]
    RLGYM_LAST_BOT_INPUT_MESSAGE_HEADER                  = [11781, 83782, 83983]
    RLGYM_RESET_TO_SPECIFIC_GAME_STATE_MESSAGE_HEADER    = [12782, 83783, 80784]

    @staticmethod
    def deserialize_header(message_floats):
        assert type(message_floats) in (list, tuple), "!ATTEMPTED TO DECODE MESSAGE HEADER FROM NON-LIST TYPE! []".format(type(message_floats))
        m = message_floats
        header_end = Message._find_first(m, Message.RLGYM_HEADER_END_TOKEN)
        return m[:header_end]

    @staticmethod
    def _find_first(lst, target):
        n = len(target)
        for i in range(len(lst)):
            if lst[i] == target[0] and lst[i:i+n] == target:
                return i
        return None

    def __init__(self, header=None, body=None):
        if header is None:
            header = Message.RLGYM_NULL_MESSAGE_HEADER
        if body is None:
            body = Message.RLGYM_NULL_MESSAGE_BODY

        self.body = body
        self.header = header

    def serialize(self):
        return self.header + Message.RLGYM_HEADER_END_TOKEN + self.body + Message.RLGYM_BODY_END_TOKEN

    def deserialize(self, message_floats):
        assert type(message_floats) == list, "!ATTEMPTED TO DECODE MESSAGE HEADER FROM NON-LIST TYPE! []".format(type(message_floats))
        m = message_floats

        header_end = Message._find_first(m, Message.RLGYM_HEADER_END_TOKEN)
        header = m[:header_end]

        start = Message._find_first(m, Message.RLGYM_HEADER_END_TOKEN) + len(Message.RLGYM_HEADER_END_TOKEN)
        end = Message._find_first(m,Message.RLGYM_BODY_END_TOKEN)
        body = m[start:end]

        self.body = body
        self.header = header


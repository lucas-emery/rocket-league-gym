
class Message(object):
    RLGYM_HEADER_END_TOKEN = "RLGEHEADER"
    RLGYM_BODY_END_TOKEN = "RLGEBODY"

    RLGYM_NULL_MESSAGE_HEADER = "RLGNMH"
    RLGYM_NULL_MESSAGE_BODY = "RLGNMB"
    RLGYM_CONFIG_MESSAGE_HEADER = "RLGC"

    RLGYM_STATE_MESSAGE_HEADER = "RLGSMH"
    RLGYM_AGENT_ACTION_MESSAGE_HEADER = "RLGAAMH"
    RLGYM_RESET_GAME_STATE_MESSAGE_HEADER = "RLGRGSMH"
    RLGYM_AGENT_ACTION_IMMEDIATE_RESPONSE_MESSAGE_HEADER = "RLGAAIRMH"

    RLGYM_REQUEST_LAST_BOT_INPUT_MESSAGE_HEADER = "RLGRLBIMH"
    RLGYM_LAST_BOT_INPUT_MESSAGE_HEADER = "RLGLBIMH"


    def __init__(self, header=None, body=None):
        if header is None:
            header = Message.RLGYM_NULL_MESSAGE_HEADER
        if body is None:
            body = Message.RLGYM_NULL_MESSAGE_BODY

        self.body = body
        self.header = header

    def serialize(self):
        return "{header}{header_token}{body}{body_token}\0".format(header=self.header,
                                                                   header_token=Message.RLGYM_HEADER_END_TOKEN,
                                                                   body=self.body,
                                                                   body_token=Message.RLGYM_BODY_END_TOKEN)

    def deserialize(self, serialized_str):
        s = serialized_str

        header = s[:s.find(Message.RLGYM_HEADER_END_TOKEN)]
        start = s.find(Message.RLGYM_HEADER_END_TOKEN) + len(Message.RLGYM_HEADER_END_TOKEN)
        end = s.find(Message.RLGYM_BODY_END_TOKEN)
        body = s[start:end]

        self.body = body
        self.header = header
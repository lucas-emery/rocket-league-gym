from rlgym.communication import Message

import win32file
import win32pipe
import time


class CommunicationHandler(object):
    RLGYM_GLOBAL_PIPE_NAME = r"\\.\pipe\RLGYM_GLOBAL_COMM_PIPE"
    RLGYM_DEFAULT_PIPE_SIZE = 4096

    def __init__(self):
        self._current_pipe_name = CommunicationHandler.RLGYM_GLOBAL_PIPE_NAME
        self._pipe = None
        self._connected = False

    def receive_message(self, header=None, num_attempts=100):
        #TODO: deal with discarded messages while waiting for a specific header
        if not self.is_connected():
            print("ATTEMPTED TO RECEIVE MESSAGE WITH NO CONNECTION")
            raise BrokenPipeError

        m = Message()
        for i in range(num_attempts):
            code, msg_bytes = win32file.ReadFile(self._pipe, CommunicationHandler.RLGYM_DEFAULT_PIPE_SIZE)
            msg_str = bytes.decode(msg_bytes)
            m.deserialize(msg_str)

            if header is None or header == m.header:
                break

        #TODO: make sure users of this object deal with the null message response
        return m

    def send_message(self, message=None, header=None, body=None):
        if not self.is_connected():
            print("ATTEMPTED TO SEND MESSAGE WITH NO CONNECTION")
            raise BrokenPipeError

        if message is None:
            if header is None:
                header = Message.RLGYM_NULL_MESSAGE_HEADER

            if body is None:
                body = Message.RLGYM_NULL_MESSAGE_BODY

            message = Message(header=header, body=body)

        # print("Sending message {}...".format(message.header))
        serialized = message.serialize()
        win32file.WriteFile(self._pipe, str.encode(serialized))

    def open_pipe(self, pipe_name=None):
        if pipe_name is None:
            pipe_name = CommunicationHandler.RLGYM_GLOBAL_PIPE_NAME

        if self._connected:
            self.close_pipe()
        self._connected = False

        self._pipe = win32pipe.CreateNamedPipe(pipe_name,
                                               win32pipe.PIPE_ACCESS_DUPLEX,

                                               win32pipe.PIPE_TYPE_MESSAGE |
                                               win32pipe.PIPE_READMODE_MESSAGE |
                                               win32pipe.PIPE_WAIT,

                                               1, CommunicationHandler.RLGYM_DEFAULT_PIPE_SIZE,
                                               CommunicationHandler.RLGYM_DEFAULT_PIPE_SIZE, 0, None)
        win32pipe.ConnectNamedPipe(self._pipe)

        self._current_pipe_name = pipe_name
        self._connected = True

    def close_pipe(self):
        self._connected = False
        win32file.CloseHandle(self._pipe)

    def is_connected(self):
        return self._connected

    @staticmethod
    def format_pipe_id(pipe_id):
        return r"\\.\pipe\{}".format(pipe_id)
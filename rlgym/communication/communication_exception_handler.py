import sys
import traceback

UNKNOWN_ERROR = -1
EOF_ERROR = 0
BROKEN_PIPE_ERROR = 1


def _eof_error():
    print("RLGym Local Pipe has crashed! Please close Rocket League and re-launch RLGym.")
    return EOF_ERROR


def handle_exception(e):
    args = e.args
    exception_code = UNKNOWN_ERROR
    print("RLGym has encountered an exception!\nException traceback:\n{}".format(traceback.format_exc()))
    if "The pipe has been ended." in args:
        exception_code = _eof_error()
    else:
        print("EXCEPTION ARGS:", args)

    return exception_code

import sys
import traceback

def _eof_error():
    print("RLGym Local Pipe has crashed! Please close Rocket League and re-launch RLGym.")
    sys.exit(-1)


def handle_exception(e):
    args = e.args
    print("RLGym has encountered an exception!\nException traceback:\n{}".format(traceback.format_exc()))
    if "The pipe has been ended." in args:
        _eof_error()
    else:
        print("EXCEPTION ARGS:",args)
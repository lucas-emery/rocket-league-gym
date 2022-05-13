import pywintypes
import win32gui
import win32process

# show_codes: 9 to show, 6 to hide
HIDE = 6
SHOW = 9


def toggle_rl_windows(minimize=True):
    # Minimize all RL processes
    window_ledger = {}

    def win_enum_handler(hwnd, ctx):
        if win32gui.IsWindowVisible(hwnd):
            if win32gui.GetWindowText(hwnd).find("Rocket League") != -1:
                window_ledger[hwnd] = win32gui.GetWindowText(hwnd)

    win32gui.EnumWindows(win_enum_handler, None)
    code = HIDE if minimize else SHOW
    for k in window_ledger.keys():
        win32gui.ShowWindow(k, code)
        print(f"{window_ledger[k]} ({k}) is now {'visible' if code == SHOW else 'hidden'}")


def toggle_rl_process(pid, minimize=True):
    # Minimize a single RL process
    window_ledger = {}

    def win_enum_handler(hwnd, ctx):
        if win32gui.IsWindowVisible(hwnd):
            _, selected_pid = win32process.GetWindowThreadProcessId(hwnd)
            if selected_pid == pid:
                window_ledger[hwnd] = win32gui.GetWindowText(hwnd)
                return False  # Stop enumeration

    try:
        win32gui.EnumWindows(win_enum_handler, None)
    except pywintypes.error as e:
        if e.args[0] != 0:  # Stopping iteration causes an error with code 0 for some reason
            raise e

    code = HIDE if minimize else SHOW
    for k in window_ledger.keys():
        win32gui.ShowWindow(k, code)
        print(f"{window_ledger[k]} ({k}) is now hidden")

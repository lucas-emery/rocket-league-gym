import ctypes
import time
from win32con import PROCESS_ALL_ACCESS, PROCESS_SET_QUOTA, PROCESS_QUERY_INFORMATION

def page_rocket_league(rl_pid: int = -1, delay: int = 0):
    if rl_pid > 0:
        if delay > 0:
            time.sleep(delay)

        print("Paging Rocket League process id", rl_pid)

        # We require specific permissions to be able to page the process
        # See https://docs.microsoft.com/en-us/windows/win32/api/psapi/nf-psapi-emptyworkingset
        perms = PROCESS_ALL_ACCESS | PROCESS_SET_QUOTA | PROCESS_QUERY_INFORMATION

        Kernel32 = ctypes.WinDLL('kernel32.dll')
        Psapi = ctypes.WinDLL('Psapi.dll')

        try:
            # Get the process handle, trigger the page removal, and cleanup the handle
            hProcess = Kernel32.OpenProcess(perms, False, rl_pid)

            if hProcess:
                Psapi.EmptyWorkingSet(hProcess)
                Kernel32.CloseHandle(hProcess)
                return True
        except:
            # We will ignore any issues where
            pass

    return False
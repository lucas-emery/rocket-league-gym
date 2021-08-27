import platform
from dataclasses import dataclass
import subprocess
import webbrowser
from pathlib import Path
from typing import Optional
from rlgym.gamelaunch.epic_launch import launch_with_epic_simple, launch_with_epic_login_trick
import os

# Copied from https://github.com/RLBot/RLBot/blob/master/src/main/python/rlbot/setup_manager.py

class ROCKET_LEAGUE_PROCESS_INFO:
    GAMEID = 252950
    PROGRAM_NAME = 'RocketLeague.exe'
    PROGRAM = 'RocketLeague.exe'
    REQUIRED_ARGS = {r'-pipe'}

    @staticmethod
    def get_ideal_args(pipe_id):
        # We are specifying RLBot_PacketSendRate=240, which will override people's TARLBot.ini settings.
        # We believe there is no downside to 240. See https://github.com/RLBot/RLBot/wiki/Tick-Rate
        return ['-pipe', f'{pipe_id}', '-nomovie']


class LaunchPreference:
    STEAM = 'steam'
    EPIC = 'epic'
    EPIC_LOGIN_TRICK = EPIC + '_login_trick'


def run_injector():
    print("Executing injector...")
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    injector_command = os.path.join(cur_dir, os.pardir, "plugin", "RLMultiInjector.exe")
    subprocess.Popen([injector_command])


def launch_rocket_league(pipe_id, launch_preference: str = LaunchPreference.EPIC) -> Optional[subprocess.Popen]:
    """
    Launches Rocket League but does not connect to it.
    """
    ideal_args = ROCKET_LEAGUE_PROCESS_INFO.get_ideal_args(pipe_id)

    if not launch_preference.startswith((LaunchPreference.EPIC, LaunchPreference.STEAM)):
        if os.path.isfile(launch_preference):
            return subprocess.Popen([launch_preference] + ideal_args)
        else:
            print("path_to_rl doesn't point to RocketLeague.exe")

    if launch_preference.startswith(LaunchPreference.EPIC):
        if launch_preference == LaunchPreference.EPIC_LOGIN_TRICK:
            proc = launch_with_epic_login_trick(ideal_args)
            if proc is not None:
                print('Launched with Epic login trick')
                return proc
            else:
                print("Epic login trick seems to have failed, falling back to simple Epic launch.")
        # Fall back to simple if the tricks failed or we opted out of tricks.
        game_process = launch_with_epic_simple(ideal_args)
        if game_process:
            print('Launched Epic version')
            return game_process

    # Try launch via Steam.
    steam_exe_path = try_get_steam_executable_path()
    if steam_exe_path:  # Note: This Python 3.8 feature would be useful here https://www.python.org/dev/peps/pep-0572/#abstract
        exe_and_args = [
                           str(steam_exe_path),
                           '-applaunch',
                           str(ROCKET_LEAGUE_PROCESS_INFO.GAMEID),
                       ] + ideal_args
        # print(f'Launching Rocket League with: {exe_and_args}')
        _ = subprocess.Popen(exe_and_args)  # This is deliberately an orphan process.
        print('Launched Steam version')
        return

    print(f'Launching Rocket League using Steam-only fall-back launch method with args: {ideal_args}')
    print("You should see a confirmation pop-up, if you don't see it then click on Steam! "
                     'https://gfycat.com/AngryQuickFinnishspitz')
    args_string = '%20'.join(ideal_args)

    # Try launch via terminal (Linux)
    if platform.system() == 'Linux':
        linux_args = [
            'steam',
            f'steam://rungameid/{ROCKET_LEAGUE_PROCESS_INFO.GAMEID}//{args_string}'
        ]

        try:
            _ = subprocess.Popen(linux_args)
            print('Launched Steam Linux version')
            return
        except OSError:
            print('Could not launch Steam executable on Linux.')

    try:
        print("Launching rocket league via steam browser URL as a last resort...")
        webbrowser.open(f'steam://rungameid/{ROCKET_LEAGUE_PROCESS_INFO.GAMEID}//{args_string}')
    except webbrowser.Error:
        print(f'Unable to launch Rocket League. Please launch Rocket League manually using the -pipe {pipe_id} option to continue.')


def try_get_steam_executable_path() -> Optional[Path]:
    """
    Tries to find the path of the Steam executable.
    Has platform specific code.
    """

    try:
        from winreg import OpenKey, HKEY_CURRENT_USER, ConnectRegistry, QueryValueEx, REG_SZ
    except ImportError as e:
        return  # TODO: Linux support.

    try:
        key = OpenKey(ConnectRegistry(None, HKEY_CURRENT_USER), r'Software\Valve\Steam')
        val, val_type = QueryValueEx(key, 'SteamExe')
    except FileNotFoundError:
        return
    if val_type != REG_SZ:
        return
    return Path(val)
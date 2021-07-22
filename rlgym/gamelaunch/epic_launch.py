import json
import os
import subprocess
import webbrowser
from pathlib import Path
from time import sleep
import psutil
from typing import Set, Tuple, Union, List, Optional
import re

# Copied from https://github.com/RLBot/RLBot/blob/master/src/main/python/rlbot/gamelaunch/epic_launch.py

def launch_with_epic_simple(ideal_args: List[str]) -> Optional[subprocess.Popen]:
    try:
        # Try launch via Epic Games
        epic_rl_exe_path = locate_epic_games_launcher_rocket_league_binary()
        if epic_rl_exe_path is not None:
            exe_and_args = [str(epic_rl_exe_path)] + ideal_args
            # print(f'Launching Rocket League with: {exe_and_args}')
            try:
                return subprocess.Popen(exe_and_args)
            except Exception as e:
                print(f'Unable to launch via Epic due to: {e}')
    except:
        print('Unable to launch via Epic.')


def launch_with_epic_login_trick(ideal_args: List[str]) -> Optional[subprocess.Popen]:
    try:
        # launch using shortcut technique
        webbrowser.open('com.epicgames.launcher://apps/Sugar?action=launch&silent=true')
        process = None
        for i in range(10):
            sleep(1)
            rl_running, process = is_process_running('RocketLeague.exe', 'RocketLeague.exe', set())
            if rl_running:
                break

        if process is None:
            return

        # get the args from the process
        all_args = process.cmdline()

        process.kill()
        all_args[1:1] = ideal_args
        print(f"Killed old rocket league, reopening with {all_args}")
        return subprocess.Popen(all_args, shell=True)
    except:
        return


def locate_epic_games_launcher_rocket_league_binary() -> Optional[Path]:
    # Make sure we're on windows, this will go poorly otherwise
    try:
        import winreg
    except ImportError:
        return

    # List taken from https://docs.unrealengine.com/en-US/GettingStarted/Installation/MultipleLauncherInstalls/index.html
    possible_registry_locations = (
        (winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\\Epic Games\\EpicGamesLauncher'),
        (winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\\WOW6432Node\\Epic Games\\EpicGamesLauncher'),
        (winreg.HKEY_CURRENT_USER, 'SOFTWARE\\Epic Games\\EpicGamesLauncher'),
        (winreg.HKEY_CURRENT_USER, 'SOFTWARE\\WOW6432Node\\Epic Games\\EpicGamesLauncher')
    )

    def search_for_manifest_file(app_data_path: Path) -> Optional[Path]:
        # Loop through the files ending in *.item in app_data_path/Manifests
        # Parse them as JSON and locate the one where MandatoryAppFolderName is 'rocketleague'
        # Extract the binary location and return it.
        for file in app_data_path.glob("*.item"):
            with open(app_data_path / file, 'r') as f:
                try:
                    data = json.load(f)
                except Exception:
                    continue

            if data.get('MandatoryAppFolderName') == 'rocketleague':
                return data

    for possible_location in possible_registry_locations:
        try:
            # get the path to the launcher's game data stuff
            path = Path(winreg.QueryValueEx(winreg.OpenKey(possible_location[0], possible_location[1]), "AppDataPath")[0]) / 'Manifests'
        except Exception:
            # the path, or the key, might not exist
            # in this case, we'll just skip over it
            continue

        binary_data = search_for_manifest_file(path)

        if binary_data is not None:
            return Path(binary_data['InstallLocation']) / binary_data['LaunchExecutable']

    # Nothing found in registry? Try C:\ProgramData\Epic\EpicGamesLauncher
    # Or consider using %programdata%
    path = Path(os.getenv("programdata")) / "Epic" / "EpicGamesLauncher" / "Data" / "Manifests"

    if os.path.isdir(path):
        binary_data = search_for_manifest_file(path)

        if binary_data is not None:
            return Path(binary_data['InstallLocation']) / binary_data['LaunchExecutable']


def is_process_running(program, scriptname, required_args: Set[str]) -> Tuple[bool, Optional[psutil.Process]]:
    # Find processes which contain the program or script name.
    matching_processes = []
    for process in psutil.process_iter():
        try:
            p = process.name()
            if program in p or scriptname in p:
                matching_processes.append(process)
        except psutil.NoSuchProcess:
            continue
    # If matching processes were found, check for correct arguments.
    if len(matching_processes) != 0:
        for process in matching_processes:
            try:
                args = process.cmdline()[1:]
                for required_arg in required_args:
                    matching_args = [arg for arg in args if re.match(required_arg, arg, flags=re.IGNORECASE) is not None]
                    # Skip this process because it does not have a matching required argument.
                    if len(matching_args) == 0:
                        break
                else:
                    # If this process has not been skipped, it matches all arguments.
                    return True, process
            except psutil.AccessDenied:
                print(f"Access denied when trying to look at cmdline of {process}!")
        # If we didn't return yet it means all matching programs were skipped.
        raise WrongProcessArgs(f"{program} is not running with required arguments: {required_args}!")
    # No matching processes.
    return False, None

class WrongProcessArgs(UserWarning):
    pass
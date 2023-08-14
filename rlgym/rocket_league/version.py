# From https://github.com/RLBot/RLBot/blob/master/src/main/python/rlbot/version.py
# Store the version here so:
# 1) we don't load dependencies by storing it in __init__.py
# 2) we can import it in setup.py for the same reason
# 3) we can import it into your module
# https://stackoverflow.com/questions/458550/standard-way-to-embed-version-into-python-package

__version__ = '2.0.0-alpha'

release_notes = {
    '2.0.0-alpha':
    """
    - This version contains numerous untested and potentially breaking changes. Run at your own risk.
    """
}


def get_current_release_notes():
    if __version__ in release_notes:
        return release_notes[__version__]
    return ''


def print_current_release_notes():
    print(f"Version {__version__}")
    print(get_current_release_notes())
    print("")
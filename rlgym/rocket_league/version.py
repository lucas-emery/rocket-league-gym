
__version__ = '2.0.0-alpha-2'


def get_current_release_notes():
    if __version__ in release_notes:
        return release_notes[__version__]
    return ''


def print_current_release_notes():
    print(f"Version {__version__}")
    print(get_current_release_notes())
    print("")


release_notes = {
    '2.0.0-alpha-2':
    """
    - This version contains numerous untested and potentially breaking changes. Run at your own risk.
    - Fixed rlviser-py dependency version
    """,
    '2.0.0-alpha-1':
    """
    - This version contains numerous untested and potentially breaking changes. Run at your own risk.
    - Lifted Python <3.10 restriction
    """,
    '2.0.0-alpha':
    """
    - This version contains numerous untested and breaking changes. Run at your own risk.
    """
}

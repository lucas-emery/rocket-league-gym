
__version__ = '2.0.0-alpha-1'


def get_current_release_notes():
    if __version__ in release_notes:
        return release_notes[__version__]
    return ''


def print_current_release_notes():
    print(f"Version {__version__}")
    print(get_current_release_notes())
    print("")


release_notes = {
    '2.0.0-alpha-1':
    """
    - This version contains numerous untested and breaking changes. Run at your own risk.
    - Added shared_info param to TransitionEngine and Renderer
    - Fixed Python <3.9 install
    """,
    '2.0.0-alpha':
    """
    - This version contains numerous untested and breaking changes. Run at your own risk.
    """
}

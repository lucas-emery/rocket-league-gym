
def install_plugin():
    print('Installing plugin')
    try:
        import os
        import sys
        import winreg
        import shutil
        import pkg_resources

        # Get bakkesmod folder
        bm_path = winreg.QueryValueEx(
            winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software\\BakkesMod\\AppPath'), 'BakkesModPath')[0]

        # Install RLGym plugin
        dll_path = pkg_resources.resource_filename('rlgym', 'plugin/RLGym.dll')
        print('dll_path', dll_path)
        shutil.copy2(dll_path, os.path.join(bm_path, 'plugins'))

        # Enable RLGym plugin
        bm_config_path = os.path.join(bm_path, 'cfg/plugins.cfg')
        print('bm_config_path', bm_config_path)
        with open(bm_config_path, 'r') as bm_config:
            content = bm_config.read()
            enabled = 'plugin load rlgym' in content

        print('enabled', enabled)
        if not enabled:
            with open(bm_config_path, 'a') as bm_config:
                bm_config.write('plugin load rlgym\n')
    except:
        raise RuntimeError('Plugin installation failed')

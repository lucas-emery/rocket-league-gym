from setuptools import setup, find_packages
from setuptools.command.install import install


__version__ = None  # This will get replaced when reading version.py
exec(open('rlgym/version.py').read())


with open('README.md', 'r') as readme_file:
    long_description = readme_file.read()


class CustomInstall(install):
    def run(self):
        install.run(self)
        self.install_plugin()

    def install_plugin(self):
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


setup(
    name='rlgym',
    packages=find_packages(),
    version=__version__,
    description='A python API that can be used to treat the game Rocket League as an Openai Gym-like environment for '
                'Reinforcement Learning projects.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Lucas Emery and Matthew Allen',
    url='https://github.com/lucas-emery/rocket-league-gym',
    install_requires=[
        'gym>=0.17',
        'numpy>=1.19',
        'pywin32==228',
        'pywinauto==0.6.8',
        'psutil>=5.8',
    ],
    python_requires='>=3.7,<3.10',
    cmdclass={'install': CustomInstall},
    license='Apache 2.0',
    license_file='LICENSE',
    keywords=['rocket-league', 'gym', 'reinforcement-learning'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        "Operating System :: Microsoft :: Windows",
    ],
    package_data={
        'rlgym': [
            'plugin/*'
        ]
    }
)

from setuptools import setup, find_packages
from setuptools.command.install import install

with open('README.md', 'r') as readme_file:
    long_description = readme_file.read()


class CustomInstall(install):
    def run(self):
        self.do_egg_install()
        self.install_plugin()

    def install_plugin(self):
        print('Installing plugin')
        try:
            import os
            import sys
            import winreg
            import shutil

            # Get bakkesmod folder
            bm_path = winreg.QueryValueEx(
                        winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software\\BakkesMod\\AppPath'), 'BakkesModPath')[0]

            # Install RLGym plugin
            module_path = os.path.dirname(sys.modules['rlgym'].__file__)
            shutil.copy2(os.path.join(module_path, 'plugin/RLGym.dll'),
                         os.path.join(bm_path, 'plugins'))

            # Enable RLGym plugin
            bm_config_path = os.path.join(bm_path, 'cfg/plugins.cfg')
            with open(bm_config_path, 'r') as bm_config:
                content = bm_config.read()
                enabled = 'plugin load rlgym' in content

            if not enabled:
                with open(bm_config_path, 'r') as bm_config:
                    bm_config.write('plugin load rlgym\n')
        except:
            raise RuntimeError('Plugin installation failed')


setup(
    name='rlgym',
    packages=find_packages(),
    version='0.1.0',
    description='A python API that can be used to treat the game Rocket League as an Openai Gym-like environment for '
                'Reinforcement Learning projects.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Lucas Emery and Matthew Allen',
    author_email='lucas.emery@hotmail.com',
    url='https://github.com/lucas-emery/rocket-league-gym',
    install_requires=[
        'gym>=0.17',
        'numpy>=1.19',
        'pywin32==228',
        'pywinauto==0.6.8',
    ],
    cmdclass={'install': CustomInstall},
    license='Apache 2.0',
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
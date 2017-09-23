import subprocess
import sys

from setuptools import setup
from setuptools.command.install import install as _install
from setuptools.command.develop import develop as _develop

def readme():
    with open('README.rst') as f:
        return f.read()

class PostInstallCommand(_install):
    def run(self):
        _install.run(self)
        proc = subprocess.Popen(['bash', 'gopigo3/fw/install.sh'],
                                stdout=subprocess.PIPE,
                                )
        stdout_value = proc.communicate()
        print(sys.argv)

setup(
    name='gopigo3-dev',
    version='0.1.0',

    description='DexterIndustries Library for the GoPiGo3.',
    long_description=readme(),

    author='Robert Lucian CHIRIAC',
    author_email='robert.lucian.chiriac@gmail.com',

    license = 'MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Embedded Systems',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    url='https://github.com/RobertLucian/GoPiGo3-dev',

    keywords=['robot', 'gopigo', 'gopigo3', 'dexter industries', 'learning', 'education'],

    packages=['gopigo3'],
    install_requires=['spidev'],
    include_package_data=True,
    zip_safe=True,
    entry_points=dict(console_scripts=['gopigo3=gopigo3.command_line:main']),
    cmdclass = {
       'install': PostInstallCommand
   },
)

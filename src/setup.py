from setuptools import setup

def readme():
    with open('gopigo3/additional-files/README.rst') as f:
        return f.read()

setup(
    name='travis_package_name',
    version='0.1.0',

    description='Alternative to DexterIndustries\' library for the GoPiGo3.',
    long_description=readme(),

    author='Robert Lucian CHIRIAC',
    author_email='robert.lucian.chiriac@gmail.com',

    license='MIT',
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
    url='https://github.com/RobertLucian/AltGPG3',

    keywords=['robot', 'gopigo', 'gopigo3', 'dexter industries', 'learning', 'education', 'alternative'],

    packages=['altgpg3'],
    package_data={'altgpg3': ['additional-files/*']},
    include_package_data=True,
    install_requires=['spidev', 'RPi.GPIO', 'rst2ansi', 'docutils'],
    entry_points=dict(console_scripts=['altgpg3=altgpg3.command_line:main']),
    zip_safe=True
)

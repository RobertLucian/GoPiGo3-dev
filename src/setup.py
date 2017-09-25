from setuptools import setup

def readme():
    with open('gopigo3/additional-files/README.rst') as f:
        return f.read()

setup(
    name='gopigo3-dev',
    version='0.1.0',

    description='DexterIndustries Library for the GoPiGo3.',
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
    url='https://github.com/RobertLucian/GoPiGo3-dev',

    keywords=['robot', 'gopigo', 'gopigo3', 'dexter industries', 'learning', 'education'],

    packages=['gopigo3'],
    package_data={'gopigo3': ['additional-files/*']},
    include_package_data=True,
    install_requires=['spidev', 'RPi.GPIO'],
    entry_points=dict(console_scripts=['gopigo3=gopigo3.command_line:main']),
    zip_safe=True
)

from setuptools import setup

setup(
    name='Swaybar-Client',
    version='0.0.1',

    install_requires=[
        'importlib',
        'psutil'
    ],

    entry_points={
        'console_scripts': [
            'swaybarclient = swaybarclient:Main',
        ]
    }
)
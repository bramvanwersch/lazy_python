from setuptools import setup

setup(
    name='lazy.py',
    version='0.1',
    packages=['src', '.'],
    url='tbd',
    license='MIT',
    entry_points={
        'console_scripts': [
            'lazy=lazy:main',
        ],
    },
    author='bramv',
    author_email='bramvanwersch@live.nl',
    description='command line idle program'
)

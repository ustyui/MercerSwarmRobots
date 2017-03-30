#from distutils.core import setup #WINDOWS
from setuptools import setup #LINUX

setup (name = 'GooMPy',
    version = '0.1',
    install_requires = ['PIL'],
    description = 'Google Maps for Python',
    packages = ['goompy',],
    license='LGPL',
    platforms='Linux; Windows; OS X'
    )

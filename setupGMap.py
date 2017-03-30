from distutils.core import setup

setup (name = 'GooMPy',
    version = '0.1',
    install_requires = ['PIL'],
    description = 'Google Maps for Python',
    packages = ['goompy',],
    author='Alec Singer and Simon D. Levy',
    author_email='simon.d.levy@gmail.com',
    license='LGPL',
    platforms='Linux; Windows; OS X'
    )
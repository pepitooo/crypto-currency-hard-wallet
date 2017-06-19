from setuptools import find_packages, setup
from qrcnc import *

dependencies = ['pyqrcode']

setup(
    name='qr2cnc',
    packages=find_packages(),
    version='0.0.1',
    url='https://github.com/pepitooo/crypto-currency-hard-wallet',
    license='GNUv3',
    author='Carteaux, Michel',
    author_email=None,
    description='A tool to generate QRCode GCode for cnc',
    long_description=__doc__,
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=dependencies,
    entry_points={
        'console_scripts': [
            'qr2cnc = qrcnc.__main__:main',
        ],
    },
)

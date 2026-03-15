from setuptools import setup, find_packages

with open('requirements.txt') as f:
    install_requires = f.read().strip().split('\n')

from salon_booking import __version__ as version

setup(
    name='salon_booking',
    version=version,
    description='Uber-like salon and beauty services booking platform for Frappe',
    author='Your Name',
    author_email='you@example.com',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
)

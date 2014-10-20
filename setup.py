import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='ceca-pass',
    version='0',
    packages=['ceca_pass'],
    include_package_data=True,
    license='BSD License',
    description='',
    long_description=README,
    url='',
    author='Rodrigo N. Carreras',
    author_email='carrerasrodrigo@gmail.com',
    install_requires=['pycrypto', 'Django>=1.7'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    entry_points={
        'console_scripts': [
            'ceca_pass_dump_to_json=ceca_pass.helpers:dump_to_json',
            'ceca_pass_dump_to_bash=ceca_pass.helpers:dump_to_bash',
            'ceca_pass_patch_bash=ceca_pass.helpers:patch_bash_file'
        ],
    },
)

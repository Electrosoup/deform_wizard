from setuptools import setup, find_packages
import os

version = '0.1'

install_requires = ['deform']

tests_require = ['nose', 'coverage', 'Mock']

here = os.path.abspath(os.path.dirname(__file__))

README = open(os.path.join(here, 'README.txt')).read()

setup(name='deform_wizard',

    version=version,

    description="Form Wizard plugin for Deform",

    long_description=README,

    classifiers=[

        "Intended Audience :: Developers",

        "Programming Language :: Python",

        "Programming Language :: Python :: 2.6",

        "Programming Language :: Python :: 2.7",

        "Programming Language :: Python :: Implementation :: CPython",

    ],

    keywords='web wsgi deform forms form',

    author='Simon Oram',

    author_email='simon@electrosoup.co.uk',

    url='http://github.com/Electrosoup',

    license='GPL',

    packages=find_packages(),

    include_package_data=True,

    zip_safe=False,

    tests_require=tests_require,

    install_requires=install_requires,

    test_suite="deform_wizard",

    extras_require={

        'testing': tests_require

        },

    entry_points="""
    """,
    )

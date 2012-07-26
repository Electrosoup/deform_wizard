from setuptools import setup, find_packages

version = '0.1'

install_requires = [
    'deform'
    ]

setup(name='deform_wizard',
    version=version,
    description="Form Wizard plugin for Deform",
    long_description="""\
""",
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Framework :: Pyramid",
    ],
    keywords='web wsgi deform forms form pyramid',
    author='Simon Oram',
    author_email='simon@electrosoup.co.uk',
    url='http://github.com/Electrosoup',
    license='GPL',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    entry_points="""
    # -*- Entry points: -*-
    """,
    )

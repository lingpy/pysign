from setuptools import setup, find_packages


setup(
    name='pysign',
    version='0.1.0.dev0',
    license='Apache 2.0',
    description='Python library for manipulating sign language data',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    author='Justin Power and Johann-Mattis List',
    author_email='list@shh.mpg.de',
    url='https://github.com/lingpy/pysign',
    keywords='data',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    python_requires='>=3.5',
    install_requires=[
        'clldutils>=3.5', 'tabulate'
    ],
    extras_require={
        'dev': ['flake8', 'wheel', 'twine'],
        'test': [
            'mock',
            'pytest>=4.3',
            'pytest-mock',
            'pytest-cov',
            'coverage>=4.2',
        ],
    },
    entry_points={
        'console_scripts': [
        ]
    },
)


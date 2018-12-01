from setuptools import setup, find_packages
from jumo_csv_groupby._version import __version__

setup(
    name='jumo-csv-groupby',
    version=__version__,
    description="Technical exercise for the JUMO interview process",
    long_description=open("README.md").read(),
    classifiers=[
        "Programming Language :: Python"
    ],
    keywords='python jumo csv groupby',
    author='Kari',
    author_email='karischoonbee@gmail.com',
    url='https://github.org/karischoonbee/jumo-csv-groupby',
    license='WTFPL',
    packages=find_packages(),
    package_data={
        "": ['version.properties'],
    },
    include_package_data=True,
    zip_safe=False,
    install_requires=['setuptools'] + [x.strip() for x in open('requirements.txt').readlines()],
    entry_points="""\
            [console_scripts]
            csv = jumo_csv_groupby.src.cli:csv
        """,
    scripts=[],
)

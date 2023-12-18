
import pathlib
from setuptools import setup, find_packages
 
HERE = pathlib.Path(__file__).parent.resolve()

setup(name='bitopro-client',
    version='1.0.3',
    description='For BitoPro crypto currency exchange written in Python',
    url='https://github.com/bitoex/bitopro-api-python.git',
    author='Bitoex',
    author_email='support@bitopro.com',
    license='MIT',
    packages=['bitoproClient'],
    python_requires = ">=3.7",
    classifiers=[f"Programming Language :: Python :: 3.{str(v)}" for v in range(7, 12)]
    
)
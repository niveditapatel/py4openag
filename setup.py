import setuptools
from setuptools import setup
import io
import os
import re

with open("README.md", "r") as fh:
    long_description = fh.read()

def read(path, encoding='utf-8'):
    path = os.path.join(os.path.dirname(__file__), path)
    with io.open(path, encoding=encoding) as fp:
        return fp.read()

def version(path):
    version_file = read(path)
    version_match = re.search(r"""^__version__ = ['"]([^'"]*)['"]""",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(name='pylenm',
      version=version('pylenm/__init__.py'),
      description='This package aims to ...',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/niveditapatel/py4openag',
      author='Nivedita Patel',
      author_email='patelnivedita@icloud.com',
      license='MIT',
      packages=setuptools.find_packages(),
      install_requires=[
        'markdown',
        'pandas',
        'openpyxl',
        'elevation',
        'richdem',
        'rasterio',
        'numpy',
        'seaborn',
        'matplotlib',
        'statsmodels',
        'scipy',
        'pyproj',
        'datetime',
        'sklearn',
        'supersmoother',
        'ipyleaflet>=0.13.0',
        'ipywidgets>=7.5.0'
        ],
      classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        ],
      python_requires='>=3.6',
      zip_safe=False)
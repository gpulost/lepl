#!/usr/local/bin/python3.0

from setuptools import setup, find_packages

setup(name='LEPL',
      version='0.1',
      description='A Parser Library for Python 3',
      author='Andrew Cooke',
      author_email='andrew@acooke.org',
      url='http://www.acooke.org/lepl/',
      packages=find_packages(),
      license = "LGPL",
      keywords = "parser",
      classifiers=['Development Status :: 2 - Pre-Alpha',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
                   'Natural Language :: English',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python :: 3.0',
                   'Topic :: Software Development',
                   'Topic :: Software Development :: Libraries',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                   'Topic :: Text Processing',
                   'Topic :: Text Processing :: Filters',
                   'Topic :: Text Processing :: General',
                   'Topic :: Utilities'
                   ]
     )
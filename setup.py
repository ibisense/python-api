from setuptools import setup

setup(name='ibisense-api-python',
      version='0.0.1',
      description="Ibisense core API wrapper",
      long_description="This is the  pythonic wrapper library for the Ibisense API.",
      url='http://ibisense.com/',
      packages=['ibisense'],
      install_requires=[
          'requests >= 1.1.0',
      ],
      zip_safe=False)

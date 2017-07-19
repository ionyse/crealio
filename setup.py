import codecs
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))


def read_file(filename):
    """Open a related file and return its content."""
    with codecs.open(os.path.join(here, filename), encoding='utf-8') as f:
        content = f.read()
    return content


README = read_file('README.rst')
CHANGELOG = read_file('CHANGELOG.rst')
CONTRIBUTORS = read_file('CONTRIBUTORS.rst')

REQUIREMENTS = [
    'Django',
]

DEPENDENCY_LINKS = [
]

ENTRY_POINTS = {
}


setup(name='crealio',
      version='2.0.0.dev0',
      description='A Django application that let you handle Curriculum Vitae',
      long_description="{}\n\n{}\n\n{}".format(README, CHANGELOG, CONTRIBUTORS),
      license='Apache License (2.0)',
      classifiers=[
          "Programming Language :: Python",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: Implementation :: CPython",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
          "License :: OSI Approved :: Apache Software License"
      ],
      keywords="web curriculum vitae services",
      author='Ionyse',
      author_email='contact@ionyse.com',
      url='https://github.com/ionyse/crealio',
      packages=find_packages(),
      package_data={'': ['*.rst', '*.py', '*.yaml']},
      include_package_data=True,
      zip_safe=False,
      install_requires=REQUIREMENTS,
      test_suite="tests",
      dependency_links=DEPENDENCY_LINKS,
      entry_points=ENTRY_POINTS)

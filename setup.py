from setuptools import setup, find_packages

setup(name='vericfg',
      version='0.0.1',
      description='vericfg: Parameter Configuration Manager that organizes '+\
                  'parameters with string keys and supports default values, '+\
                  'setting value restrictions, and insuring that restrictions '+\
                  'do not conflict between multiple calls.',
      url='https://github.com/StephenMal/vericfg',
      author='Stephen Maldonado',
      author_email='vericfg@stephenmal.com',
      packages=find_packages(),
      install_requires=[],
      extras_require={},
      classifiers=['Development Status :: 1 - Planning',
                   'Programming Language :: Python :: 3 :: Only',
                   'Topic :: Utilities']
)

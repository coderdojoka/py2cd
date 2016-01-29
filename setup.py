from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='py2cd',
      version='0.3.2',
      description='Wrapper for pygame to provide a simple drawing and gaming framework in German.'
                  ' This project is developed for the use in the CoderDojo Karlsruhe.',
      url='http://github.com/coderdojoka/py2cd',
      author='Mark Weinreuter (CoderDojo Karlsruhe), pygameui (https://github.com/fictorial/pygameui)',
      packages=['py2cd', 'py2cd.pygameui', 'py2cd.erweiterungen', 'py2cd.erweiterungen.jnr'],
      package_data={'py2cd': ['pygameui/resources/*/*','resourcen/bilder/*.png', 'resourcen/bilder/*/*.png', 'resourcen/bilder/*/*/*.png', 'resourcen/animationen/*']},
      install_requires=[
          'pygame'
      ],
      test_suite="tests",
      zip_safe=False)

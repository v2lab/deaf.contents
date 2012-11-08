from setuptools import setup, find_packages
import os

version = '0.1dev'

setup(name='deaf.contents',
      version=version,
      description="Installable content and templates for DEAF 2012",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='Infrae',
      author_email='info@infrae.com',
      url='https://svn.v2.nl/plone/deaf.contents/',
      license='GPL',
      package_dir={'': 'src'},
      packages=find_packages('src'),
      namespace_packages=['deaf'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'Products.Maps',
        'Products.Person',
        'archetypes.clippingimage',
        'collective.contentleadimage',
        'five.grok',
        'setuptools',
        'zeam.utils.batch',
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )

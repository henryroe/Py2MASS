from setuptools import setup

setup(name='Py2MASS',
      version='0.1.2',
      description='Routines for accessing a self-hosted local copy of the 2MASS point-source and extended source catalogs (PSC, XSC)',
      long_description=open('README.md').read(),
      author='Henry Roe',
      author_email='hroe@hroe.me',
      url='https://github.com/henryroe/Py2MASS',
      license='LICENSE.txt',
      data_files=[('format_descriptors/', ['format_descriptors/psc_format_descriptor.csv',
                                           'format_descriptors/xsc_format_descriptor.csv'])],
      py_modules=['py2mass', 'py2mass_process_original_psc'],
      scripts=['py2mass'],
      install_requires=['pandas>=0.10.1'])

import setuptools


version = '0.0.0'

console_scripts = ['maskimage=earthmasker.bin.maskimage:main']

packages = ['earthmasker',
            'earthmasker.lib',
            'earthmasker.bin',
            'earthmasker.gui',
            'earthmasker.gui.ui',
            'earthmasker.lib.load',
            'earthmasker.lib.trainingData']

requires = ['numpy>1.12.0',
            'scipy>0.19.0',
            'matplotlib>2.0.0',]

setuptools.setup(name='earthmasker',
      version='0.0',
      description='scripts for image masking',
      author='Andrew Hoffman',
      author_email='hoffmaaow@uw.edu',
      url='http://github.com/hoffmaao/earthmasker',
      packages=packages,
      install_requires=requires,
      entry_points = {'console_scripts': console_scripts}
     )
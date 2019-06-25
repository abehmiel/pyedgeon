from distutils.core import setup
setup(
      name = 'pyedgeon',
      packages = ['pyedgeon'],
      version = '0.1',
      license='MIT',
      description = 'Create optical illusion buttons',
      author = 'Abraham Hmiel',
      author_email = 'abehmiel@gmail.com',
      url = 'https://github.com/abehmiel/pyedgeon',
    download_url = 'https://github.com/abehmiel/pyedgeon/archive/0.2.tar.gz',
      keywords = ['Optical Illusion', 'PIL', 'Graphics', 'Text'],
      install_requires=[
                        'pillow',
                        ],
      classifiers=[
              'Development Status :: 4 - Beta',
              'Topic :: Software Development :: Build Tools',
              'License :: OSI Approved :: MIT License',
              'Programming Language :: Python :: 3.4',
              'Programming Language :: Python :: 3.5',
              'Programming Language :: Python :: 3.6',
            ],
)

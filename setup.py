from distutils.core import setup
setup(
  name = 'gravityfield',
  packages = ['gravityfield'],
  version = '0.1',
  license='MIT',
  description = 'Calculate the relative acceleration field for celestial bodies in a rotating reference frame',
  author = 'Nestor Fabian Villar',
  author_email = 'nesfvillar@gmail.com',
  url = 'https://github.com/user/gravityfield',
  download_url = 'https://github.com/nesfvillar/gravityfield/archive/refs/tags/v_01.tar.gz',
  keywords = ['science, orbit, celestial, mechanics, rocket'],
  install_requires=[
          'numpy',
          'plotly',
      ],
  classifiers=[  # Optional
    # How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 3 - Alpha',

    # Indicate who your project is intended for
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',

    # Pick your license as you wish
    'License :: OSI Approved :: MIT License',

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 3',
  ],
)
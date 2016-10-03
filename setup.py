from distutils.core import setup

setup(
    name='corsika_wrapper',
    version='1.0.0',
    description='Call CORSIKA in a thread safe and comfortable way.',
    url='https://github.com/fact-project/corsika_wrapper.git',
    author='Sebastian Achim Mueller',
    author_email='sebmuell@phys.ethz.ch',
    license='MIT',
    packages=[
        'corsika_wrapper',
    ],
    install_requires=[
        'docopt'
    ],
    entry_points={'console_scripts': [
        'corsika = corsika_wrapper.__init__:main',
    ]},
    zip_safe=False,
)

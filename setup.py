from distutils.core import setup

setup(
    name='corsika_caller',
    version='1.0.0',
    description='Call CORSIKA in a thread safe and comfortable way.',
    url='https://github.com/fact-project/corsika_caller.git',
    author='Sebastian Achim Mueller',
    author_email='sebmuell@phys.ethz.ch',
    license='MIT',
    packages=[
        'corsika_caller',
    ],
    install_requires=[
        'docopt'
    ],
    entry_points={'console_scripts': [
        'corsika = corsika_caller.__init__:main',
    ]},
    zip_safe=False,
)

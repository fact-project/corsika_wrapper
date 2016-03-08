from distutils.core import setup

setup(
    name='corsika_iact_caller',
    version='0.0.1',
    description='call the CORSIKA executable with IACT package in a modern and thread safe way',
    url='https://github.com/fact-project/corsika_iact_caller.git',
    author='Sebastian Mueller',
    author_email='sebmuell@phys.ethz.ch',
    license='MIT',
    packages=[
        'corsika_iact_caller',
    ],
    install_requires=[
        'docopt'
    ],
    entry_points={'console_scripts': [
        'corsika_iact = corsika_iact_caller.__init__:main',
    ]},
    zip_safe=False,
)

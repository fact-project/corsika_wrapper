import setuptools
import os

setuptools.setup(
    name='corsika_wrapper',
    version='1.0.1',
    description='Call CORSIKA in a thread safe and comfortable way.',
    url='https://github.com/fact-project/corsika_wrapper.git',
    author='Sebastian Achim Mueller',
    author_email='sebastian-achim.mueller@mpi-hd.mpg.de',
    license='GPL v3',
    packages=[
        'corsika_wrapper',
    ],
    package_data={'corsika_wrapper': [os.path.join('tests', 'resources','*')]},
    install_requires=[
        'docopt',
    ],
    entry_points={'console_scripts': [
        'corsika = corsika_wrapper.main:main',
    ]},
)

import setuptools
import os

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name='corsika_wrapper',
    version='1.0.1',
    description='Call CORSIKA in a thread safe and comfortable way.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/fact-project/corsika_wrapper.git',
    author='Sebastian Achim Mueller',
    author_email='sebastian-achim.mueller@mpi-hd.mpg.de',
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
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Astronomy",
    ],
)

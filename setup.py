from setuptools import setup

ENTRY_POINTS = {
    'console_scripts': [
        'check_omex=archive_tools:main',
        'export_copasi_sedml=export_copasi:main',
    ]
}

setup(
    name='harmony_scripts',
    version='0.0.1',
    packages=[''],
    url='https://github.com/fbergmann/harmony_scripts',
    license='Artistic-2.0',
    author='Frank T. Bergmann',
    author_email='frank.bergmann@bioquant.uni-heidelberg.de',
    description='HARMONY 2021 scripts',
    entry_points=ENTRY_POINTS,
    install_requires=['numpy', 'pandas', 'python-copasi', 'python-libsbml', 'python-libcombine', 'python-libsedml'],
    dependency_links=['github.com/copasi/basico.git/tarball/master#egg=basico'],
)

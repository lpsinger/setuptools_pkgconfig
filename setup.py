from setuptools import setup
import setuptools_pkgconfig

setup(
    name='setuptools_pkgconfig',
    version='0.0.1',
    author='Leo Singer',
    author_email='leo.singer@ligo.org',
    description=setuptools_pkgconfig.__doc__.splitlines()[1],
    long_description=setuptools_pkgconfig.__doc__,
    py_modules=['setuptools_pkgconfig'],
    zip_safe=False,
    entry_points={
        'distutils.commands': [
            'build_clib = setuptools_pkgconfig:build_clib'
        ]
    }
)

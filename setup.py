from setuptools import setup
import setuptools_pkgconfig

setup(
    name='setuptools_pkgconfig',
    version='0.0.1',
    author='Leo Singer',
    author_email='leo.singer@ligo.org',
    description=setuptools_pkgconfig.__doc__.splitlines()[1],
    long_description=setuptools_pkgconfig.__doc__,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Build Tools',
        'Topic :: System :: Software Distribution'
    ],
    py_modules=['setuptools_pkgconfig'],
    zip_safe=False,
    entry_points={
        'distutils.commands': [
            'build_clib = setuptools_pkgconfig:build_clib'
        ]
    }
)

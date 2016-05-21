Setuptools add-on to depend on external libraries located using pkgconfig

Usage:

    from setuptools import setup
    setup(
        ...,
        libraries=[
            # some example library dependencies
            'gsl', {'pkg_config': 'gsl >= 2.0'},
            'fftw3', {'pkg_config': 'fftw3'}
        ],
        setup_requires=['setuptools_pkgconfig']
    )

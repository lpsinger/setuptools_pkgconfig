# Based on https://github.com/healpy/healpy/blob/master/setup.py
# and https://github.com/healpy/healpy/blob/master/run_pykg_config.py

"""
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
"""

if __name__ == '__main__':
    # Helper to run pykg-config, whether it is installed or lives in a zipped egg.
    from setuptools import Distribution
    from pkg_resources import run_script
    requirement = 'pykg-config >= 1.2.0'
    Distribution().fetch_build_eggs(requirement)
    run_script(requirement, 'pykg-config.py')
else:
    import os
    import errno
    import sys
    import shlex
    from subprocess import check_output
    from distutils.command.build_clib import build_clib as _build_clib
    from distutils import log


    class build_clib(_build_clib):
        """Subclass of Distutils' standard build_clib subcommand. Adds support for
        libraries that are installed externally and detected with pkg-config, with
        an optional fallback to build from a local configure-make-install style
        distribution."""

        def __init__(self, dist):
            _build_clib.__init__(self, dist)
            self.build_args = {}

        def env(self):
            """Construct an environment dictionary suitable for having pkg-config
            pick up .pc files in the build_clib directory."""
            # Test if pkg-config is present. If not, fall back to pykg-config.
            try:
                env = self._env
            except AttributeError:
                env = dict(os.environ)

                try:
                    check_output(['pkg-config', '--version'])
                except OSError as e:
                    if e.errno != errno.ENOENT:
                        raise
                    log.warn('pkg-config is not installed, falling back to pykg-config')
                    env['PKG_CONFIG'] = sys.executable + ' ' + __file__
                else:
                    env['PKG_CONFIG'] = 'pkg-config'

                self._env = env
            return env

        def pkgconfig(self, *packages):
            env = self.env()
            PKG_CONFIG = tuple(shlex.split(
                env['PKG_CONFIG'], posix=(os.sep == '/')))
            kw = {}
            index_key_flag = (
                (2, '--cflags-only-I', ('include_dirs',)),
                (0, '--cflags-only-other', ('extra_compile_args', 'extra_link_args')),
                (2, '--libs-only-L', ('library_dirs', 'runtime_library_dirs')),
                (2, '--libs-only-l', ('libraries',)),
                (0, '--libs-only-other', ('extra_link_args',)))
            for index, flag, keys in index_key_flag:
                cmd = PKG_CONFIG + (flag,) + tuple(packages)
                log.debug('%s', ' '.join(cmd))
                args = [token[index:].decode() for token in check_output(cmd, env=env).split()]
                if args:
                    for key in keys:
                        kw.setdefault(key, []).extend(args)
            return kw

        def build_library(self, library, pkg_config, local_source=None, supports_non_srcdir_builds=True):
            return self.pkgconfig(pkg_config)

        def build_libraries(self, libraries):
            # Build libraries that have no 'sources' key, accumulating the output
            # from pkg-config.
            for lib_name, build_info in libraries:
                if 'sources' not in build_info:
                    for key, value in self.build_library(lib_name, **build_info).items():
                        if key in self.build_args:
                            self.build_args[key].extend(value)
                        else:
                            self.build_args[key] = value

            # Use parent method to build libraries that have a 'sources' key.
            _build_clib.build_libraries(self, ((lib_name, build_info)
                for lib_name, build_info in libraries if 'sources' in build_info))

# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Pcms(CMakePackage):
    """FIXME: Put a proper description of your package here."""

    homepage      = "https://github.com/SCOREC/pcms"
    git      = "https://github.com/SCOREC/pcms"
    maintainers = ['jacobmerson','cwsmith']

    #version('0.0.5', tag='v0.0.5') 
    version('0.0.5', commit='12d609cc2622c62b7d43263812fb8403a0a5f6ef')
    version('develop', branch='develop')

    variant('omega-h', default=True, description='enable Omega-h for unstructured meshes')
    variant('client', default=True, description='enable pcms client code')
    variant('server', default=True, description='enable pcms client code')
    variant('tests', default=True, description='enable test cases')

    depends_on('redev@main', when='@develop')
    depends_on('redev@4.3.1:')
    depends_on('kokkos')
    depends_on('omega-h@scorec.10.6.0+kokkos',when="+omega-h")
    depends_on('fftw')
    #depends_on('catch2@2:2.99', when='+tests')
    depends_on('catch2@3:', when='+tests')
    depends_on('perfstubs')

    resource(name='testdata',
            git='https://github.com/SCOREC/wdmapp_testcases',
            branch='master',
            destination='testdata')

    def cmake_args(self):
        args = [
                self.define_from_variant("WDMCPL_ENABLE_OMEGA_H", 'omega-h'),
                self.define_from_variant("WDMCPL_ENABLE_SERVER", 'server'),
                self.define_from_variant("WDMCPL_ENABLE_CLIENT", 'client'),
                self.define_from_variant("BUILD_TESTING", 'tests'),
                self.define('WDMCPL_ENABLE_C', True),
                self.define('WDMCPL_ENABLE_Fortran', True),
                self.define('WDMCPL_TEST_DATA_DIR', self.stage.source_path+'/testdata')
                ]
        return args

    # modify the default behavior in lib/spack/build_systems/cmake.py
    # to not use parallel builds
    def check(self):
        """Searches the CMake-generated Makefile for the target ``test``
        and runs it if found.
        """
        with working_dir(self.build_directory):
            if self.generator == 'Unix Makefiles':
                self._if_make_target_execute('test',
                                             jobs_env='CTEST_PARALLEL_LEVEL',parallel=False)
                self._if_make_target_execute('check',parallel=False)
            elif self.generator == 'Ninja':
                self._if_ninja_target_execute('test',
                                              jobs_env='CTEST_PARALLEL_LEVEL',parallel=False)
                self._if_ninja_target_execute('check',parallel=False)

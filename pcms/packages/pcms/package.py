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
    variant('shared', default=True, description='enable shared library builds')
    variant('fortran', default=True, description='enable fortran interfaces')

    depends_on('redev@main', when='@develop')
    depends_on('redev@4.3.1:',type=('build','link','run'))
    depends_on('kokkos', type=('build','link','run'))
    depends_on('omega-h@scorec.10.6.0+kokkos',when="+omega-h",type=('build','link','run'))
    depends_on('fftw',type=('build','link','run'))
    depends_on('catch2@3:', when='@0.0.6:+tests',type=('build','link','run'))
    depends_on('catch2@2:2.99', when='@:0.0.5+tests',type=('build','link','run'))
    depends_on('perfstubs',type=('build','link','run'))
    depends_on('adios2+fortran@2.7.1:',when="+fortran",type=('build', 'link','run'))

    resource(name='testdata',
            git='https://github.com/jacobmerson/pcms_testcases.git',
            branch='main',
            placement='testdata')

    def cmake_args(self):
        prefix = "PCMS"
        if self.spec.satisfies("@:0.0.5"):
            prefix = "WDMCPL"
        args = [
                self.define_from_variant(f"{prefix}_ENABLE_OMEGA_H", 'omega-h'),
                self.define_from_variant(f"{prefix}_ENABLE_SERVER", 'server'),
                self.define_from_variant(f"{prefix}_ENABLE_CLIENT", 'client'),
                self.define_from_variant("BUILD_TESTING", 'tests'),
                self.define_from_variant("BUILD_SHARED_LIBS", 'shared'),
                self.define(f'{prefix}_ENABLE_C', True),
                self.define_from_variant(f'{prefix}_ENABLE_Fortran', 'fortran'),
                self.define(f'{prefix}_TEST_DATA_DIR', self.stage.source_path+'/testdata')
                ]
        args.append(self.define("perfstubs_DIR",self.spec["perfstubs"].libs.directories[0] + "/cmake" ))
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

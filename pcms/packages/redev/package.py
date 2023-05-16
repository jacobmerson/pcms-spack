# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

class Redev(CMakePackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://scorec.github.io/redev/"
    git      = "https://github.com/SCOREC/redev"

    maintainers = ['jacobmerson','cwsmith']

    # FIXME: Add proper versions and checksums here.
    # version('1.2.3', '0123456789abcdef0123456789abcdef')
    version('4.3.1', tag='v4.3.1')
    version('main', branch='main')

    depends_on('mpi')
    depends_on('adios2@2.7.1:')

    def cmake_args(self):
        args = []
        if 'sst' in self.spec["adios2"]:
            args.append(self.define("ADIOS2_HAVE_SST", True))
        return args

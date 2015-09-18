##
# Copyright 2012-2015 Ghent University
#
# This file is part of EasyBuild,
# originally created by the HPC team of Ghent University (http://ugent.be/hpc/en),
# with support of Ghent University (http://ugent.be/hpc),
# the Flemish Supercomputer Centre (VSC) (https://vscentrum.be/nl/en),
# the Hercules foundation (http://www.herculesstichting.be/in_English)
# and the Department of Economy, Science and Innovation (EWI) (http://www.ewi-vlaanderen.be/en).
#
# http://github.com/hpcugent/easybuild
#
# EasyBuild is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation v2.
#
# EasyBuild is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EasyBuild.  If not, see <http://www.gnu.org/licenses/>.
##
"""
Support for OpenMPI as toolchain MPI library.

@author: Stijn De Weirdt (Ghent University)
@author: Kenneth Hoste (Ghent University)
"""
from distutils.version import LooseVersion

from easybuild.tools.toolchain.constants import COMPILER_VARIABLES, MPI_COMPILER_VARIABLES
from easybuild.tools.toolchain.mpi import Mpi
from easybuild.tools.toolchain.variables import CommandFlagList


TC_CONSTANT_OPENMPI = "OpenMPI"
TC_CONSTANT_MPI_TYPE_OPENMPI = "MPI_TYPE_OPENMPI"


class OpenMPI(Mpi):
    """OpenMPI MPI class"""
    MPI_MODULE_NAME = ["OpenMPI"]
    MPI_FAMILY = TC_CONSTANT_OPENMPI
    MPI_TYPE = TC_CONSTANT_MPI_TYPE_OPENMPI

    MPI_LIBRARY_NAME = 'mpi'

    # version-dependent, see http://www.open-mpi.org/faq/?category=mpi-apps#override-wrappers-after-v1.0
    MPI_COMPILER_MPIF77 = 'mpif77'
    MPI_COMPILER_MPIF90 = 'mpif90'
    MPI_COMPILER_MPIFC = 'mpifc'

    # OpenMPI reads from CC etc env variables
    MPI_SHARED_OPTION_MAP = dict([('_opt_%s' % var, '') for var in MPI_COMPILER_VARIABLES])

    MPI_LINK_INFO_OPTION = '-showme:link'

    def __init__(self, *args, **kwargs):
        """Toolchain constructor."""
        super(OpenMPI, self).__init__(*args, **kwargs)

        ompi_ver = self.get_software_version(self.MPI_MODULE_NAME)
        if LooseVersion(ompi_ver) >= LooseVersion('1.7'):
            self.MPI_COMPILER_MPIF77 = 'mpifort'
            self.MPI_COMPILER_MPIF90 = 'mpifort'
            self.MPI_COMPILER_MPIFC = 'mpifort'
        else:
            self.MPI_COMPILER_MPIF77 = 'mpif77'
            self.MPI_COMPILER_MPIF90 = 'mpif90'
            self.MPI_COMPILER_MPIFC = 'mpif90'

    def _set_mpi_compiler_variables(self):
        """Add OMPI_* variables to set."""

        # this needs to be done first, otherwise e.g., CC is set to MPICC if the usempi toolchain option is enabled
        for var in COMPILER_VARIABLES:
            if isinstance(var, basestring):
                source_var = var
                target_var = var
            else:
                source_var = var[0]
                target_var = var[1]
            var = 'OMPI_%s' % target_var
            self.variables.nappend(var, str(self.variables[source_var].get_first()), var_class=CommandFlagList)

        super(OpenMPI, self)._set_mpi_compiler_variables()

## Different clusters, CPU and GPU

Here is a brief description on how VASP was installed on different clusters. While NSC and many other HPC centers have a center license for providing VASP installations to users with a confirmed license, this is not always the case, e.g. for MeluXina and LUMI. Therefore, it can be of interest to install and test VASP by oneself. The main license holder (or contact person) can download the source code from the [VASP portal](https://www.vasp.at/). 

Detailed descriptions on how to install VASP can be found at the [VASP-wiki](https://www.vasp.at/wiki/index.php/Category:Installation).

Note that the recipes here below might not be the best ways to install VASP (e.g. limitations on available tool-chains and effort levels on benchmarking and optimization), but can be of interest as some practical examples.

### Tetralith

Description on how VASP 6.4.0 was built on [Tetralith](https://www.nsc.liu.se/systems/tetralith/) (regular installation with access during workshop). The regular nodes contain 2x Intel Xeon Gold 6130 CPUs with a total of (2x 16) 32 cores and 96 GB RAM.

Further details of the Tetralith installations are found on the [NSC VASP page](https://www.nsc.liu.se/software/installed/tetralith/vasp/).

The module used in the workshop

    VASP/6.4.0.14022023-omp-nsc1-intel-2018a-eb

was built in this way

    module load buildenv-intel/2018a-eb
    cp arch/makefile.include.intel_omp makefile.include

The changes for Tetralith were 

    ...
               -DMPI -DMPI_BLOCK=65536 -Duse_collective \
    ...
               -DCACHE_SIZE=65536 \
    ...
               -D_OPENMP -DnoSTOPCAR -DLONGCHAR 
    ...
    VASP_TARGET_CPU ?= -xCORE-AVX2
    ...
    FCL        += -mkl
    MKLROOT    ?= 
    ...
    CPP_OPTIONS+= -DVASP_HDF5
    HDF5_ROOT  ?= /software/sse/easybuild/prefix/software/HDF5/1.10.1-intel-2018a-nsc1
    LLIBS      += -L$(HDF5_ROOT)/lib -lhdf5_fortran
    INCS       += -I$(HDF5_ROOT)/include

Running the testsuite which follows VASP, the tests using `ML_ISTART=2` failed. In near future, newer intel compiler tool-chains will be tested. In the mean time, an alternative gnu installation was made. For a test case it was slightly faster by including intel MKL (though slower than the intel build).

    module load buildenv-gcc/2022a-eb
    cp arch/makefile.include.gnu_ompi_mkl_omp makefile.include

The changes were

    ...
               -DMPI -DMPI_BLOCK=65536 -Duse_collective \
    ...
               -DCACHE_SIZE=65536 \
    ...
               -D_OPENMP -DnoSTOPCAR -DLONGCHAR
    ...
    MKLROOT   ?= /software/sse/easybuild/prefix/software/imkl/2018.1.163-iimpi-2018a/mkl
    ...
    SCALAPACK_ROOT ?= /software/sse/easybuild/prefix/software/ScaLAPACK/2.2.0-gompi-2022a-fb
    ...
    CPP_OPTIONS+= -DVASP_HDF5
    HDF5_ROOT  ?= /software/sse/easybuild/prefix/software/HDF5/1.12.2-gompi-2022a-nsc1
    LLIBS      += -L$(HDF5_ROOT)/lib -lhdf5_fortran
    INCS       += -I$(HDF5_ROOT)/include

### MeluXina
An example on how VASP 6.4.0 was built on MeluXina (temporary workshop installation). The regular nodes used in the workshop contain 2x AMD EPYC Rome 7H12 with a total of (2x 64) 128 cores (256 with hyper-threading) and 512 GB RAM. 

    module load foss/2022a
    module load HDF5/1.12.2-gompi-2022a
    cp arch/makefile.include.gnu_omp makefile.include

The changes here were 

    ...
               -DOpenMP -DnoSTOPCAR -DLONGCHAR
    ...
    OPENBLAS_ROOT ?= /apps/USE/easybuild/release/2022.1/software/OpenBLAS/0.3.20-GCC-11.3.0
    ...
    SCALAPACK_ROOT ?= /apps/USE/easybuild/release/2022.1/software/ScaLAPACK/2.2.0-gompi-2022a-fb
    ...
    FFTW_ROOT  ?= /apps/USE/easybuild/release/2022.1/software/FFTW/3.3.10-GCC-11.3.0
    ...
    CPP_OPTIONS+= -DVASP_HDF5
    HDF5_ROOT  ?= /apps/USE/easybuild/release/2022.1/software/HDF5/1.12.2-gompi-2022a
    LLIBS      += -L$(HDF5_ROOT)/lib -lhdf5_fortran
    INCS       += -I$(HDF5_ROOT)/include

Since hyper-threading is switched on by default on MeluXina, we try to run without it, i.e.

    srun --hint=nomultithread -n 8 vasp_std

An intel compiler installation was also tested on MeluXina, though some problems were noted.

### General points

* For heavy computations, look into adjusting `NB`, the blocking factor for distribution of matrices in src/scala.F, to higher value e.g.

      NB=96

* If building for AMD CPUs look into if intel MKL can be used more efficiently, see e.g. [this link](https://danieldk.eu/Posts/2020-08-31-MKL-Zen.html). Note that the procedure might be different depending on intel compiler suite version. Might also set

      export MKL_ENABLE_INSTRUCTIONS=AVX2
      export MKL_CBWR=AVX2

* For `BRMIX` problems for intel builds, might need to set (at runtime)

      export I_MPI_ADJUST_REDUCE=3 

* For better stability of some intel builds, I'm testing to include (at runtime), if built with `-xCORE-AVX2`

      export MKL_CBWR=AVX2 

### GPU example

This is an example on how VASP 6.3.2 was compiled for a benchmark and energy consumption test on [Berzelius](https://www.nsc.liu.se/systems/berzelius/) nodes equipped with Nvidia A100 GPUs (since Berzelius is prioritized for AI and machine learning, it's typically unavailable for regular VASP calculations).

Note that the OpenACC GPU version of VASP is used, the previous CUDA version is no longer maintained.

    module load buildenv-nvhpc/.22.1-cu11.4
    cp arch/makefile.include.nvhpc_acc makefile.include

The changes were taking into account the GPU (Nvidia A100) and CUDA version used

    FC          = mpif90 -acc -gpu=cc80,cuda11.4
    FCL         = mpif90 -acc -gpu=cc80,cuda11.4 -c++libs
    ...
    NVROOT      = /software/sse/manual/nvhpc/22.1-bdist1/Linux_x86_64/22.1
    ...
    OFLAG_IN   = -fast -Mwarperf
    SOURCE_IN  := nonlr.o
    ...
    FFTW_ROOT  ?= /software/sse/manual/FFTW/3.3.9/g83/nsc1
    LLIBS      += $(FFTW_ROOT)/lib/libfftw3.a

For running e.g. on two GPUs, the job script looks like

    #!/bin/bash
    ...
    #SBATCH --gpus=2

    module load buildenv-nvhpc/.22.1-cu11.4
    OMP_NUM_THREADS=1 srun --mpi=pmix -n 2 ./vasp_start.swrap

calling a wrapper script which contains the path to the binary

    #!/bin/bash
    export CUDA_VISIBLE_DEVICES=$SLURM_LOCALID
    /path/to/installation/vasp_std


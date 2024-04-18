## For using LEONARDO (EuroHPC)

Note that the hands-on part was adjusted to LEONARDO from Tetralith (and previous workshops), so there are some differences.

### User account and login

See links sent out to the workshop participants for all information.

### General information
There is some detailed [LEONARDO user documentation available here](https://wiki.u-gov.it/confluence/display/SCAIUS/HPC+User+Guide).

### Running jobs
In each example for the hands-on part of the workshop, there's a job script available called "run.sh". The job script is submitted to the slurm job queue with

    sbatch run.sh

one can check its progress with the command

    squeue -u USERNAME

### Example job script
Typically, the workshop job scripts prepared for running on LEONARDO looks like this

    #!/bin/bash
    #SBATCH -A EUHPC_TD02_030
    #SBATCH -p boost_usr_prod
    #SBATCH --qos=boost_qos_dbg
    #SBATCH --time 00:15:00
    #SBATCH -n 8
    #SBATCH --ntasks-per-node=8
    #SBATCH --cpus-per-task=1
    #SBATCH --job-name=vaspjob

    module use /leonardo_scratch/fast/EUHPC_TD02_030/vasp_ws2024/modules
    module load VASP/6.4.3-cpu1
    module load intel-oneapi-compilers/2023.2.1
    module load intel-oneapi-mpi/2021.10.0
    module load intel-oneapi-mkl/2023.2.0
    module load hdf5/1.14.3--intel-oneapi-mpi--2021.10.0--oneapi--2023.2.0

    export SRUN_CPUS_PER_TASK=$SLURM_CPUS_PER_TASK
    export OMP_NUM_THREADS=1

    srun vasp_std

since the examples are selected to be small and fast, only a few CPU cores (-n 8) on a LEONARDO boost partition node (in total 32 cores and 4 GPUs) is used.

"module use" is for activating modules which were created for the present workshop, e.g. for VASP. Note that the modules used for building VASP on LEONARDO needs to be loaded (on Tetralith, it's sufficient to load the VASP module). 

While OpenMP was included in the present build, OMP_NUM_THREADS=1 is set since hybrid MPI/OpenMP calculations are not used in the examples.

A basic analysis of the output can be done directly on the LEONARDO cluster, e.g. with gnuplot and py4vasp, further analysis can be made on a local computer. For instance, visualizing the structures with VESTA and running p4vasp and py4vasp (via jupyter-lab).

## More examples and topics 

If you want further examples or prefer to select ones depending on your topic of interest, have a look at 

* The [VASP wiki](https://www.vasp.at/wiki/index.php/The_VASP_Manual) for [examples](https://www.vasp.at/wiki/index.php/Category:Examples) and [tutorials](https://www.vasp.at/wiki/index.php/Category:Tutorials)

* For [py4vasp](https://www.vasp.at/py4vasp/latest/) there are also [tutorials available](https://www.vasp.at/tutorials/latest/)

There are many more topics available, not covered by the present hands-on examples. By comparing with the adjusted examples in this workshop, it is possible to modify the above material for running on Tetralith and other clusters.

* If one is interested in applying **machine learning force fields**, there is an example for [liquid Si](https://www.vasp.at/wiki/index.php/Liquid_Si_-_MLFF).

* It is now possible to compute **X-ray absorption spectra** with VASP, see this example for [XANES in diamond](https://www.vasp.at/wiki/index.php/XANES_in_Diamond).

Note that the hands-on sessions in this workshop are **not** suitable for heavier computational jobs, though it's fine for testing and looking into running different types of VASP calculations. 

### Select material for study

You might start from a system of your choice and perform a similar analysis as for the examples presented in this workshop and at the VASP wiki. An idea might be to search for the material at the [Crystallography Open Database](https://www.crystallography.net/cod/) and transform the .cif file to POSCAR, using cif2cell

    cif2cell filename.cif -p vasp

In the produced POSCAR file, it's useful to add the species in a new 6th line below the lattice vectors (the correct ordering is printed in the top line), so that it can readily be used for visualization with e.g. VESTA.

### Trying different tools

There are many useful tools which are available for VASP, e.g. for post-processing or setting up structures. Depending on your interest, you can select some of the ones described in the [section on useful tools](../tools), also see the last presentation, "Utilities & Summary".

### Running on GPUS at LEONARDO

There is also a VASP OpenACC GPU build for the workshop which can be used for running calculations. Below is an example job script for running on a single GPU (since each Booster node got 32 cores and 4 GPUs, we select 8 cores with each GPU)

    #!/bin/bash
    #SBATCH -A EUHPC_TD02_030
    #SBATCH -p boost_usr_prod
    #SBATCH --qos=boost_qos_dbg
    #SBATCH --time 00:15:00
    #SBATCH -n 8
    #SBATCH --gres=gpu:1
    #SBATCH --job-name=vaspjob

    module use /leonardo_scratch/fast/EUHPC_TD02_030/vasp_ws2024/modules
    module load VASP/6.4.3-gpu1
    module load nvhpc/23.11   
    module load fftw/3.3.10--openmpi--4.1.6--nvhpc--23.11  
    module load hdf5/1.14.3--openmpi--4.1.6--nvhpc--23.11
    module load netlib-scalapack/2.2.0--openmpi--4.1.6--nvhpc--23.11

    srun -n 1 vasp_std


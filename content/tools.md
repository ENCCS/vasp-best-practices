## Useful tools

Some of the tools are also described in the examples. For an easy overview, a description is collected on this page. There are many more tools which can be used, a selection is shown in the last part of the presentations (Utilities & Summary).

`````{callout} System-specific instructions
Select instructions for the system you are using:
 ````{tabs}
  ```{group-tab} Tetralith
Instructions for use on the NAISS cluster Tetralith (NSC)
  ```
  ```{group-tab} MeluXina
Instructions for use on the EuroHPC cluster MeluXina 
  ```
 ````
`````

### Command line

Basic experience with common Unix/Linux commands such as

    ls, cd, cp, mv, mkdir, rm

it is also very useful to handle

    grep, less, cat

Can quickly look into their manual in a terminal, e.g. by typing

    man grep

### Text editors

There are many text editors which can be used directly in a terminal, such as `vi`, `emacs` and `nano`. In a virtual desktop environment several more are available, e.g. `gedit` on Tetralith via ThinLinc. Pick the one you prefer. There are lot of guides available online.

A very brief guide to vi (vim)

    vi filename   # open the file "filename"
    i             # switch to interactive mode, used for typing, close with `esc`
    `esc`         # needed to close interactive mode
    :w            # save
    :wq           # save and quit
    :q!           # quit without saving
    r             # replace character
    x             # delete character
    u             # undo
    G             # go to end of file
    gg            # go to beginning of file
    .             # repeat last command
    dd            # delete one line
    yy            # copy (yank) line
    p             # put line which was copied

a number X before a command will repeat it X times. On Tetralith/MeluXina arrow keys can be used to move around in the file.
 
### Gnuplot

[gnupot](http://www.gnuplot.info/) is a common tool for plotting data and is readily available on most systems. It's also possible to directly save a plot to an image.

 ````{tabs}
  ```{group-tab} Tetralith
      module load gnuplot/5.2.2-nsc1
  ```
  ```{group-tab} MeluXina
      module load gnuplot/5.4.4-GCCcore-11.3.0 
  ```
 ````

typing

    gnuplot

will give a gnuplot prompt in the terminal `gnuplot>`. To directly plot to a png image e.g.

    set term png
    set output "image.png"

### p4vasp

[p4vasp](https://github.com/orest-d/p4vasp) is an open source visualization tool for VASP, with a wide range of functions (e.g. plotting DOS, bandstructure, energy and force convergence, structure relaxation). At this time it's [official webpage](https://www.p4vasp.at/) seems to be down.

 ````{tabs}
  ```{group-tab} Tetralith
  p4vasp is installed on Tetralith

      module load p4vasp/0.3.30-nsc1
      p4v &
  ```
  ```{group-tab} MeluXina
  p4vasp is not available as a regular installation, but is possible to run from a provided singularity image on MeluXina. First, connect with

      ssh -Y meluxina

  to get a compute node with X11 forwarding, start interactive job, thereafter run singularity

      salloc -A p200051 -p cpu --qos default -N 1 -t 1:00:00 bash -c 'ssh -Y $(scontrol show hostnames | head -n 1)'

      /apps/USE/easybuild/release/2022.1/software/Singularity-CE/3.10.2-GCCcore-11.3.0/bin/singularity  run -B /project/home/p200051  /project/home/p200051/singularity/p4.simg

  At the `Singularity>` prompt, start with

      p4v
  ```
 ````

### py4vasp

[py4vasp](https://www.vasp.at/py4vasp/latest/) is a python interface which extracts data from a VASP calculation, using the HDF5 `.h5` output file (meaning that VASP needs to be compiled with HDF5 support). It can be used e.g. to quickly plot density of states, bandstructure and energy convergence. It's optimized for use together with jupyter-lab and jupyter-notebook.

After starting a Python kernel which includes py4vasp via jupyter, in the notebook one first loads py4vasp and thereafter sets where to find the finished VASP calculation of interest

    import py4vasp
    mycalc = py4vasp.Calculation.from_path("/path/to/your/calculation/folder/here")

alternatively, one can provide the direct path to the VASP `.h5` output file

    mycalc = py4vasp.Calculation.from_file("/path/to/your/file/vaspout.h5")

Here below a few examples are shown. For a much more detailed description, refer to the [py4vasp page](https://www.vasp.at/py4vasp/latest/) and also see some [example of tutorials using py4vasp from the VASP developers](https://www.vasp.at/tutorials/latest/).

Examples for plotting density of states (DOS)

    mycalc.dos.plot()              # plot total DOS
    mycalc.dos.plot("s,p,d")       # plot s, p and d orbitals
    mycalc.dos.plot("3(s)"))       # plot s orbital of atom 3 in POSCAR
    mycalc.dos.plot("s(Na, Cl")    # plot s orbital for Na and Cl  
    mycalc.dos.plot("down(1:3)")   # plot spin-down for atoms 1 to 3 in POSCAR combined

Plotting the bandstructure

    mycalc.band.plot()

Showing the POSCAR structure in 3D

    mycalc.structure.plot()

Plotting the energy convergence

    mycalc.energy[:].plot()       # plot the full energy range
    mycalc.energy[5].plot()       # plot at step 5
    mycalc.energy[1:10].plot()    # plot between steps 1 and 10

 ````{tabs}
  ```{group-tab} Tetralith
  You can install py4vasp in a Python virtual environment, for example

      ml Python/3.10.4-env-nsc1-gcc-2022a-eb buildenv-gcc/2022a-eb 
      virtualenv --system-site-packages mypy4venv
      source mypy4venv/bin/activate
      pip install py4vasp

  To logout from the virtual environment, type

      deactivate
  ```
  ```{group-tab} MeluXina
  For instructions on how to setup py4vasp, [refer to the MeluXina starting page](../meluxina)

  ```
 ````

### ASE

[The Atomic Simulation Environment (ASE)](https://wiki.fysik.dtu.dk/ase/) is a set of tools and Python modules for setting up, manipulating, running, visualizing and analyzing atomistic simulations. It can be used together with VASP and many other programs.

In this workshop it's used to help compute the equation of state in some of the examples.

 ````{tabs}
  ```{group-tab} Tetralith
  To use ASE, load its module together with a suitable Python installation e.g.

      module load ASE/3.21.0-nsc1
      module load Python/3.10.4-env-nsc1-gcc-2022a-eb
  ```
  ```{group-tab} MeluXina
  ASE is directly available from the py4vasp Python virtual environment
  ```
 ````

### cif2cell

[cif2cell](https://github.com/torbjornbjorkman/cif2cell) is a tool for generating input structures (e.g. POSCAR) for electronic structure codes (e.g. VASP) starting from a CIF file. 

For example, it can be very useful if you start from an experimental structure reported in the [Crystallograpohy Open Database](https://www.crystallography.net/cod/) which uses the CIF format. If you have a different structure format which can be converted to CIF, you can use cif2cell to produce POSCAR as a second step.

 ````{tabs}
  ```{group-tab} Tetralith
  It is availble as a module

      module load cif2cell/1.2.10-nsc1
      cif2cell --help
  ```
  ```{group-tab} MeluXina
  It can be installed, follow instructions on its github page
  ```
 ````

### VESTA

[VESTA](https://jp-minerals.org/vesta/en/) is a 3D visualization program for structural models, volumetric data such as electron/nuclear densities, and crystal morphologies.

It's available for Windows, Mac and Linux. Free of charge for non-commercial users.

 ````{tabs}
  ```{group-tab} Tetralith
  It is available as a module

      module load vesta/3.4.4-nsc1
      vesta &
  ```
  ```{group-tab} MeluXina
  VESTA is not available as a regular installation, but is possible to run from a provided singularity image on MeluXina. First, connect with

      ssh -Y meluxina

  to get a compute node with X11 forwarding, start interactive job, thereafter run singularity

      salloc -A p200051 -p cpu --qos default -N 1 -t 1:00:00 bash -c 'ssh -Y $(scontrol show hostnames | head -n 1)'

      /apps/USE/easybuild/release/2022.1/software/Singularity-CE/3.10.2-GCCcore-11.3.0/bin/singularity  run -B /project/home/p200051  /project/home/p200051/singularity/vesta.sif
  ```
 ````

### Jupyter-notebook and jupyter-lab

In brief, jupyter-notebook is a web-based interactive document which can be shared. For example, it can be used to run Python. Jupyter-lab is an extensive interface which includes jupyter-notebook.

The main page is in [this link](https://jupyter.org/). Also see [documentation](https://docs.jupyter.org/en/latest/index.html).

 ````{tabs}
  ```{group-tab} Tetralith
  Jupyter-notebook is typically available within the Python env installations on Tetralith. For example

      module load Python/3.10.4-env-nsc1-gcc-2022a-eb

  confirm e.g. with

      pip list | grep -i jupyter

  A different possibility is to install it using conda or a Python virtual environment, see the [NSC Python page](https://www.nsc.liu.se/software/python/) for more details. Also see the material from the latest [NSC introduction 

  ```
  ```{group-tab} MeluXina
  For using jupyter-notebook in the hands-on exercises, [refer to the MeluXina starting page](../meluxina). In more general for MeluXina, [refer to the documentation](https://docs.lxp.lu/).

  It is also possible to start a job directly as a [jupyter-lab session on MeluXina](https://docs.lxp.lu/cloud/jlab/jlab/), though at the moment it doesn't work together with py4vasp.
  ```
 ````

## Useful tools

Some of the tools are also described in the examples. For an easy overview, a description is collected on this page. There are many more tools which can be used, a selection is shown in the 4th and last presentation, "Utilities & Summary".

In general, Tetralith is well suitable for post-processing directly on the login node, or using work nodes for more heavy processing, via the ThinLinc virtual desktop. 

On LEONARDO, test to use py4vasp together with jupyter-lab via port forwarding to your local computer, alternatively produce static images. Gnuplot and vaspkit can also be used to produce images. It is also possible to install many of the tools on a local computer for post-processing of the output, e.g. VESTA is usually easy to install.


`````{callout} System-specific instructions
Select instructions for the system you are using:
 ````{tabs}
  ```{group-tab} Tetralith
Instructions for use on the NAISS cluster Tetralith (NSC)
  ```
  ```{group-tab} LEONARDO
Instructions for use on the EuroHPC cluster LEONARDO
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

a number X before a command will repeat it X times. On Tetralith/LEONARDO arrow keys can be used to move around in the file.

### tmux

tmux can be useful for running several terminal sessions e.g. within one login if connecting via ssh. There are many guides available online. A very brief outline below:

    tmux             # start
    tmux ls          # list sessions
    tmux attach      # reactivate
    ctrl b c         # create new window
    ctrl b n         # step between windows
    ctrl b d         # deactivate

### Gnuplot

[gnupot](http://www.gnuplot.info/) is a common tool for plotting data and is readily available on most systems. It's also possible to directly save a plot to an image.

It is available in the path on both clusters (if a specific version is needed, it can be searched after with "module avail gnuplot").

Typing

    gnuplot

will give a gnuplot prompt in the terminal `gnuplot>`. To directly plot to a png image e.g.

    set term png
    set output "image.png"

you can also get a quick ASCII sketch of a plot in the terminal by setting

    set term dumb

before a plot command.

### Python

In general, Python can be very useful both for smaller basic analysis scripts and in the form of more involved software such as e.g. ASE and py4vasp (see below).

It's a good idea to **keep different programs separate** (unless they're meant to be used together), such that their dependencies aren't mixed in a common environment, e.g. as packages installed in a user home account under `.local`. A typical issue is that different software can be sensitive to exact versions of dependencies. Therefore, one can look into creating Python virtual environments and/or using conda or its drop-in replacement mamba, to keep environments separate. For Tetralith, check the following pages for handling [Python](https://www.nsc.liu.se/software/python/) and [conda/mamba](https://www.nsc.liu.se/software/anaconda/).

### p4vasp

[p4vasp](https://github.com/orest-d/p4vasp) is an open source visualization tool for VASP, with a wide range of functions (e.g. plotting DOS, bandstructure, energy and force convergence, structure relaxation). At this time it's [official webpage](https://www.p4vasp.at/) seems to be down.

 ````{tabs}
  ```{group-tab} Tetralith
  p4vasp is installed on Tetralith

      module load p4vasp/0.3.30-nsc1
      p4v &
  ```
  ```{group-tab} LEONARDO
  p4vasp is not available
  ```
 ````

### py4vasp

[py4vasp](https://www.vasp.at/py4vasp/latest/) is a python interface which extracts data from a VASP calculation, using the HDF5 `.h5` output file (meaning that VASP needs to be compiled with HDF5 support). It can be used e.g. to quickly plot density of states, bandstructure and energy convergence. It's optimized for use together with jupyter-lab and jupyter-notebook, but can also output image files directly.

After starting a Python kernel which includes py4vasp via jupyter, in the notebook one first loads py4vasp and thereafter sets where to find the finished VASP calculation of interest

    import py4vasp
    mycalc = py4vasp.Calculation.from_path("/path/to/your/calculation/folder/here")

alternatively, one can provide the direct path to the VASP `.h5` output file

    mycalc = py4vasp.Calculation.from_file("/path/to/your/file/vaspout.h5")

or go to the folder in the notebook via

    cd /path/to/your/calculation/folder/here
    mycalc = py4vasp.Calculation.from_path(".")

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
  py4vasp is available via a module

      module load py4vasp/0.7.4-hpc1

  by loading it also python, ASE, numpy, jupyter and many other packages become available. See all with "pip list". See below for how to directly write an image file. See the last section for starting jupyter-lab, from which py4vasp can be run in the browser. 
  ```
  ```{group-tab} LEONARDO
  py4vasp is available via a Python module prepared for the workshop

      module use /leonardo_scratch/fast/EUHPC_TD02_030/vasp_ws2024/modules 
      module load pythonws-env/1.0-hpc1

  by loading it also python, ASE, numpy, jupyter and many other packages become available. See all with "pip list". See below for how to directly write an image file. See the last section for starting jupyter-lab, from which py4vasp can be run in the browser.

  ```
 ````
**Note that py4vasp can also be used directly in a python script, writing output to an image file instead of a plot via jupyter**.

For example, a script "py4dos.py"

    import py4vasp
    mycalc = py4vasp.Calculation.from_path(".")
    mycalc.dos.to_image("s,p,d")

activate a Python environment including py4vasp, and run with

    python py4dos.py

this will output a DOS image "dos.png".

Another example for a band structure plot "py4band.py"

    import py4vasp
    mycalc = py4vasp.Calculation.from_path(".")
    mycalc.band.to_image()

this will give a band-structure image "band.png".

### ASE

[The Atomic Simulation Environment (ASE)](https://wiki.fysik.dtu.dk/ase/) is a set of tools and Python modules for setting up, manipulating, running, visualizing and analyzing atomistic simulations. It can be used together with VASP and many other programs.

In this workshop it's used to help compute the equation of state in some of the examples.

 ````{tabs}
  ```{group-tab} Tetralith
  To use ASE, load its module together with a suitable Python installation e.g.

      module load ASE/3.21.0-nsc1
      module load Python/3.10.4-env-nsc1-gcc-2022a-eb

  Also note that ASE is directly available from the py4vasp module:

      module load py4vasp/0.7.4-hpc1
  ```
  ```{group-tab} LEONARDO
  ASE is available via a Python module prepared for the workshop

      module use /leonardo_scratch/fast/EUHPC_TD02_030/vasp_ws2024/modules 
      module load pythonws-env/1.0-hpc1

  ```
 ````

### vaspkit

[vaspkit](https://vaspkit.com/) is a tool for both pre- and post-processing of VASP calculations for a wide range of material properties. Here, we apply the free to use version of it.

 ````{tabs}
  ```{group-tab} Tetralith
  TBA
  ```
  ```{group-tab} LEONARDO
  Before first use, copy its configuration file to your home folder

      cp /leonardo_scratch/fast/EUHPC_TD02_030/vasp_ws2024/vaspkit.1.5.1/.vaspkit ~/.

 thereafter, it can be used by loading the module and run in the same folder as your calculation

      module use /leonardo_scratch/fast/EUHPC_TD02_030/vasp_ws2024/module
      module load vaspkit/1.5.1-hpc1
      vaspkit

  ```
 ````

### cif2cell

[cif2cell](https://github.com/torbjornbjorkman/cif2cell) is a tool for generating input structures (e.g. POSCAR) for electronic structure codes (e.g. VASP) starting from a CIF file. 

For example, it can be very useful if you start from an experimental structure reported in the [Crystallograpohy Open Database](https://www.crystallography.net/cod/) which uses the CIF format. If you have a different structure format which can be converted to CIF, you can use cif2cell to produce POSCAR as a second step.

 ````{tabs}
  ```{group-tab} Tetralith
  It is available as a module

      module load cif2cell/2.1.0-hpc1
  ```
  ```{group-tab} LEONARDO
  A module is prepared for the workshop

      module use /leonardo_scratch/fast/EUHPC_TD02_030/vasp_ws2024/modules
      module load cif2cell/2.1.0-hpc1 
  ```
 ````
Its options can be found by

    cif2cell --help

A quick example, read a name.cif structure file and output to POSCAR

    cif2cell name.cif -p vasp

### VESTA

[VESTA](https://jp-minerals.org/vesta/en/) is a 3D visualization program for structural models, volumetric data such as electron/nuclear densities, and crystal morphologies.

It's available for Windows, Mac and Linux. Free of charge for non-commercial users.

 ````{tabs}
  ```{group-tab} Tetralith
  It is available as a module

      module load vesta/3.4.4-nsc1
      vesta &
  ```
  ```{group-tab} LEONARDO
  It is not available (can install on local computer to try out)
  ```
 ````

### Jupyter-notebook and jupyter-lab

In brief, jupyter-notebook is a web-based interactive document which can be shared. For example, it can be used to run Python. Jupyter-lab is an extensive interface which includes jupyter-notebook.

The main page is in [this link](https://jupyter.org/). Also see [documentation](https://docs.jupyter.org/en/latest/index.html).

 ````{tabs}
  ```{group-tab} Tetralith
  The jupyter-lab and notebook are included together with the py4vasp module

      module load py4vasp/0.7.4-hpc1

  It can be started directly on the login node via ThinLinc by typing

      jupyter-lab

  and it will open in a browser. This is fine for regular plots etc. For heavier processing, instead start it in an interactive job session on a work node, for example

      interactive -A naiss2024-22-241 -t 01:00:00 -n 4
      jupyter-lab --no-browser --ip=NODENAME

  if the session runs on e.g. node n58, set `--ip=n58`. From the output, start Firefox and copy & paste the corresponding link.

  Jupyter is also typically available within the Python env installations on Tetralith. A different possibility is to install it using conda/mamba or a Python virtual environment, see the [NSC Python page](https://www.nsc.liu.se/software/python/) for more details.

  ```
  ```{group-tab} LEONARDO
  While jupyter-lab and notebook is available in the Python environment prepared for the workshop

      module use /leonardo_scratch/fast/EUHPC_TD02_030/vasp_ws2024/modules 
      module load pythonws-env/1.0-hpc1

  one needs to set up port-forwarding in order to connect a session on a LEONARDO login node to ones local computer. For example, on the login node one can start

      jupyter-lab --no-browser

   and it will output a link which can be used for a browser. In this information, a specific port is shown. Now, one needs to on the local computer set up a port-forwarding which may look like   

      ssh -N -f -L localhost:YYYY:localhost:YYYY USERNAME@loginNN-ext.leonardo.cineca.it

  or

      ssh -TN -f USERNAME@loginNN-ext.leonardo.cineca.it -L YYYY:localhost:YYYY

  here, one fills in the port YYYY, USERNAME, and specific login node NN where jupyter-lab is started. If the port-forwarding is successful, then it's possible to open the session in ones browser on the local computer.

  ```
 ````
    

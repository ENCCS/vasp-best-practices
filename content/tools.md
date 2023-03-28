## Useful tools

Some of the tools are also described in the examples. For an easy overview, a description is collected on this page. There are many more tools which can be used, some are mentioned in seminar part 4 (Utilities & Summary).

### Command line tools


### Text editors


### Gnuplot


### p4vasp


### py4vasp

[py4vasp](https://www.vasp.at/py4vasp/latest/) is a python interface which extracts data from a VASP calculation, using the HDF5 `.h5` output file (meaning that VASP needs to be compiled with HDF5 support). It can be used e.g. to quickly plot density of states, bandstructure and energy convergence. It's optimized for use together with jupyter-lab and jupyter-notebook.

After starting a Python kernel which includes py4vasp via jupyter, in the notebook one first loads py4vasp and thereafter sets where to find the finished VASP calculation of interest

    import py4vasp
    mycalc = py4vasp.Calculation.from_path("/path/to/your/calculation/folder/here")

alternatively, one can provide the direct path to the VASP `.h5` output file

    mycalc = py4vasp.Calculation.from_file("/path/to/your/file/vaspout.h5")

Here below a few examples are shown. For a much more detailed description, refer to the [py4vasp page](https://www.vasp.at/py4vasp/latest/) and also see some [example of tutorials using py4vasp from the VASP developers](https://www.vasp.at/tutorials/latest/).

Examples for plotting density of states (DOS)

    mycalc.dos.plot()
    mycalc.dos.plot("s,p,d")
    mycalc.dos.plot()
    mycalc.dos.plot()

Plotting the bandstructure

    mycalc.band.plot()

Showing the POSCAR structure in 3D

    mycalc.structure.plot()

Plotting the energy convergence

    mycalc.energy[:].plot()


### ASE


### cif2cell


### VESTA


### Jupyter-notebook

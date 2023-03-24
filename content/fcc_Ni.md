## fcc Ni

[Based on the VASP wiki example in this link](https://www.vasp.at/wiki/index.php/Fcc_Ni)

**Task:** For spin-polarized (collinear magnetism) fcc Ni. Do a lattice parameter optimization, calculate DOS and bandstructure.

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

First, copy the example folder which contains some of the VASP input files

    cp -r /software/sse/manual/vasp/training/ws2023/fcc_Ni .
    cd fcc_Ni

and copy the latest POTCAR file for Ni

    cp /software/sse/manual/vasp/POTCARs/PBE/2015-09-21/Ni/POTCAR .

Perform the calculations below in the same way as was done for the [cd Si example](../cd_Si).

### Input files

POSCAR

    fcc Ni
     3.53 
     0.5 0.5 0.0
     0.0 0.5 0.5
     0.5 0.0 0.5
    Ni
       1
    cartesian
    0 0 0

INCAR

    general:
      SYSTEM = fcc Ni
      ISTART = 0 ; ICHARG=2
      ENCUT  =    270
      ISMEAR =    1  ; SIGMA = 0.2
      LORBIT=11
    spin:
      ISPIN=2
      MAGMOM = 1

* [ISTART](https://www.vasp.at/wiki/index.php/ISTART)=0, static calculation (default)
* [ICHARG](https://www.vasp.at/wiki/index.php/ICHARG)=2, initial charge-density from overlapping atoms (default if ISTART=0)
* [ENCUT](https://www.vasp.at/wiki/index.php/ENCUT)=270, default energy cutoff 270 eV
* [ISMEAR](https://www.vasp.at/wiki/index.php/ISMEAR)=1, Methfessel-Paxton smearing used for metal
* [SIGMA](https://www.vasp.at/wiki/index.php/ISMEAR)=0.2, default smearing
* [LORBIT](https://www.vasp.at/wiki/index.php/LORBIT)=11, write DOSCAR and *lm*-decomposed PROCAR
* [ISPIN](https://www.vasp.at/wiki/index.php/ISPIN)=2, gives a spin-polarized calculation and [MAGMOM](https://www.vasp.at/wiki/index.php/MAGMOM)=1, an initial magnetic moment of 1 Bohr magnetons 

KPOINTS

    k-points
     0
    Monkhorst Pack
     11 11 11
     0  0  0

* Equally spaced k-mesh
* Odd Monkhorst-Pack k-mesh > Gamma centered

 
### 1. Volume relaxation

Similar as for the [cd Si](../cd_Si) example, check the total energy over a range of volumes, by using the tailored job script "run-vol.sh"

    sbatch run-vol.sh

after it finishes, check the total energy vs lattice constant e.g. using gnuplot

    gnuplot 
    
and at the prompt type 

    plot "SUMMARY.dia" using ($1):($4) w lp

is the equilibrium lattice parameter close to *a* = 3.5 Å?

In the same way as was done in [fcc Si](../fcc_Si) and [cd Si](../cd_Si), investigate the output from Birch-Murnaghan EOS by using the "eqos.py" script.

* What is the equilibrium lattice parameter in this case?

### 2. DOS

Create a new folder "dos", copy the relevant files and go there

    mkdir dos
    cp INCAR POSCAR KPOINTS POTCAR run.sh dos
    cd dos
    
As in the previous example for [cd Si](../cd_Si) we compute DOS in a single step. Edit INCAR such that it looks like

    general:
      SYSTEM = fcc Ni
      ISTART = 0 ; ICHARG=2
      ENCUT  =    270
      ISMEAR =   -5
      LORBIT=11
    spin:
      ISPIN=2
      MAGMOM = 1

notice the change to [ISMEAR](https://www.vasp.at/wiki/index.php/ISMEAR)=-5, the tetrahedron method with Blöchl corrections, suitable for DOS and total energies.

Finally, submit the job

    sbatch run.sh

To check the result after finish, use `p4vasp` as in the previous examples.

* Does the DOS show the spin split?

### 3. Bandstructure

In the main "fcc_Ni" folder, create a new folder "band", copy the relevant files and go there, note the treatment for the "KPOINTS" file

    mkdir band
    cp INCAR POSCAR POTCAR run.sh band
    cp KPOINTS.band band/KPOINTS
    cd band

the file KPOINTS.band, which was copied to KPOINTS, looks like

    kpoints for bandstructure L-G-X-U K-G
     10
    line
    reciprocal
      0.50000  0.50000  0.50000    1
      0.00000  0.00000  0.00000    1

      0.00000  0.00000  0.00000    1
      0.00000  0.50000  0.50000    1

      0.00000  0.50000  0.50000    1
      0.25000  0.62500  0.62500    1

      0.37500  0.7500   0.37500    1
      0.00000  0.00000  0.00000    1

As in previous bandstructure examples, e.g. [cd Si](../cd_Si), we need a suitable `CHGCAR` file. First check that INCAR is correct, edit the file using e.g. `gedit` such that

    ICHARG=11

i.e. that CHGCAR is read. Copy CHGCAR from the previous DOS calculation

    cp ../dos/CHGCAR .

thereafter submit the job

    sbatch run.sh
    
To check the results after finish, use `p4vasp`. Compare with the [result on the VASP wiki](https://www.vasp.at/wiki/index.php/Fcc_Ni).


## cd Si volume relaxation

[Based on the VASP wiki example in this link](https://www.vasp.at/wiki/index.php/Cd_Si_volume_relaxation)

**Task:** Relaxation of the internal coordinates, volume and cell shape in cubic diamond Si. [Also see the discussion on energy vs volume, volume relaxations and Pulay stress](https://www.vasp.at/wiki/index.php/Energy_vs_volume_Volume_relaxations_and_Pulay_stress)

There are several ways in which the equilibrium volume can be determined

* By fitting the total energies over a volume range e.g. using an equation of state method
* Relaxing the structure with VASP "on the fly"

The first approach was done in the previous example [cd Si](../cd_Si). Here, the second approach will be used. While it's fast, one needs to be careful regarding the accuracy and consider the [Pulay stress](https://www.vasp.at/wiki/index.php/Energy_vs_volume_Volume_relaxations_and_Pulay_stress).

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

First, copy the example folder which contains the VASP input files
 ````{tabs}
  ```{group-tab} Tetralith
      cp -r /software/sse2/tetralith_el9/manual/vasp/training/ws2024/cd_Si_vol_relax .
      cd cd_Si_vol_relax

  and copy the latest POTCAR file for Si

      cp /software/sse2/tetralith_el9/manual/vasp/POTCARs/PBE/2024-03-19/Si/POTCAR .
  ```
  ```{group-tab} LEONARDO
      cp -r /leonardo_scratch/fast/EUHPC_D02_030/vasp_ws2024/examples/cd_Si_vol_relax .
      cd cd_Si_vol_relax

  and copy the latest POTCAR file for Si

      cp /leonardo_scratch/fast/EUHPC_D02_030/vasp_ws2024/potpaw_PBE.64/Si/POTCAR .
  ```
 ````

### Input files

POSCAR

    cubic diamond Si
       5.5
     0.0    0.5     0.5
     0.5    0.0     0.5
     0.5    0.5     0.0
    Si
      2
    Direct
     -0.125 -0.125 -0.125
      0.125  0.125  0.125

INCAR

    System = diamond Si

    ISMEAR    = 0 
    SIGMA     = 0.1
    ENMAX     = 240
    IBRION    = 2 
    ISIF      = 3 
    NSW       = 15
    EDIFF     = 0.1E-04
    EDIFFG    = -0.01

* [IBRION](https://www.vasp.at/wiki/index.php/IBRION)=2, for using the conjugate-gradient algorithm
* [ISIF](https://www.vasp.at/wiki/index.php/ISIF)=3, for change of internal parameters, shape and volume at the same time
* [NSW](https://www.vasp.at/wiki/index.php/NSW)=15, max number of ionic steps
* [EDIFF](https://www.vasp.at/wiki/index.php/EDIFF)=0.1E-04, the default stop value for difference in total energy between steps
* [EDIFFG](https://www.vasp.at/wiki/index.php/EDIFFG)=-0.01, if negative value, stop criterium for ionic relaxation if forces are smaller than |EDIFFG|

KPOINTS

    k-points
     0
    Monkhorst Pack
     11 11 11
     0  0  0

### Calculation

Start the volume relaxation calculation by submitting the job 

    sbatch run.sh

Monitor how the structural relaxation progresses with

    cat OSZICAR

Check the relaxed final structure

    cat CONTCAR

* Compare with the EOS lattice parameter obtained in the [previous example](../cd_Si) and from the [VASP wiki](https://www.vasp.at/wiki/index.php/Cd_Si_volume_relaxation) a= 5.4687 Å

* Note that one doesn't use the total energy or DOS from a structural relaxation. For that, CONTCAR should be copied to POSCAR for a separate caclulation with no structural relaxation.

 ````{tabs}
  ```{group-tab} Tetralith
  Check the convergence of the total energy and forces using p4vasp

      p4v &

  by selecting Convergence > Energy or > Forces.

  ```
  ```{group-tab} LEONARDO
  Check the convergence of the total energy using py4vasp

      import py4vasp
      mycalc = py4vasp.Calculation.from_path("/path/to/your/calculation/folder/here")
      mycalc.energy[:].plot()

  ```
 ````

### Extra tasks

* Repeat the volume relaxation calculation in a new folder, but this time start from the relaxed structure `CONTCAR`, by copying it to POSCAR. Does the structure change, if so, how much?

* Repeat the volume relaxation calculation from scratch with higher accuracy, e.g. set ENCUT to 1.3 x ENMAX (grep ENMAX POTCAR) and PREC=Accurate in INCAR. Also, set a smaller value for EDIFF. Any difference in the lattice parameter a?

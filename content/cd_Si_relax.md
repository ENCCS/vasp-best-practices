## cd Si relaxation

[Based on the VASP wiki example in this link](https://www.vasp.at/wiki/index.php/Cd_Si_relaxation)

**Task:** Relaxation of the internal coordinates of a perturbed cubic diamond Si structure. 

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

First, copy the example folder which contains some of the VASP input files and useful scripts 

    cp -r /software/sse/manual/vasp/training/ws2023/cd_Si_relax .
    cd cd_Si_relax

and copy the latest POTCAR file for Si:

    cp /software/sse/manual/vasp/POTCARs/PBE/2015-09-21/Si/POTCAR .

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
      0.125  0.125  0.130

* Note the distortion for the 2nd atom in z, from 0.125 to 0.130

INCAR

    System = diamond Si
    
    ISTART = 0
    ICHARG=2
    ENCUT  =    240
    ISMEAR = 0 
    SIGMA = 0.1
    NSW    =  10 
    IBRION =  2
    ISIF   =  2
    EDIFFG = -0.0001

* [NSW](https://www.vasp.at/wiki/index.php/NSW)=10 relaxation steps
* [IBRION](https://www.vasp.at/wiki/index.php/IBRION)=2, conjugate-gradient algorithm
* [ISIF](https://www.vasp.at/wiki/index.php/ISIF)=2, relax only internal parameters

KPOINTS

    k-points
     0
    Monkhorst Pack
     11 11 11
     0  0  0

 
### Calculation

The input files are ready for the atom relaxation, so the job can be started directly

    sbatch run.sh

Check the progress of the relaxation by e.g.

    cat slurm*out
    cat OSZICAR

the calculation should be quite fast. At the end of OUTCAR, e.g. using `less`, check the final forces

     POSITION                                       TOTAL-FORCE (eV/Angst)
     -----------------------------------------------------------------------------------
          4.81938      4.81938      4.81254        -0.000143     -0.000143     -0.001100
          0.69437      0.69437      0.68746         0.000143      0.000143      0.001100
     -----------------------------------------------------------------------------------
        total drift:                                0.000001      0.000001     -0.000003

* The resulting structure can be found in [CONTCAR](https://www.vasp.at/wiki/index.php/CONTCAR)
* The progress of the structure at each relaxation point is found in [XDATCAR](https://www.vasp.at/wiki/index.php/XDATCAR)



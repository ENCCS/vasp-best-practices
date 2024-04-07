## fcc Ni revisited

[Based on the VASP wiki example in this link](https://www.vasp.at/wiki/index.php/Fcc_Ni_(revisited))

**Task:** Calculate partial DOS of spin-polarized fcc ferromagnet Ni. 

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

First, copy the example folder which contains some of the VASP input files
 ````{tabs}
  ```{group-tab} Tetralith
      cp -r /software/sse2/tetralith_el9/manual/vasp/training/ws2024/fcc_Ni_rev .
      cd fcc_Ni_rev

  and copy the latest POTCAR file for Ni

      cp /software/sse2/tetralith_el9/manual/vasp/POTCARs/PBE/2024-03-19/Ni/POTCAR .
  ```
  ```{group-tab} LEONARDO
      cp -r /leonardo_scratch/fast/EUHPC_D02_030/vasp_ws2024/examples/fcc_Ni_rev .
      cd fcc_Ni_rev

  and copy the latest POTCAR file for Ni

      cp /leonardo_scratch/fast/EUHPC_D02_030/vasp_ws2024/potpaw_PBE.64/Ni/POTCAR .
  ```
 ````

### Input files

POSCAR

    fcc Ni
     -10.93 
     0.5 0.5 0.0
     0.0 0.5 0.5
     0.5 0.0 0.5
    Ni
       1
    cartesian
    0 0 0

* Note the use of volume instead of lattice parameter in the 2nd line, indicated by minus "-"

INCAR

    SYSTEM  = Ni fcc bulk 

    ISTART  = 0
    ISPIN   = 2
    MAGMOM  = 1.0
    ISMEAR  = -5
    VOSKOWN = 1 
    LORBIT  = 11

* [ISTART](https://www.vasp.at/wiki/index.php/ISTART)=0, start job from scratch (default)
* [ISPIN](https://www.vasp.at/wiki/index.php/ISPIN)=2, gives a spin-polarized calculation
* [MAGMOM](https://www.vasp.at/wiki/index.php/MAGMOM)=1.0, an initial magnetic moment of 1.0 Bohr magnetons is set 
* [ISMEAR](https://www.vasp.at/wiki/index.php/ISMEAR)=-5, Tetrahedron method with Blöchl's corrections used for k-mesh integration
* [VOSKOWN](https://www.vasp.at/wiki/index.php/VOSKOWN)=1, interpolation scheme of Vosko, Wilk and Nusair applied
* [LORBIT](https://www.vasp.at/wiki/index.php/LORBIT)=11, write DOSCAR and *lm*-decomposed PROCAR

KPOINTS

    k-points
     0
    Gamma
     11 11 11
     0  0  0

* Equally spaced k-mesh
* Here the Gamma (G) k-mesh is used, which always include the Gamma point

### 1. Collinear calculation

First create a new folder "col", copy the files and go there

    mkdir col
    cp INCAR POSCAR POTCAR KPOINTS run.sh col
    cd col

since INCAR is already prepared for a collinear calculation, it's just to submit the job

    sbatch run.sh

and it should finish quite quickly. Check the magnetic moment, e.g. by

    cat OSZICAR

at the end it might look something like

    ...
    DAV:   9    -0.545925473247E+01    0.23756E-02   -0.16066E-03  3008   0.279E-01    0.250E-01
    DAV:  10    -0.545865706078E+01    0.59767E-03   -0.57805E-04  2004   0.147E-01    0.261E-02
    DAV:  11    -0.545865295189E+01    0.41089E-05   -0.33171E-05  1412   0.519E-02
       1 F= -.54586530E+01 E0= -.54586530E+01  d E =0.000000E+00  mag=     0.5874

Notice the value for the magnetic moment on the right hand side. To just show last line, e.g. `grep mag OSZICAR`.

One can also check the *l* decomposed parts of the magnetic moment at the end of OUTCAR, e.g. open it with

    less OUTCAR

and press `G` (that is `shift` `g`) to go to the end (quit with `q`). It looks like

     magnetization (x)
     
    # of ion       s       p       d       tot
    ------------------------------------------
        1       -0.007  -0.026   0.636   0.602

* What happens if one instead sets an initial magnetic moment of `MAGMOM = 0.0` or `MAGMOM = 2.0`?
* What can be said about the importance of setting appropriate initial magnetic moments?
* Check the spin-polarized DOS using p4vasp or py4vasp
* Any interesting messages in slurm-JOBID.out?

### 2. Non-collinear calculation

In the case of a non-collinear calculation, the magnetic moment will be allowed to point in three dimensions. Now, go back to the main folder "fcc_Ni_rev", create a new folder "nonc" and copy relevant files

    mkdir nonc
    cp INCAR POSCAR POTCAR KPOINTS run.sh nonc
    cd nonc
    
For non-collinear calculations, one needs to change INCAR, comment out the two lines for the collinear calculations

    #ISPIN   = 2
    #MAGMOM  = 1.0
    
and insert two lines

    LNONCOLLINEAR = .TRUE.
    MAGMOM        = 0.0 0.0 1.0    

The default is [LNONCOLLINEAR](https://www.vasp.at/wiki/index.php/LNONCOLLINEAR)=.FALSE. To run non-collinear calculations, the VASP binary must also be changed to `vasp_ncl`, otherwise the job will crash.

First, copy the example folder which contains some of the VASP input files.

Edit the job script "run.sh" so that the last lines look like

 ````{tabs}
  ```{group-tab} Tetralith
      #mpprun vasp_std
      mpprun vasp_ncl
  ```
  ```{group-tab} LEONARDO
      #srun vasp_std
      srun vasp_ncl
  ```
 ````

Run the calculation

    sbatch run.sh

and check the magnetic moment in the same way as for **1.** when it finishes. For OSZICAR it might look like

    DAV:  10    -0.546407531955E+01    0.67997E-03   -0.80644E-05  7064   0.195E-01    0.291E-02
    DAV:  11    -0.546409507244E+01   -0.19753E-04   -0.12794E-04  7588   0.126E-01
       1 F= -.54640951E+01 E0= -.54640951E+01  d E =0.000000E+00  mag=    -0.0000     0.0000     0.5878

and at the end of OUTCAR

     magnetization (x)
 
    # of ion       s       p       d       tot
    ------------------------------------------
        1       -0.000   0.000  -0.000  -0.000
 


     magnetization (y)
 
    # of ion       s       p       d       tot
    ------------------------------------------
        1        0.000  -0.000   0.000   0.000
 


     magnetization (z)
 
    # of ion       s       p       d       tot
    ------------------------------------------
        1       -0.008  -0.027   0.637   0.602

* What happens by changing the direction of the initial magnetic moment, e.g. setting `MAGMOM = 1.0 0.0 0.0` or `MAGMOM = 0.0 1.0 0.0`?

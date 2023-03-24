## Ni100 surface

Based on the three VASP wiki examples in the links [1](https://www.vasp.at/wiki/index.php/Ni_100_surface_relaxation), [2](https://www.vasp.at/wiki/index.php/Ni_100_surface_DOS) and [3](https://www.vasp.at/wiki/index.php/Ni_100_surface_bandstructure) 

**Task:** Perform a relaxation of the first two layers of a Ni (100) surface, thereafter calculate its DOS and bandstructure.

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

    cp -r /software/sse/manual/vasp/training/ws2023/Ni100_surf .
    cd Ni100_surf

and copy the latest POTCAR file for Ni

    cp /software/sse/manual/vasp/POTCARs/PBE/2015-09-21/Ni/POTCAR .

### Input files

POSCAR

    fcc (100) surface
     3.53
       .50000   .50000   .00000
      -.50000   .50000   .00000
       .00000   .00000  5.00000
    Ni
      5
    Selective Dynamics
    Cartesian
       .00000   .00000   .00000 F F F
       .00000   .50000   .50000 F F F
       .00000   .00000  1.00000 F F F
       .00000   .50000  1.50000 T T T
       .00000   .00000  2.00000 T T T

* Ni lattice constant a = 3.53Å
* 1 atom per layer
* 5 layers in total
* Note "S" or "Selective dynamics" chosen in the line under number of atoms

INCAR

      ISTART = 0; ICHARG = 2
    
    general:
      SYSTEM = clean Ni(100) surface
      ENCUT = 270 
      ISMEAR = 2 ; SIGMA = 0.2
      ALGO = Fast
      EDIFF = 1E-6
    
    spin:
      ISPIN=2
      MAGMOM = 5*1
    
    dynamic:
      NSW = 100
      POTIM = 0.8
      IBRION = 1

* [ISTART](https://www.vasp.at/wiki/index.php/ISTART)=0, static calculation (default)
* [ICHARG](https://www.vasp.at/wiki/index.php/ICHARG)=2, initial charge-density from overlapping atoms (default if ISTART=0)
* [ENCUT](https://www.vasp.at/wiki/index.php/ENCUT)=270, default energy cutoff 270 eV
* [ISMEAR](https://www.vasp.at/wiki/index.php/ISMEAR)=2, Methfessel-Paxton smearing used for metal
* [SIGMA](https://www.vasp.at/wiki/index.php/SIGMA)=0.2, default smearing
* [ALGO](https://www.vasp.at/wiki/index.php/ALGO)=Fast, (default is Normal) first steps according to Davidson, thereafter RMM-DIIS, algorithms for electron minimization
* [EDIFF](https://www.vasp.at/wiki/index.php/EDIFF)=1E-6,
* [ISPIN](https://www.vasp.at/wiki/index.php/ISPIN)=2, gives a spin-polarized calculation
* [MAGMOM](https://www.vasp.at/wiki/index.php/MAGMOM)=5*1, for the 5 atoms in POSCAR an initial magnetic moment of 1 Bohr magnetons
* [NSW](https://www.vasp.at/wiki/index.php/NSW)=100, 
* [POTIM](https://www.vasp.at/wiki/index.php/POTIM)=0.8, 
* [IBRION](https://www.vasp.at/wiki/index.php/IBRION)=1, ionic relaxation (RMM-DIIS)

KPOINTS

    k-points
    0
    Monkhorst-Pack
    9 9 1
    0 0 0

* Equally spaced k-mesh
* Odd Monkhorst-Pack k-mesh > Gamma centered
* Note, only one k-point in the z-direction for the surface

### 1. Surface relaxation

First, note how selective dynamics (S) works in the [POSCAR](https://www.vasp.at/wiki/index.php/POSCAR) file

    Selective Dynamics
    Cartesian
       .00000   .00000   .00000 F F F
       .00000   .50000   .50000 F F F
       .00000   .00000  1.00000 F F F
       .00000   .50000  1.50000 T T T
       .00000   .00000  2.00000 T T T

So, for relaxation `F=False` and `T=True`, so one sees that the two atoms at z=1.5 and 2.0 are able to move in all directions, while the three lower atoms (layers) are fixed. 

* For surface relaxations it's typical to fix the bulk-like atoms in the bottom and let the ones close to the surface be able to relax
* Alternatively, a symmetric supercell can be constructed with inner bulk-like layers

Run the calculation with

    sbatch run.sh
    
and observe the relaxation e.g. with

    cat OSZICAR
    
After the calculation is finished, compare the forces in OUTCAR between the first and the last step.

First step:

     POSITION                                       TOTAL-FORCE (eV/Angst)
     -----------------------------------------------------------------------------------
          0.00000      0.00000      0.00000         0.000000      0.000000      0.419201
          0.00000      1.76500      1.76500         0.000000      0.000000     -0.401608
          0.00000      0.00000      3.53000         0.000000      0.000000     -0.002589
          0.00000      1.76500      5.29500         0.000000      0.000000      0.392849
          0.00000      0.00000      7.06000        -0.000000     -0.000000     -0.407852
     -----------------------------------------------------------------------------------
        total drift:                               -0.000000     -0.000000     -0.008050


Last step:

     POSITION                                       TOTAL-FORCE (eV/Angst)
     -----------------------------------------------------------------------------------
          0.00000      0.00000      0.00000        -0.000000      0.000000      0.425910
          0.00000      1.76500      1.76500         0.000000     -0.000000     -0.402950
          0.00000      0.00000      3.53000        -0.000000      0.000000     -0.023012
          0.00000      1.76500      5.29871        -0.000000      0.000000     -0.001056
         -0.00000     -0.00000      6.98070        -0.000000     -0.000000      0.001107
     -----------------------------------------------------------------------------------
        total drift:                                0.000000     -0.000000     -0.019988    

Check the obtained relaxed structure in `CONTCAR`:

    fcc (100) surface                       
       3.53000000000000     
         0.5000000000000000    0.5000000000000000    0.0000000000000000
        -0.5000000000000000    0.5000000000000000    0.0000000000000000
         0.0000000000000000    0.0000000000000000    5.0000000000000000
       Ni
         5
    Selective dynamics
    Direct
      0.0000000000000000  0.0000000000000000  0.0000000000000000   F   F   F
      0.5000000000000000  0.5000000000000000  0.1000000000000014   F   F   F
      0.0000000000000000  0.0000000000000000  0.2000000000000028   F   F   F
      0.5000000000000000  0.5000000000000000  0.3002099841022341   T   T   T
     -0.0000000000000000  0.0000000000000000  0.3955072458335201   T   T   T

* Check the convergence using p4vasp
* Compare surface energies following the example in the [VASP wiki](https://www.vasp.at/wiki/index.php/Ni_100_surface_relaxation)
* What is the inward relaxation of the surface layers (compare VASP wiki)
* Visualize the relaxation of the structure using p4vasp (follow VASP wiki figures)

### 2. Surface DOS

Now, in a new folder "dos", calculate the local DOS for the relaxed Ni(100) surface using CONTCAR from the previous step

    mkdir dos
    cp CONTCAR dos/POSCAR
    cp INCAR.dos dos/INCAR
    cp POTCAR KPOINTS run.sh dos
    cd dos

Also note that we use a new INCAR (from INCAR.dos) which looks like

    general:
      SYSTEM = clean (100) Ni surface
      ENMAX = 270
      ISMEAR =   -5
      ALGO = Normal 
    
    spin:
      ISPIN = 2
      MAGMOM = 5*1   
    
      LORBIT = 11  # lm and site decomposed DOS inside PAW spheres

* [ISMEAR](https://www.vasp.at/wiki/index.php/ISMEAR)=-5, the tetrahedron method with Blöchl corrections, suitable for DOS
* [ALGO](https://www.vasp.at/wiki/index.php/ALGO)=Normal, the default electron minimization algorithm
* [LORBIT](https://www.vasp.at/wiki/index.php/LORBIT)=11, lm and site decomposed DOS

Run the calculation with

    sbatch run.sh

After it finishes, at the end of OUTCAR, check the information on local charge and magnetization

     total charge     
 
    # of ion       s       p       d       tot
    ------------------------------------------
        1        0.464   0.328   8.294   9.086
        2        0.488   0.483   8.309   9.280
        3        0.491   0.485   8.317   9.294
        4        0.498   0.505   8.334   9.338
        5        0.477   0.350   8.332   9.158
    --------------------------------------------------
    tot          2.418   2.151  41.586  46.156
 


     magnetization (x)
 
    # of ion       s       p       d       tot
    ------------------------------------------
        1       -0.003  -0.021   0.751   0.727
        2       -0.008  -0.026   0.645   0.611
        3       -0.008  -0.026   0.636   0.602
        4       -0.008  -0.026   0.630   0.596
        5       -0.004  -0.021   0.725   0.700
    --------------------------------------------------
    tot         -0.032  -0.120   3.388   3.236

* By setting [LORBIT](https://www.vasp.at/wiki/index.php/LORBIT)=1 and changing [RWIGS](https://www.vasp.at/wiki/index.php/RWIGS), it's possible to control the total number of electrons within the sphere
* What can be said about the magnetic moments for the different layers?
* Test to plot DOS using p4vasp, see figures at the end of the [VASP wiki example](https://www.vasp.at/wiki/index.php/Ni_100_surface_DOS)

### 3. Surface bandstructure

Now, calculate the corresponding bandstructure for the relaxed Ni(100) surface structure. Go to the main folder "Ni100_surf" and there create the folder "band" and copy the needed files

    mkdir band
    cp CONTCAR band/POSCAR
    cp INCAR.band band/INCAR
    cp KPOINTS.band band/KPOINTS
    cp POTCAR run.sh band
    cd band

Also note that we use a new INCAR (from INCAR.band) which looks like

      ICHARG = 11
    general:
      SYSTEM = clean (100) nickel surface
      ENMAX  = 270
      ISMEAR = 2 ; SIGMA = 0.2
      ALGO = Normal
    
    spin:
      ISPIN = 2
      MAGMOM = 5*1
    
      LORBIT = 11

* [ICHARG](https://www.vasp.at/wiki/index.php/ICHARG)=11, for a non-self consistent run using previously obtained CHGCAR

Copy CHGCAR

    cp ../dos/CHGCAR .
  
This time KPOINTS for the bandstructure looks like

    kpoints for band-structure G-X-M-G
      13
    reziprok
       .00000   .00000   .00000    1
       .12500   .00000   .00000    1
       .25000   .00000   .00000    1
       .37500   .00000   .00000    1
       .50000   .00000   .00000    1

       .50000   .12500   .00000    1
       .50000   .25000   .00000    1
       .50000   .37500   .00000    1
       .50000   .50000   .00000    1

       .37500   .37500   .00000    1
       .25000   .25000   .00000    1
       .12500   .12500   .00000    1
       .00000   .00000   .00000    1  
  
* 13 k-points along the line Gamma - X - M - Gamma
* Reciprocal coordinates
* Each point has weight 1
      
Submit the job

    sbatch run.sh

and wait for it to finish. Investigate the bandstructure using p4vasp, compare with the [VASP wiki example](https://www.vasp.at/wiki/index.php/Ni_100_surface_bandstructure).



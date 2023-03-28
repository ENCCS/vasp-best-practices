## fcc Si 

[Based on the VASP wiki example in this link](https://www.vasp.at/wiki/index.php/Fcc_Si)

**Task:** Run a self-consistent calculation for fcc Si. Thereafter, optimize the lattice constant. Use some basic tools and scripts.

* An introductory example for working with VASP
* In general, examples are chosen for fast calculation
* Use different job scripts, submit to the Slurm job scheduler (Tetralith) or run interactively (MeluXina)
* Use VASP, gnuplot, python, ASE
* bash shell scripts

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

First, copy the example folder which contains the input files INCAR, POSCAR, KPOINTS and some useful scripts 
 ````{tabs}
  ```{group-tab} Tetralith
      cp -r /software/sse/manual/vasp/training/ws2023/fcc_Si .
      cd fcc_Si

  also copy the latest POTCAR (PBE GGA) file for Si

      cp /software/sse/manual/vasp/POTCARs/PBE/2015-09-21/Si/POTCAR .

  ```
  ```{group-tab} MeluXina
      cp -r /project/home/p200051/vasp_ws2023/examples/fcc_Si .
      cd fcc_Si

  also copy the latest POTCAR (PBE GGA) file for Si

      cp /project/home/p200051/vasp_ws2023/vasp/potpaw_PBE.54/Si/POTCAR .
  ```
 ````

### Input files

POSCAR

    fcc Si
     3.9
     0.5 0.5 0.0
     0.0 0.5 0.5
     0.5 0.0 0.5
    Si
       1
    cartesian
    0 0 0

* Fcc Si lattice constant a=3.9 Å
* "Si" on line 6 isn't needed for the run, but for viewing e.g. using VESTA and practical as a reminder if you have several elements. Note that POTCAR decides the actual order of the elements in POSCAR, check with `grep PAW POTCAR`
* 1 atom in the cell

INCAR

    System = fcc Si

    ISTART = 0       
    ICHARG = 2       
    ENCUT  = 240     
    ISMEAR = 0       
    SIGMA  = 0.1     

* [ISMEAR](https://www.vasp.at/wiki/index.php/ISMEAR) determines the partial occupancies of each orbital. For band gap systems -5 (tetrahedron method with Blöchl corrections) or 0 (Gaussian smearing) are suitable.
* For very accurate total energy calculations or DOS, use ISMEAR = -5

KPOINTS

    k-points
     0
    Monkhorst Pack
     11 11 11
     0  0  0
 
* Face-centered-cubic structure, so use an equally spaced k-mesh 
* Odd number of k-points in each direction -> Gamma centered mesh
* Alternatively, use the Gamma centered k-mesh, replacing the line "Monkhorst Pack" (M) with "Gamma" (G) 

POTCAR

      PAW_PBE Si 05Jan2001                   
       4.00000000000000     
     parameters from PSCTR are:
       VRHFIN =Si: s2p2
       LEXCH  = PE
       EATOM  =   103.0669 eV,    7.5752 Ry

       TITEL  = PAW_PBE Si 05Jan2001
       LULTRA =        F    use ultrasoft PP ?
       IUNSCR =        1    unscreen: 0-lin 1-nonlin 2-no
       RPACOR =    1.500    partial core radius
       POMASS =   28.085; ZVAL   =    4.000    mass and valenz
       RCORE  =    1.900    outmost cutoff radius
       RWIGS  =    2.480; RWIGS  =    1.312    wigner-seitz radius (au A)
       ENMAX  =  245.345; ENMIN  =  184.009 eV
       ICORE  =        2    local potential
       LCOR   =        T    correct aug charges
       LPAW   =        T    paw PP
       EAUG   =  322.069
       DEXC   =    0.000
       RMAX   =    1.950    core radius for proj-oper
       RAUG   =    1.300    factor for augmentation sphere
       RDEP   =    1.993    radius for radial grids
       RDEPT  =    1.837    core radius for aug-charge
 
       Atomic configuration
        6 entries
         n  l   j            E        occ.
         1  0  0.50     -1785.8828   2.0000
         2  0  0.50      -139.4969   2.0000
         2  1  1.50       -95.5546   6.0000
         3  0  0.50       -10.8127   2.0000
         3  1  0.50        -4.0811   2.0000
         3  2  1.50        -4.0817   0.0000
    ...
    
* The top lines of the POTCAR file
* Never (almost) edit

Check that correct POTCARs are used and the ENMAX values for setting ENCUT in INCAR

    grep PAW POTCAR
    grep ENMAX POTCAR
    
### 1. Calculation 

A first static calculation for Si with the lattice constant 3.9 Å. Create a new folder "scf0", move the input files + job script, copy the folder to "scf1" (we will use it later) and go to "scf0"

    mkdir scf0
    mv INCAR POSCAR KPOINTS POTCAR run.sh scf0
    cp -r scf0 scf1
    cd scf0

 ````{tabs}
  ```{group-tab} Tetralith
  Submit the job script "run.sh" to the job queue with

      sbatch run.sh

  The job script looks like below

      #!/bin/bash
      #SBATCH -A snic2022-22-17
      #SBATCH -t 0:30:00
      #SBATCH -n 4 
      #SBATCH -J vaspjob

      module load VASP/6.3.0.20012022-omp-nsc1-intel-2018a-eb
      mpprun vasp_std

  ```
  ```{group-tab} MeluXina
  Run the job interactively in the Jupyter-notebook terminal with

      srun --hint=nomultithread -n 8 vasp_std

  This works if the settings were applied previously, see [starting section](../meluxina)

      source /project/home/p200051/vasp_ws2023/setup.sh

  which set the path to VASP binaries and loads the corresponding modules it was built with, check e.g. with "cat"

      cat /project/home/p200051/vasp_ws2023/setup.sh
  ```
 ````

The job should finish quite quickly. Check the status of the job (if submitted to the queue) with

    squeue -u USERNAME

it might already have finished, in that case it'll not be shown. Among the output files in particular note
     
    OUTCAR
    OSZICAR
    slurm-JOBID.out

in which `JOBID` is a string of numbers. Note that

* Some warning messages will only show in the standard output of the job, `slurm-JOBID.out` if submitted to the queue.
**Therefore, also carefully check the output when running interactively.**

You can quickly check the iteration steps and convergence with "cat", in a different terminal if it's still running interactively

    cat OSZICAR
    
For checking into the main output file OUTCAR and other large files, it's convenient to use the fast and safe (no writing) text viewer "less"

    less OUTCAR

"less" can be quit with pressing `q`.

### 2. Total energy vs volume calculation

Go back to the main folder "fcc_Si" with

    cd ..
    pwd

"pwd" shows the present folder, confirm that you're back in "fcc_Si", otherwise use "cd" to go there.

In this part we will calculate the total energies of fcc Si between 3.5 and 4.3 Å. To do this a bit quicker, a special job script "run-vol.sh" is prepared (bash shell script):

 ````{tabs}
  ```{group-tab} Tetralith
      #!/bin/bash
      #SBATCH -A snic2022-22-17
      #SBATCH -t 0:30:00
      #SBATCH -n 4
      #SBATCH -J vaspjob

      module load VASP/6.3.0.20012022-omp-nsc1-intel-2018a-eb

      for i in  3.5 3.6 3.7 3.8 3.9 4.0 4.1 4.2 4.3 ; do
      mkdir -p $i
      cd $i
      cp /software/sse/manual/vasp/POTCARs/PBE/2015-09-21/Si/POTCAR .
      cp /software/sse/manual/vasp/training/ws2023/fcc_Si/INCAR .
      cp /software/sse/manual/vasp/training/ws2023/fcc_Si/KPOINTS .
      cat >POSCAR <<EOF
      fcc:
         $i
       0.5 0.5 0.0
       0.0 0.5 0.5
       0.5 0.0 0.5
      Si
         1
      cartesian
      0 0 0
      EOF
      mpprun vasp_std
      E=`awk '/F=/ {print $0}' OSZICAR` ; echo $i $E  >>../SUMMARY.fcc
      cd ..
      done
  ```
  ```{group-tab} MeluXina
      #!/bin/bash

      for i in  3.5 3.6 3.7 3.8 3.9 4.0 4.1 4.2 4.3 ; do
      mkdir -p $i
      cd $i
      cp /project/home/p200051/vasp_ws2023/vasp/potpaw_PBE.54/Si/POTCAR .
      cp /project/home/p200051/vasp_ws2023/examples/fcc_Si/INCAR .
      cp /project/home/p200051/vasp_ws2023/examples/fcc_Si/KPOINTS .
      cat >POSCAR <<EOF
      fcc:
         $i
       0.5 0.5 0.0
       0.0 0.5 0.5
       0.5 0.0 0.5
      Si
         1
      cartesian
      0 0 0
      EOF
      srun --hint=nomultithread -n 8 vasp_std
      E=`awk '/F=/ {print $0}' OSZICAR` ; echo $i $E  >>../SUMMARY.fcc
      cd ..
      done
  ```
 ````

In brief, the above script creates a new folder with the same name as the lattice constant, copying POTCAR, INCAR and KPOINTS, while creating a new POSCAR file. It also collects the total energies from all OSZICAR files into a new file "SUMMARY.fcc".

Now, submit the job script "run-vol.sh" to the queue (Tetralith), or run it as an interactive job (MeluXina)

    sbatch run-vol.sh

respectively

    ./run-vol.sh

After a successful run, there should now be folders 3.5 - 4.3 with the different calculations and a file SUMMARY.fcc which can be checked e.g. with "less" or "cat"

    3.5 1 F= -.44256909E+01 E0= -.44234194E+01 d E =-.454310E-02
    3.6 1 F= -.46614931E+01 E0= -.46600638E+01 d E =-.285864E-02
    3.7 1 F= -.47980122E+01 E0= -.47959555E+01 d E =-.411323E-02
    3.8 1 F= -.48645323E+01 E0= -.48630343E+01 d E =-.299612E-02
    3.9 1 F= -.48774144E+01 E0= -.48758835E+01 d E =-.306173E-02
    4.0 1 F= -.48487753E+01 E0= -.48481407E+01 d E =-.126921E-02
    4.1 1 F= -.47852971E+01 E0= -.47845193E+01 d E =-.155573E-02
    4.2 1 F= -.46937300E+01 E0= -.46922884E+01 d E =-.288335E-02
    4.3 1 F= -.45831536E+01 E0= -.45812206E+01 d E =-.386597E-02

You can make a quick plot of the total energy as a function of the lattice constant, e.g. by using gnuplot. First, load the module

 ````{tabs}
  ```{group-tab} Tetralith
      module load gnuplot/5.2.2-nsc1
  ```
  ```{group-tab} MeluXina
      module load gnuplot/5.4.4-GCCcore-11.3.0 
  ```
 ````
and start it with

    gnuplot

thereafter, at the "gnuplot>" prompt type

 ````{tabs}
  ```{group-tab} Tetralith
      plot "SUMMARY.fcc" using ($1):($4) w lp
  ```
  ```{group-tab} MeluXina
      set term png 
      set output "SUMMARY.fcc.png"
      plot "SUMMARY.fcc" using ($1):($4) w lp

  Thereafter, open the output file `SUMMARY.fcc.png` in Jupyter-notebook.
  ```
 ````

From the plot we can see that the equilibrium lattice constant is around 3.9 Å.

To find a more exact value, we can use an equation of state method. For example, a popular method is Birch-Murnaghan. To quickly check, you can try a python script which uses functions from the Atomic Simulation Environment (ASE) collection of tools based on Python3. 

 ````{tabs}
  ```{group-tab} Tetralith
  First, we need to load ASE and a suitable Python3 module, 

      module load ASE/3.19.0-nsc1
      module load Python/3.6.3-anaconda-5.0.1-nsc1

  ```
  ```{group-tab} MeluXina
  Using py4vasp, ASE is already included as a dependency and therefore directly available. However, since the terminal was used for running VASP interactively, meaning that a different set of modules were loaded with `source /project/home/p200051/vasp_ws2023/setup.sh`), it will not work immediately in the same terminal. 

   * The fastest way to fix this is to open up a new terminal in Jupyter-notebook for just running ASE in the terminal.

   * Alternatively, load the correct dependecies to use the Python 

         module load Python/3.10.4-GCCcore-11.3.0

     after finishing with ASE, to continue to run VASP interactively, again apply

         source /project/home/p200051/vasp_ws2023/setup.sh
  ```
 ````

As input a file with volume (Å^3) and total energy (eV) is needed. To save some time, there is a script which can be used, so run:

    ./get-vol-etot.sh
    
The bash script "get-vol-etot.sh" looks like

    #!/bin/bash
    for i in  3.5 3.6 3.7 3.8 3.9 4.0 4.1 4.2 4.3 ; do
    #V = `grep volume $i/vasprun.xml | head -1 | awk '{print $3}'`
    cd $i
    V=`awk '/volume/ {print $3; exit}' vasprun.xml`
    E=`awk '/F=/ {print $3}' OSZICAR`  
    echo $V $E  >>../vol_etot.dat
    cd ..
    done    
    
and produces the file "vol_etot.dat". We will use a small python script "eqos.py" which uses ASE and looks like
 
    import numpy
    from ase.units import GPa
    from ase.eos import EquationOfState

    # Read data
    volumes,energies = numpy.loadtxt('vol_etot.dat', unpack=True)

    # Fit EOS
    eos = EquationOfState(volumes,energies, eos='birchmurnaghan')

    # There are several other choices for eos, see doc at:
    # https://wiki.fysik.dtu.dk/ase/ase/eos.html
    # set eos to e.g. birchmurnaghan, sjeos (ASE default), p3

    v0,e0,B = eos.fit()

    print ()
    print ("Equation of state:")
    print ("-------------------")
    print ("E0: %2.6f eV" % (e0))
    print ("V0: %2.6f A^3" % (v0))
    print ("B: %2.6f GPa" % (B/GPa))
    print ()   

run it to calculate the equilibrium volume using an equation of state

    python eqos.py

the output might look like

    Equation of state:
    -------------------
    E0: -4.880229 eV
    V0: 14.546730 A^3
    B: 84.365350 GPa

The EOS methods are expected to work better closer to the equilibrium. The chosen method can be changed by editing `eos='birchmurnaghan'` in the line

    eos = EquationOfState(volumes,energies, eos='birchmurnaghan')

Note that the volume *V0* is for a single atom, so to obtain the lattice constant *a*, one needs to calculate (since there are 4 atoms per fcc cell)

    a = (4 x V0)^1/3

To quickly compute *a*, you might e.g. use python directly in the terminal

    python

and input at the ">>>" prompt

    (4*14.546730) ** (1./3.)

and exit with `ctrl d` (what happens adding 0.7 + 0.6 using python?).

### 3. Calculation

A second static calculation, now using the obtained equilibrium volume. Go to the folder "scf1" which was created previously 

    cd scf1

and insert the lattice parameter **a** obtained in **2.** by editing POSCAR, e.g. with

    vi POSCAR

or use your favourite text editor (`emacs`, `nano`, `gedit`, ...). Finally, submit the job (Tetralith)

    sbatch run.sh

or run it interactively (MeluXina)

    srun --hint=nomultithread -n 8 vasp_std

and compare the total energy with previous results. For example, try

    grep "free  energy" OUTCAR
    grep "free energy" OUTCAR
    grep F= OSZICAR
    cat OSZICAR
    grep F= slurm-JOBID.out
    cat slurm-JOBID.out
    
* Comparing with the EOS result, does it look reasonable?

### Extra tasks

* Try different methods to compute the equilibrium by editing the script "eqos.py"

* Compute the equilibrium volumes for a less dense k-mesh `5 5 5` in KPOINTS and with ENCUT set to ENMIN from POTCAR, and (2) for a denser k-mesh `29 29 29` and with ENCUT = ENMAX x 1.3. Suggestion: create new folders, copy and edit the "run_vol.sh" job script


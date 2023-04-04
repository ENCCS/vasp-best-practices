## cd Si

[Based on the VASP wiki example in this link](https://www.vasp.at/wiki/index.php/Cd_Si)

**Task:** Do a volume relaxation as well as calculate the DOS and bandstructure for cubic diamond (cd) structure Si.

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
 ````{tabs}
  ```{group-tab} Tetralith
      cp -r /software/sse/manual/vasp/training/ws2023/cd_Si .
      cd fcc_Si_DOS

  also copy the latest POTCAR file for Si

      cp /software/sse/manual/vasp/POTCARs/PBE/2015-09-21/Si/POTCAR .

  ```
  ```{group-tab} MeluXina
      cp -r /project/home/p200051/vasp_ws2023/examples/cd_Si .
      cd fcc_Si_DOS

  also copy the latest POTCAR file for Si

      cp /project/home/p200051/vasp_ws2023/vasp/potpaw_PBE.54/Si/POTCAR .
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

* cubic diamond Si with lattice constant 5.5 Å
* fcc cell
* 2 atoms in the cell

INCAR

    System = diamond Si
    
    ISTART = 0 
    ICHARG=2
    ENCUT  =    240
    ISMEAR = 0 
    SIGMA = 0.1

KPOINTS

    k-points
     0
    Monkhorst Pack
     11 11 11
     0  0  0

### 1. Volume relaxation

Here, investigate the total energy as a function of volume in a similar way as for the [fcc Si example](../fcc_Si). There's a job script which can be used "run-vol.sh"

 ````{tabs}
  ```{group-tab} Tetralith
      #!/bin/bash
      #SBATCH -A naiss2023-22-205
      #SBATCH -t 0:30:00
      #SBATCH -n 4
      #SBATCH -J vaspjob

      module load VASP/6.3.0.20012022-omp-nsc1-intel-2018a-eb

      for i in 5.1 5.2 5.3 5.4 5.5 5.6 5.7 ; do
      mkdir -p $i
      cd $i
      cp /software/sse/manual/vasp/POTCARs/PBE/2015-09-21/Si/POTCAR .
      cp /software/sse/manual/vasp/training/ws2023/cd_Si/INCAR .
      cp /software/sse/manual/vasp/training/ws2023/cd_Si/KPOINTS .
      cat >POSCAR <<EOF
      cubic diamond Si
         $i
       0.0    0.5     0.5
       0.5    0.0     0.5
       0.5    0.5     0.0
      Si
        2
      Direct
       -0.125 -0.125 -0.125
        0.125  0.125  0.125
      EOF
      mpprun vasp_std
      E=`awk '/F=/ {print $0}' OSZICAR` ; echo $i $E  >>../SUMMARY.dia
      cd ..
      done

  submit it with

      sbatch run-vol.sh
  ```
  ```{group-tab} MeluXina
      #!/bin/bash

      for i in 5.1 5.2 5.3 5.4 5.5 5.6 5.7 ; do
      mkdir -p $i
      cd $i
      cp /project/home/p200051/vasp_ws2023/vasp/potpaw_PBE.54/Si/POTCAR .
      cp /project/home/p200051/vasp_ws2023/examples/cd_Si/INCAR .
      cp /project/home/p200051/vasp_ws2023/examples/cd_Si/KPOINTS .
      cat >POSCAR <<EOF
      cubic diamond Si
         $i 
       0.0    0.5     0.5
       0.5    0.0     0.5
       0.5    0.5     0.0
      Si
        2
      Direct
       -0.125 -0.125 -0.125
        0.125  0.125  0.125
      EOF
      srun --hint=nomultithread -n 8 vasp_std
      E=`awk '/F=/ {print $0}' OSZICAR` ; echo $i $E  >>../SUMMARY.dia
      cd ..
      done

  run it with

      ./run-vol.sh
  ```
 ````
after some short time, the folders 5.1 - 5.7 with the output should appear and a file "SUMMARY.dia":

    5.1 1 F= -.10233838E+02 E0= -.10233747E+02 d E =-.180914E-03
    5.2 1 F= -.10528200E+02 E0= -.10528187E+02 d E =-.271766E-04
    5.3 1 F= -.10713336E+02 E0= -.10713334E+02 d E =-.215112E-05
    5.4 1 F= -.10806746E+02 E0= -.10806746E+02 d E =-.111754E-06
    5.5 1 F= -.10823085E+02 E0= -.10823085E+02 d E =-.431458E-08
    5.6 1 F= -.10775151E+02 E0= -.10775151E+02 d E =-.205580E-09
    5.7 1 F= -.10673630E+02 E0= -.10673630E+02 d E =-.114038E-10

check it e.g. using gnuplot

    gnuplot
    
and at the prompt type

 ````{tabs}
  ```{group-tab} Tetralith
      plot "SUMMARY.dia" using ($1):($4) w lp
  ```
  ```{group-tab} MeluXina
      set term png
      set output "SUMMARY.dia.png"
      plot "SUMMARY.dia" using ($1):($4) w lp

  Thereafter, open the output file `SUMMARY.fcc.png` in Jupyter-notebook.
  ```
 ````

From the plot one can see that the equilibrium lattice constant is close to a = 5.5 Å.

As in the [previous example](../fcc_Si) compare with an equation of state method, first extract the volume and total energies by running

    ./get-vol-etot.sh

thereafter, use the ASE script "eqos.py"

    python eqos.py

the output might look like

    Equation of state:
    -------------------
    E0: -10.825495 eV
    V0: 40.987525 A^3
    B: 87.612808 GPa

using the Birch-Murnaghan EOS. Similar as before, we quickly compute the lattice constant *a* using python

    python

and input at the ">>>" prompt

    (4*40.987525) ** (1./3.)

* If a cubic diamond unit cell contains 8 atoms, why multiply by 4 when computing the lattice constant above (compare with [fcc Si](../fcc_Si))? Hint: "grep volume OUTCAR"

### 2. Density of states (DOS)

Calculate DOS in a new folder "dos"

    mkdir dos
    cp POSCAR INCAR KPOINTS POTCAR run.sh dos
    cd dos

For a single step calculation, edit INCAR e.g. with `vi` or your text editor of choice, such that it looks like

    System = diamond Si
    
    ISTART = 0 
    ICHARG=2
    ENCUT  =    240
    ISMEAR = -5 
    #SIGMA = 0.1
    LORBIT = 11

thereafter submit the job (Tetralith)

    sbatch run.sh
    
or run interactively (MeluXina)

    srun --hint=nomultithread -n 8 vasp_std

After it finished, check that the output looks fine, e.g. "cat slurm*out" or check output in terminal.

Now use p4vasp or py4vasp to check DOS, similar as was described for [fcc Si DOS](../fcc_Si_DOS)

### 3. Bandstructure

Return to the main example folder "cd_Si" and prepare for a bandstructure calculation

    mkdir band
    cp POSCAR INCAR POTCAR run.sh band
    cd band

we can use the same KPOINTS input file as for the [fcc Si bandstructure](../fcc_Si_bandstructure) example, e.g.

 ````{tabs}
  ```{group-tab} Tetralith
      cp /software/sse/manual/vasp/training/ws2023/fcc_Si_band/KPOINTS .
  ```
  ```{group-tab} MeluXina
      cp /project/home/p200051/vasp_ws2023/examples/fcc_Si_band/KPOINTS .
  ```
 ````
and edit INCAR such that it looks like

    System = diamond Si
    
    ISTART = 0 
    ICHARG=11
    ENCUT  =    240
    ISMEAR = 0 
    SIGMA = 0.1
    LORBIT = 11
    
assuring that `CHGCAR` will be read (ICHARG=11) and same as for DOS, setting LORBIT=11. Submit the job (Tetralith)

    sbatch run.sh

or run interactively (MeluXina)

    srun --hint=nomultithread -n 8 vasp_std

and wait for it to finish. Check that the output looks fine and once again use p4vasp or py4vasp, following the previous example of [fcc Si bandstructure](../fcc_Si_bandstructure).

In addition, test to plot the orbital characters of the bands following the examples (see bottom figures) in the [VASP wiki](https://www.vasp.at/wiki/index.php/Cd_Si). 

### Extra tasks

* Test with other methods for EOS by editing the "eqos.py" script

* Perform the volume relaxation in **1.** with a higher ENCUT in INCAR 


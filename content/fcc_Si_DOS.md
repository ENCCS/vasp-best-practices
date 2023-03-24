## fcc Si DOS 

[Based on the VASP wiki example in this link](https://www.vasp.at/wiki/index.php/Fcc_Si_DOS)

**Task:** Calculation of the density of states (DOS) for fcc Si.
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
A DOS calculation is typically done in two steps: \
(1) a self consistent, static, converged calculation and \
(2) a non-self consistent calculation, using the charge density (CHGCAR) from the first with a denser k-mesh 

Note that

* This approach saves computational time, in particular for large systems
* DOS is only meaningful for static (no structural relaxation) calculations
 
First, copy the example folder which contains some of the VASP input files and useful scripts 

    cp -r /software/sse/manual/vasp/training/ws2023/fcc_Si_DOS .
    cd fcc_Si_DOS

and copy the latest POTCAR file for Si

    cp /software/sse/manual/vasp/POTCARs/PBE/2015-09-21/Si/POTCAR .

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

INCAR

    System = fcc Si

    #ICHARG = 11   # read charge file
    ENCUT = 240
    ISMEAR = -5 
    LORBIT = 11

* [ICHARG](https://www.vasp.at/wiki/index.php/ICHARG)=11, VASP will do a non-self consistent calculation for a fixed charged density read from `CHGCAR`  
* For DOS we want to use the *tetrahedron method + Blöchl corrections* for how to treat partial occupancies of bands, controlled by setting [ISMEAR](https://www.vasp.at/wiki/index.php/ISMEAR)=-5
* [LORBIT](https://www.vasp.at/wiki/index.php/LORBIT) gives output to PROOUT or PROCAR files, also see [RWIGS](https://www.vasp.at/wiki/index.php/RWIGS)
* With LORBIT set, partial charge densities are found in OUTCAR

KPOINTS

    k-points
     0
    Monkhorst Pack
     21 21 21
     0  0  0

* We keep an odd number of k-points in each direction for MP k-mesh -> Gamma centered mesh, also needed for the tetrahedron method
 
### 1a. Calculation from scratch

We can either start completely from scratch, or use the results from the [previous example "fcc Si"](../fcc_Si). For the latter, go to the next section **1b** further below.

Since this is a small system, calculation will be fast independent of the procedure.

From scratch, set up the folder "dos" with all the input files (use `*` or `INCAR POSCAR KPOINTS POTCAR plotdos.sh run.sh`)

    mkdir dos
    mv * dos
    cd dos
    
submit the calculation

    sbatch run.sh

and wait for it to finish. Any interesting messages in `slurm-JOBID.out`?

    cat slurm*.out

### 1b. Calculation from using previous example

If you did the calculations from scratch in **1a**, you can skip this section.

First, create a folder and move the input files for the static self consistent calculation

    mkdir dos
    mv INCAR POSCAR KPOINTS POTCAR plotdos.sh run.sh dos
    cd dos

Now, copy the charge density file CHGCAR from a calculation in the [previous example](../fcc_Si), checking that the path is correct

    cp ../../fcc_Si/3.9/CHGCAR .

Now, edit INCAR (with e.g. `gedit`or use your favourite editor)

    gedit INCAR

such that it looks like

    System = fcc Si

    ICHARG = 11
    ENCUT = 240
    ISMEAR = -5 #tetrahedron
    LORBIT = 11

submit the calculation

    sbatch run.sh

and wait for it to finish. Any interesting messages in `slurm-JOBID.out`?

    cat slurm*.out

### 2. Check the result

To quickly check the resulting DOS, you can use the small script "plotdos.sh" provided with the example, it looks like

    #!/bin/bash

    awk 'BEGIN{i=1} /dos>/,\
                    /\/dos>/ \
                     {a[i]=$2 ; b[i]=$3 ; i=i+1} \
         END{for (j=12;j<i-5;j++) print a[j],b[j]}' vasprun.xml > dos.dat

    ef=`awk '/efermi/ {print $3}' vasprun.xml`

    cat >plotfile <<!
    # set term postscript enhanced eps colour lw 2 "Helvetica" 20
    # set output "optics.eps"
    plot "dos.dat" using (\$1-$ef):(\$2) w lp
    !

    gnuplot -persist plotfile

    # rm dos.dat plotfile 

run it with

    ./plotdos.sh

it produces the two files "dos.dat" and "plotfile", it also automatically starts gnuplot.

For more advanced functionalities and lots of different options, one can instead use `p4vasp`

     module load p4vasp/0.3.30-nsc1
     p4v &

this will open the GUI of p4vasp in your ThinLinc session. If you started p4vasp outside the folder, you'll need to load the `vasprun.xml`output file by selecting File > Load system > step to correct folder and select `vasprun.xml` > press "Ok".

To check the DOS, in the upper menu select "Electronic" and click "DOS + bands".

When the DOS window is shown, you can e.g. select to export the DOS data by clicking "Graph" in the menu bar, selecting the raw data (.dat) option. It's also possible to directly export for use with `XmGrace`(.agr).

### Extra tasks

* Compare DOS for s, p and d states using p4vasp. Select "Electronic" > "Local DOS + bands control"
* Anything interesting about the fcc Si system considering the DOS?

Test to export DOS as a file "dos.agr" and open using XmGrace
    
    module load grace/5.1.25-nsc1-intel-2018a-eb
    xmgrace dos.agr &

* Compare total DOS for using a denser k-mesh (KPOINTS), ENCUT = 1.5 x ENMAX (`grep ENMAX POTCAR`) and PREC=Accurate (INCAR), any difference?


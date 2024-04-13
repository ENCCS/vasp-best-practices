## fcc Si DOS 

[Based on the VASP wiki example in this link](https://www.vasp.at/wiki/index.php/Fcc_Si_DOS)

**Task:** Calculation of the density of states (DOS) for fcc Si.
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
A DOS calculation is typically done in two steps: \
(1) a self consistent, static, converged calculation and \
(2) a non-self consistent calculation, using the charge density (CHGCAR) from the first with a denser k-mesh 

Note that

* This approach saves computational time, in particular for large systems
* DOS is only meaningful for static (no structural relaxation) calculations
 
First, copy the example folder which contains some of the VASP input files and useful scripts 
 ````{tabs}
  ```{group-tab} Tetralith
      cp -r /software/sse2/tetralith_el9/manual/vasp/training/ws2024/fcc_Si_DOS .
      cd fcc_Si_DOS

  also copy the latest POTCAR file for Si

      cp /software/sse2/tetralith_el9/manual/vasp/POTCARs/PBE/2024-03-19/Si/POTCAR .

  ```
  ```{group-tab} LEONARDO
      cp -r /leonardo_scratch/fast/EUHPC_TD02_030/vasp_ws2024/examples/fcc_Si_DOS .
      cd fcc_Si_DOS

  also copy the latest POTCAR file for Si

      cp /leonardo_scratch/fast/EUHPC_TD02_030/vasp_ws2024/potpaw_PBE.64/Si/POTCAR .
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

and wait for it to finish. Any interesting messages in `slurm-JOBID.out` or the output?

    cat slurm*.out

### 1b. Calculation from using previous example

If you did the calculations from scratch in **1a**, you can skip this section.

First, create a folder and move the input files for the static self consistent calculation

    mkdir dos
    mv INCAR POSCAR KPOINTS POTCAR plotdos.sh run.sh dos
    cd dos

Now, copy the charge density file CHGCAR from a calculation in the [previous example](../fcc_Si), checking that the path is correct

    cp ../../fcc_Si/3.9/CHGCAR .

Now, edit INCAR (with e.g. `vi`or use your favourite editor)

    vi INCAR

such that it looks like

    System = fcc Si

    ICHARG = 11
    ENCUT = 240
    ISMEAR = -5 #tetrahedron
    LORBIT = 11

submit the calculation

    sbatch run.sh

and wait for it to finish. Any interesting messages in `slurm-JOBID.out` or output?

    cat slurm*.out

### 2. Check the result

To quickly check the resulting DOS, you can use the small script "plotdos.sh" provided with the example, it looks like

 ````{tabs}
  ```{group-tab} Tetralith
      #!/bin/bash

      awk 'BEGIN{i=1} /dos>/,\
                      /\/dos>/ \
                       {a[i]=$2 ; b[i]=$3 ; i=i+1} \
           END{for (j=12;j<i-5;j++) print a[j],b[j]}' vasprun.xml > dos.dat

      ef=`awk '/efermi/ {print $3}' vasprun.xml`

      cat >plotfile <<EOF
      # set term postscript enhanced eps colour lw 2 "Helvetica" 20
      # set output "optics.eps"
      plot "dos.dat" using (\$1-$ef):(\$2) w lp
      EOF

      gnuplot -persist plotfile
  ```
  ```{group-tab} LEONARDO
      #!/bin/bash

      awk 'BEGIN{i=1} /dos>/,\
                      /\/dos>/ \
                       {a[i]=$2 ; b[i]=$3 ; i=i+1} \
           END{for (j=12;j<i-5;j++) print a[j],b[j]}' vasprun.xml > dos.dat

      ef=`awk '/efermi/ {print $3}' vasprun.xml`

      cat >plotfile <<EOF
      set term png
      set output "optics.png"
      plot "dos.dat" using (\$1-$ef):(\$2) w lp
      EOF

      gnuplot plotfile
  ```
 ````

run it with

    ./plotdos.sh

it produces the two files "dos.dat" and "plotfile", it also automatically starts gnuplot (Tetralith) or produces an image "optics.png" (LEONARDO).

For more advanced functionalities and lots of different options, one can instead use `p4vasp` (Tetralith) or `py4vasp` (Tetralith, local computer)

 ````{tabs}
  ```{group-tab} Tetralith
  Here, an example is made on how to use p4vasp 

      module load p4vasp/0.3.30-nsc1
      p4v &

  this will open the GUI of p4vasp in your ThinLinc session. If you started p4vasp outside the folder, you'll need to load the `vasprun.xml`output file by selecting File > Load system > step to correct folder and select `vasprun.xml` > press "Ok".

  To check the DOS, in the upper menu select "Electronic" and click "DOS + bands".

  When the DOS window is shown, you can e.g. select to export the DOS data by clicking "Graph" in the menu bar, selecting the raw data (.dat) option. It's also possible to directly export for use with `XmGrace`(.agr).
  ```
  ```{group-tab} LEONARDO
  Copy the output files to your local computer using "scp" and investigate using `py4vasp`. For `p4vasp`, follow Tetralith instructions.

  Here, an example is made on how to use py4vasp. Assuming that a jupyter-notebook is running, from the launcher, select `New` and under `Notebook` select `py4vasp`. At the prompt `In [ ]` you can add commands

      import py4vasp
      mycalc = py4vasp.Calculation.from_path("/path/to/your/calculation/folder/here")
      mycalc.dos.plot()

  To start calculate, press the `Run` button. It might take some time for it to finish, an asterisk will be shown at the prompt `[*]` and the circle after "py4vasp" in the upper right corner will be filled. When finished, hopefully a DOS plot will be seen and a new empty prompt `[ ]` appears further below.

  The DOS plot figure can e.g. be zoomed, downloaded etc. see buttons in the upper right corner of the figure.

  The plot can be updated by changing the commands and press `Run` again.

  ```
 ````

### Extra tasks

* Compare DOS for s, p and d states using p4vasp (select "Electronic" > "Local DOS + bands control") or by using py4vasp, e.g.:

      import py4vasp
      mycalc = py4vasp.Calculation.from_path("/path/to/your/calculation/folder/here")
      mycalc.dos.plot("s,p,d")

* Anything interesting about the fcc Si system considering the DOS?
* Compare total DOS for using a denser k-mesh (KPOINTS), ENCUT = 1.5 x ENMAX (`grep ENMAX POTCAR`) and PREC=Accurate (INCAR), any difference?
* Tetralith: Test to export DOS as a file "dos.agr" and open using XmGrace
    
      module load grace/5.1.25-hpc1-intel-2023a-eb
      xmgrace dos.agr &

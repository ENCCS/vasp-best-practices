## fcc Si bandstructure

[Based on the VASP wiki example in this link](https://www.vasp.at/wiki/index.php/Fcc_Si_bandstructure)

**Task:** Calculation of the bandstructure for fcc Si along [L-Gamma-X-U and K-Gamma symmetry points](https://www.cryst.ehu.es/cgi-bin/cryst/programs/nph-kv-list?gnum=225&fig=fm3qmf&what=data).

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
Note that bandstructure calculations **should** be done in two steps (compare with the [procedure for DOS](../fcc_Si_DOS)): \
(1) a self consistent, static, converged calculation and \
(2) a non-self consistent calculation, using the charge density (CHGCAR) from the first, with k-points selected from an interesting path in the Brillouin zone.

First, copy the example folder which contains some of the VASP input files and useful scripts 
 ````{tabs}
  ```{group-tab} Tetralith
      cp -r /software/sse/manual/vasp/training/ws2023/fcc_Si_band .
      cd fcc_Si_band

  also copy the latest POTCAR file for Si

      cp /software/sse/manual/vasp/POTCARs/PBE/2015-09-21/Si/POTCAR .

  ```
  ```{group-tab} MeluXina
      cp -r /project/home/p200051/vasp_ws2023/examples/fcc_Si_band .
      cd fcc_Si_band

  also copy the latest POTCAR file for Si

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

INCAR

    System = fcc Si

    ICHARG = 11  #read charge file
    ENCUT = 240
    ISMEAR = 0
    SIGMA = 0.1
    LORBIT = 11

* [ICHARG](https://www.vasp.at/wiki/index.php/ICHARG)=11, perform a static calculation reading CHGCAR
* [ISMEAR](https://www.vasp.at/wiki/index.php/ISMEAR)=0, for bandstructure calculation

KPOINTS

    k-points for bandstructure L-Gamma-X-U K-Gamma
     10
    line
    reciprocal
      0.50000  0.50000  0.50000    1 !L
      0.00000  0.00000  0.00000    1 !Gamma

      0.00000  0.00000  0.00000    1 !Gamma
      0.00000  0.50000  0.50000    1 !X

      0.00000  0.50000  0.50000    1 !X
      0.25000  0.62500  0.62500    1 !U

      0.37500  0.7500   0.37500    1 !K
      0.00000  0.00000  0.00000    1 !Gamma

* k-points along the line L - Gamma - X - U and K - Gamma
* 10 points per line
* Keyword *line* to generate bandstructure
* Reciprocal coordinates
* All points with weight 1

 
### Calculation

Here we'll assume that the first self consistent, static, step is done in the [previous fcc Si example](../fcc_Si). Now perform a non-self consistent calculation, to do that copy `CHGCAR` from the previous example, e.g.

    cp ../fcc_Si/3.9/CHGCAR .
    
and submit the job to the queue

    sbatch run.sh

when the job has finished, check slurm-JOBID.out

    cat slurm*.out


 ````{tabs}
  ```{group-tab} Tetralith
  Plot the bandstructure using p4vasp

      p4v &

  and select: Electronic > DOS+bands > Show > Bands. As in the case of DOS, it's possible to save the data by selecting Graph > Export, to e.g. raw data or an XmGrace file (.agr).
  ```
  ```{group-tab} MeluXina
  Plot the bandstructure using py4vasp via the Jupyter-notebook

      import py4vasp
      mycalc = py4vasp.Calculation.from_path("/path/to/your/calculation/folder/here")
      mycalc.band.plot()
  ```
 ````
Compare with the figure shown in the [VASP wiki example](https://www.vasp.at/wiki/index.php/Fcc_Si_bandstructure).

### Extra tasks

* Have a look at the paths in the Brillouin zone for fcc by using the [Bilbao crystallographic server](https://www.cryst.ehu.es/), select: Space-group symmetry > KVEC > enter "225" for space group > Brillouin zone
* Tetralith: test to plot bandstructure also using py4vasp

## Bandgap of Si using different DFT+HF methods

[Based on the VASP wiki example in this link](https://www.vasp.at/wiki/index.php/Bandgap_of_Si_using_different_DFT%2BHF_methods)

**Task:** Calculate the bandgap of Si using different DFT+HF schemes: PBE, B3LYP, PBE0, HSE06 and HF.

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

First, copy the example folder which contains some of the VASP input files and useful scripts
 ````{tabs}
  ```{group-tab} Tetralith
      cp -r /software/sse2/tetralith_el9/manual/vasp/training/ws2024/bandgap_Si .
      cd bandgap_Si

  and copy the latest POTCAR file for Si

      cp /software/sse2/tetralith_el9/manual/vasp/POTCARs/PBE/2024-03-19/Si/POTCAR .
  ```
  ```{group-tab} LEONARDO
      cp -r /leonardo_scratch/fast/EUHPC_D02_030/vasp_ws2024/examples/bandgap_Si .
      cd bandgap_Si

  and copy the latest POTCAR file for Si

      cp /leonardo_scratch/fast/EUHPC_D02_030/vasp_ws2024/potpaw_PBE.64/Si/POTCAR .
  ```
 ````

### Input files

POSCAR

    System: Si                             
     5.430 
     0.5 0.5 0.0
     0.0 0.5 0.5
     0.5 0.0 0.5
    Si
       1  
    Cartesian
    0    0    0
    0.25 0.25 0.25

INCAR

    ## Better preconverge with PBE first
    ## and use the WAVECAR file as inout for the DFT+HF calculation
   
    ## Selects the B3LYP hybrid function
    #LHFCALC = .TRUE. ; GGA = B3 ; AEXX = 0.2 ; AGGAX = 0.72 
    #AGGAC = 0.81 ; ALDAC = 0.19
    #ALGO = D ; TIME = 0.4 
   
    ## Selects the PBE0  hybrid function
    #LHFCALC = .TRUE. ; 
    #ALGO = D ; TIME = 0.4 
   
    ## Selects the HSE06 hybrid function
    #LHFCALC = .TRUE. ; HFSCREEN = 0.2 ; 
    #ALGO = D ; TIME = 0.4 
   
    ## Selects HF 
    #LHFCALC = .TRUE. ; AEXX = 1.0 ; ALDAC = 0.0 ; AGGAC = 0
    #ALGO = D ; TIME = 0.4 
   
    ## Leave this in
    ISMEAR =  0
    SIGMA  =  0.01
    GGA    = PE

* This INCAR will run a standard PBE calculation, since all DFT+HF methods are commented out 

KPOINTS

    k-points
    0
    Gamma
      6  6  6
      0  0  0

* Gamma (G) k-mesh -> gamma point included by default

### Calculations

First, run the regular PBE calculation which will be used as a start for the DFT+HF methods by submitting the job 

    sbatch run.sh

When it's finished, cycle through the different DFT+HF methods, don't forget to copy `WAVECAR`

    mkdir B3LYP
    cp INCAR POSCAR KPOINTS POTCAR run.sh gap.sh WAVECAR B3LYP
    cd B3LYP

edit INCAR such that the method of interest is uncommented, e.g.

    ## Selects the B3LYP hybrid function
    LHFCALC = .TRUE. ; GGA = B3 ; AEXX = 0.2 ; AGGAX = 0.72 
    AGGAC = 0.81 ; ALDAC = 0.19
    ALGO = D ; TIME = 0.4 

* Note the use of [ALGO](https://www.vasp.at/wiki/index.php/ALGO)=Damped or D, for the DFT+HF methods, different from the default ALGO=Normal.

and run the job as before. After it has finished, inspect the output

    cat slurm*out
    cat OSZICAR

to obtain energies for the highest occupied and lowest unoccupied states, run the provided script "gap.sh" in this way

    ./gap.sh OUTCAR
    
The bandgap is then given by: `bandgap = min(cband) - max(vband)`.

In the same way, repeat the calculations for PBE0, HSE06 and HF.

* Compare the results with PBE, how big is the difference?
* Why didn't we explicitly set [ISTART](https://www.vasp.at/wiki/index.php/ISTART)=1 in INCAR in order to continue the calculation? Because, since a WAVECAR was present in the folder, the default is set to ISTART=1 instead of 0. Confirm with "grep ISTART OUTCAR".

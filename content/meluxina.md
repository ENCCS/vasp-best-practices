## For using MeluXina (EuroHPC)

Note that the hands-on part was adjusted to MeluXina from Tetralith. 

### User account and login

### General information
There is detailed [MeluXina user documentation](https://docs.lxp.lu/) available, e.g. on how to connect and use the resources.

### (1) Start an interactive job
Since it's not allowed to load modules and run software on the shared MeluXina login nodes, the hands-on session will use interactive jobs.
Note that text editing (vi, emacs, nano), submitting jobs (sbatch) and checking output with standard command line tools (grep, less, awk) are still possible on the login node.

Let's request an interactive job on a work node

    salloc -A p200051 -p cpu --qos default -N 1 -t 6:00:00

and wait for it to start before going to the next section below. The idea is to use this interactive job for setting everything up in order to run the hands-on examples.

### (2) Set up py4vasp 
py4vasp is a versatile tool for e.g. analysing VASP output. In the hands-on examples, it will mainly be used for plotting density of states and bandstructures.
A Python virtual environment with py4vasp has been prepared. A few extra steps are needed for it to work together with jupyter-notebooks, used in the hands-on sessions.

In the terminal with the interactive job running (see previous section), let's prepare to use py4vasp

    module load Python/3.10.4-GCCcore-11.3.0
    python3 -m ipykernel install --name py4vasp --user

one also needs to fix the "kernel.json" file, at the top of your home folder (type "cd" to get there):

    cd .local/share/jupyter/kernels/py4vasp
    cp /project/home/p200051/vasp_ws2023/kernel.json .

### (3) Starting jupyter-notebook
In the same interactive job as above, load the prepared virtual environment "py4venv" (this assumes that we already loaded the module `Python/3.10.4-GCCcore-11.3.0` in the previous step)

    source /project/home/p200051/vasp_ws2023/py4venv/bin/activate

you will get a prompt which might look like `(py4venv) [u000000@mel0000 ~]$`. Now, start jupyter-notebook with

    jupyter-notebook --no-browser

after some time an output will be shown with a link at the end which can be used for connecting to the jupyter-notebook. **Note: before connecting with your own browser on a local desktop/laptop computer, one first needs to setup port forwarding**.

In a new terminal from your local computer, first login to MeluXina with **port forwarding**, change `u00000` to your username:

    ssh -L 8888:localhost:8888 u000000@login.lxp.lu -p 8822

this connects port 8888 on the local computer to port 8888 on the login node.

Now, in the terminal which was just connected to the login node, set port forwarding between the login and work node, change `mel0000` to the work node name (seen from the prompt in the interactive job):

    ssh -L 8888:localhost:8888 mel0000

Since one needs to use a unique port, 8888 might already be occupied (in such case you'll see a warning), just try another port in the same range (e.g. 8900 etc.).

When the port forwarding is done, the jupyter-notebook can be opended by using the link which contains "localhost" in its name, by pasting it in the local browser. It might look something like

    http://localhost:8888/?token=79453hgs9823gsl9sg3hsekw883qk3s3o3kjgey34kw4ijj3

### (4) Run VASP 
Here we assume that a jupyter-notebook is running on a work node and that it opened up fine in a local browser after fixing the port forwarding.
Terminals can now be opened in its own browser window by pressing the button `New` in the upper right hand side and then `Terminal` in its menu.
Go to the window with the new terminal and load settings for VASP

    source /project/home/p200051/vasp_ws2023/setup.sh

when opening up a new terminal, the same steps need to be applied again for running VASP.

Now, a VASP job can be run directly

    srun -n 8 vasp_std

For this workshop, the approach of running interactively using a terminal via jupyter-notebook is recommended.
This allows to run several terminals (if needed) and py4vasp simultaneously.

For the common use case of running longer production jobs, one would instead typically submit jobscripts to the queue. 

### Run VASP - alternative
It might be enough to shutdown the process and restart it in the browser. Note that it might take some time for the python kernel to finish (if the circle next to its name is filled, it's processing).

In case it fails or is too difficult to get jupyter-notebook working, it is still possible to run the VASP examples directly in the interactive job on the work node, or by submitting jobs to the queue system. An example jobscript can be copied

    cp /project/home/p200051/vasp_ws2023/run.sh .

check it (using e.g. vi) and change if needed, thereafter submit it to the queue

    sbatch run.sh

By saving the output, an analysis could be made e.g. by using tools on a local computer. A basic analysis can also be done by standard command line tools.


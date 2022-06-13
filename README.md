# Brain-inspired spiking neural network controller for a neurorobotic whisker system
Code related to the paper: "Brain-inspired spiking neural network controller for a neurorobotic whisker system" by Alberto Antonietti, Alice Geminiani, Edoardo Negri, Egidio D'Angelo, Claudia Casellato*, and Alessandra Pedrocchi*. _Front. Neurorobot._ 16:817948. doi: [10.3389/fnbot.2022.817948.](https://doi.org/10.3389/fnbot.2022.817948)

## Organization of the repository
- `./` The main folder contains all the files that are needed to clone the experiment in the NRP (NeuroRobotics Platform) of the Human Brain Project.
- `mouse/` contains the 3D model of the modified robot mouse
- `data/` contains the data coming from the 10 experiments performed for Control and L7-PP2B groups
  - `Control/` contains the data for the 10 Control simulations (sub-folders `0-9`), each one contains the data of a single simulation
  - `L7-PP2B/` contains the data for the 10 Knock-out simulations (sub-folders `0-9`), each one contains the data of a single simulation
  - `Generate_Figures.ipynb` is the Jupyter Notebook that can be used to generate the figures of the paper and the data reported.

## Software used and library versions
For the simulations, we have used a local installation of the NRP version 3.1, exploiting Python 3.8 (RRID:SCR_008394), Gazebo 11, and ROS Noetic.
The simulation has been done with NEST. We used NEST 2.18 (RRID:SCR_002963), interfaced through PyNN 0.9.5 (RRID:SCR_002963).
All the simulations have been carried out on a Desktop PC provided with Intel Core i7-2600 CPU @ 3.40 GHz and 16 GB of RAM, running 64 bit Ubuntu 20.04.2 LTS.

# How to use this repository

## Recreate the figures of the paper
**Target**: all users, no experience needed

Following these steps, you can recreate all the figures and data that we have reported in the paper. In addition to ensuring methods reproducibility (see the definition [here](https://www.frontiersin.org/articles/10.3389/fninf.2017.00076/full)), this allows you to explore the data in an interactive way.

The process is very simple, everything you need to do is:
1) Clone or download the repository
2) Run the notebook `Generate_Figures.ipynb` using Jupyter [here a guide for beginners](https://jupyter-notebook-beginner-guide.readthedocs.io/en/latest/)

## Reuse the whisker system model in your experiment
**Target**: expert NRP users

You can re-run the virtual experiment or reuse the components we have developed (i.e., the mouse robot model provided with the four whiskers, the control system, the transfer functions, or the state machine).

Here we provide all the files that are needed, however this is not a straightforward process and some previous experience with the NRP is a pre-requisite.
If you are totally new to the NRP, we suggest to follow the [tutorials for beginners](https://neurorobotics.net/Documentation/latest/nrp/tutorials.html) first.

1) **The first step is to install the NRP.** You can find all information on how to download and install a local version of the NRP [here](https://neurorobotics.net/access-the-nrp.html). We recommend to use the [docker installation](https://neurorobotics.net/Documentation/latest/nrp/user_manual/docker_installation.html#docker-installation), since it facilitates a lot the procedure. Remember that the system has been developed and tested with the NRP version 3.1 and version 3.2.
2) Once you have your docker version of the NRP, you can **import the experiment**. To do so, you need to:
    - Download as zip this repository
    - Open the NRP
    - Go to "My experiments"
    - Click on "Import zip" and select the repository zip file you have downloaded
    - You will see the messagge "1 successfully imported zip files"
    - You will see the experiment called "Whisking experiment" in your experiments list
    - You can launch the experiment and modify it as it pleases you or re-use components (i.e., the various Python files that are contained) to generate the experiment that you prefer.

For any problem, do not hesitate to open an Issue in this repository.

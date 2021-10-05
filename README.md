# Brain-inspired spiking neural network controller for a neurorobotic whisker system
Code related to the paper: "Brain-inspired spiking neural network controller for a neurorobotic whisker system" by Alberto Antonietti, Alice Geminiani, Edoardo Negri, Egidio D'Angelo, Claudia Casellato*, and Alessandra Pedrocchi*. Under review.

## Organization of the repository
- `./` The main folder contain all the files that are needed to clone the experiment in the NRP (NeuroRobotics Platform) of the Human Brain Project.
- `mouse/` contains the 3D model of the modified robot mouse
- `data/` contains the data coming from the 10 experiments performed for Control and L7-PP2B groups
  - `Control/` contains the data for the 10 Control simulations (sub-folders 0-9), each one contains the data of a single simulation
  - `L7-PP2B/` contains the data for the 10 Knock-out simulations (sub-folders 0-9), each one contains the data of a single simulation
  - `Generate_Figures.ipynb` is the Jupyter Notebook that can be used to generate the figures of the paper and the data reported.

## Software used and library versions
For the simulations, we have used a local installation of the NRP version 3.1, exploiting Python 3.8 (RRID:SCR_008394), Gazebo 11, and ROS Noetic.
The simulation has been done with NEST. We used NEST 2.18 (RRID:SCR_002963), interfaced through PyNN 0.9.5 (RRID:SCR_002963).
All the simulations have been carried out on a Desktop PC provided with Intel Core i7-2600 CPU @ 3.40 GHz and 16 GB of RAM, running 64 bit Ubuntu 20.04.2 LTS.

You can find all information on how to download and install a local version of the NRP [here](https://neurorobotics.net/access-the-nrp.html).



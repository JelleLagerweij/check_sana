# Project Goal
To check how sanas code computes hydrogen bonding in relation with pbc and shifted boxes.

## Python

The python code reads a .xyz file, shifts it by half the box size, wraps it back to fit pbc and writes it out.
Run the python file the following way:
```shell
python shift_save.py <boxsize> <inputfile> <outputfile>
```

for the given .xyz file, the following code can be ran:
```shell
python shift_save.py 14.899721 traj1.xyz traj2.xyz
```


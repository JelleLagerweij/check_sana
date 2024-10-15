# Project Goal
To check how sanas code computes hydrogen bonding in relation with pbc and shifted boxes.

## Python Running and Requirements

The python code reads a .xyz file, shifts it by half the box size, wraps it back to fit pbc and writes it out.
Run the python file the following way:
```shell
python shift_save.py <boxsize> <inputfile> <outputfile>
```

for the given .xyz file, the following code can be ran:
```shell
python shift_save.py 14.899721 traj1.xyz traj2.xyz
```

For the python environment, the following is advised:

```shell
python -m venv .venv
source .venv/bin/activate
pip install --upgrade ase
```

Checking the install
```shell
pip list
```

should show something similar to

```shell
Package         Version
--------------- -----------
ase             3.23.0
contourpy       1.3.0
cycler          0.12.1
fonttools       4.54.1
kiwisolver      1.4.7
matplotlib      3.9.2
numpy           2.1.2
packaging       24.1
pillow          10.4.0
pip             22.0.2
pyparsing       3.2.0
python-dateutil 2.9.0.post0
scipy           1.14.1
setuptools      59.6.0
six             1.16.0
```
## Running GATeWAY
A by Jelle compiled GATeWAY version is used to run, however unadjusted versions should result in the same.
Run GATeWAY as:

```shell
/path/to/GATeWAY/bin/interface -w <inputfile> -x <boxsize x> -y <boxsize y> -z <boxsize z> -d <number of bonds to analyze>
```

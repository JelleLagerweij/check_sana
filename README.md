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
pip install pandas
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
pandas          2.2.3
pillow          10.4.0
pip             22.0.2
pyparsing       3.2.0
python-dateutil 2.9.0.post0
pytz            2024.2
scipy           1.14.1
setuptools      59.6.0
six             1.16.0
tzdata          2024.2
```

## Running GATeWAY

A by Jelle compiled GATeWAY version is used to run, however unadjusted versions should result in the same.
Run GATeWAY as:

```shell
/path/to/GATeWAY/bin/interface -w <inputfile> -x <boxsize x> -y <boxsize y> -z <boxsize z> -d <number of bonds to analyze>
```

In this case, the correct run would be:

```shell
/path/to/GATeWAY/bin/interface -w traj1.xyz -x 14.899721 -y 14.899721 -z  14.899721 -d 7
rm -f graph*
/path/to/GATeWAY/bin/interface -w traj2.xyz -x 14.899721 -y 14.899721 -z  14.899721 -d 7
rm -f graph*
```

this results into:
```shell
nb_steps=50
    50 / 50
Statistics for traj1.xyz
Number of conformations is 50
Average of water molecules total 110.000000

Average of Hbonds per atom (except hydrogen atoms) = 1.828929

 Running time = 3.642453
The trajectory is analysed with the PBC :x =14.900  y =14.900  z =14.900
nb_steps=50
    50 / 50
Statistics for traj2.xyz
Number of conformations is 50
Average of water molecules total 110.000000

Average of Hbonds per atom (except hydrogen atoms) = 1.800357

 Running time = 3.665786
```

Note that the number of hydrogen bonds per water are different for these tests, however, we know that they should be identical as they contain identical data, just shifted coordinates.
## Checking GATeWAY output with python

The output of gateway can also be compared for only the OH hydrogen bonding.
This can be ran using 

```shell
python test_shift.py <outputfolder1> <outputfolder2>
```

A good example for the run would then be:

```
python test_shift.py traj1 traj2
```

Note that this can result in long list, depending on the length of the trajectory. For 50 snapshots, we get:

```shell
completed comparing 'traj1' and 'traj2'
hbs(0) = '            2'    and   '2'
hbs(1) = '            2'    and   '2'
hbs(2) = '            2'    and   '2'
hbs(3) = '            3'    and   '3'
hbs(4) = '            3'    and   '3'
hbs(5) = '            2'    and   '2'
hbs(6) = '            2'    and   '2'
hbs(7) = '            2'    and   '2'
hbs(8) = '            2'    and   '2'
hbs(9) = '            2'    and   '2'
hbs(10) = '            2'    and   '2'
hbs(11) = '            2'    and   '2'
hbs(12) = '            2'    and   '2'
hbs(13) = '            2'    and   '2'
hbs(14) = '            2'    and   '2'
hbs(15) = '            2'    and   '2'
hbs(16) = '            2'    and   '2'
hbs(17) = '            2'    and   '2'
hbs(18) = '            2'    and   '2'
hbs(19) = '            2'    and   '2'
hbs(20) = '            2'    and   '2'
hbs(21) = '            2'    and   '2'
hbs(22) = '            2'    and   '2'
hbs(23) = '            2'    and   '2'
hbs(24) = '            2'    and   '2'
hbs(25) = '            2'    and   '2'
hbs(26) = '            2'    and   '2'
hbs(27) = '            2'    and   '1'
hbs(28) = '            2'    and   '2'
hbs(29) = '            2'    and   '1'
hbs(30) = '            2'    and   '2'
hbs(31) = '            2'    and   '1'
hbs(32) = '            2'    and   '2'
hbs(33) = '            2'    and   '2'
hbs(34) = '            2'    and   '2'
hbs(35) = '            2'    and   '2'
hbs(36) = '            2'    and   '2'
hbs(37) = '            2'    and   '2'
hbs(38) = '            2'    and   '2'
hbs(39) = '            2'    and   '2'
hbs(40) = '            2'    and   '2'
hbs(41) = '            2'    and   '2'
hbs(42) = '            2'    and   '2'
hbs(43) = '            2'    and   '2'
hbs(44) = '            2'    and   '2'
hbs(45) = '            2'    and   '2'
hbs(46) = '            2'    and   '2'
hbs(47) = '            2'    and   '2'
hbs(48) = '            2'    and   '2'
hbs(49) = '            2'    and   '2'
```

Here some of the outpus do show a difference between the two. Look at timestep 27, 31. Although not to bad, there seem to be some inconsistency. Besdes that, the hydrogenbonding number is much lower than expected from other methods. (TODO JELLE)

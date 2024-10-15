"""
This python code contains a simple comparrison class to compare two GATeWAY output folders.
"""

import os
import argparse
import shutil
import tempfile
import subprocess
from typing import List
import numpy as np
import pandas as pd

class Gateway:
    """
    Gateway class to filter GATeWAY output and only get the for Jelle relevant parts
    """
    def __init__(self, name : str):
        # read the gateway output files
        self.oh_list = self.grep_fast_filter(name + "/" + name +
                                             "_OH_stats.txt", r"\s1\s*$", cols=[0, 2])
        self.hb_list = self.grep_fast_filter(name+ "/" + name +
                                             "_HBs_stats.txt", r"\bwp\b", cols=[0, 1, 2])
        self.check_timsteps()

    def grep_fast_filter(self, filename: str, pattern: str, cols: List[int]) -> np.ndarray:
        """ 
        Runs the grep of ripgrep commands to filter files efficiently.
        Utelyzes system memory to be fast
        """
        # Check if 'rg' is availab
        rg_available = shutil.which('rg') is not None

        # Construct the command based on availability
        if rg_available:
            command = ['rg', '-N', pattern, os.path.join(filename)]
        else:
            command = ['grep', pattern, os.path.join(filename)]

        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError as e:
            # Handle the error here
            print(f"Command failed with return code {e.returncode}")
            print(f"Error output: {e.stderr}")
            raise RuntimeError(f"Error running {' '.join(command)}") from e

        max_size = 1024 * 1024 * 1024  # 1GB in bytes
        with tempfile.SpooledTemporaryFile(mode='w+', max_size=max_size) as temp_file:
            # Write the result to the temporary file
            temp_file.write(result.stdout)
            temp_file.seek(0)  # Rewind the file to the beginning
            # Read the tempfile into a pandas DataFrame
            df = pd.read_csv(temp_file, sep=r'\s+', header=None, usecols=cols)
            # Convert DataFrame to NumPy array
            array = df.to_numpy()
        return array

    def check_timsteps(self):
        """
        Checks every timestep what the number of hbonds is and
        mustates the class with the updated result.
        """
        unique_timesteps, start_indices = np.unique(self.oh_list[:, 0], return_index=True)
        end_indices = np.r_[start_indices[1:], len(self.oh_list)]
        n_max = unique_timesteps.shape[0]

        self.n_hb = np.zeros(n_max, dtype=int)  # number of hydrogen bonds
        self.i_oh = np.zeros_like(self.n_hb) # index of OH-
        self.n_oh = np.zeros_like(self.n_hb) # number of OH-

        last_oh = None
        for t in unique_timesteps:
            oh_indices = self.oh_list[start_indices[t]:end_indices[t], 1]

            self.n_oh[t] = oh_indices.shape[0]
            # determine OH-
            if self.n_oh[t] == 1:
                # only 1 oh to deal with
                self.i_oh[t] = oh_indices[0]
            else:
                # if more then 1
                if (last_oh in oh_indices) or (self.n_oh[t] == 0):
                    # take same as last one
                    self.i_oh[t] = last_oh
                else:
                    # or take just the first of the list
                    self.i_oh[t] = oh_indices[0]

            last_oh = self.i_oh[t]
            # Create mask to count hydrogen bonds

            self.n_hb[t] = np.count_nonzero(self.hb_list[:, 0] == t)

if __name__ == "__main__":
    # Parse inputs and provie error messaging when wrong inputs are used.
    parser = argparse.ArgumentParser(description='postprocesses two GATeWAY outputs and compares')
    parser.add_argument('inputfolder1', type=str, help='Name of first inputfolder, should be ' +
                        'GATeWAY output folder')
    parser.add_argument('inputfolder2', type=str, help='Name of second inputfolder, should be ' +
                        'GATeWAY output folder')

    args = parser.parse_args()

    # postprocess both outputs
    version1 = Gateway(args.inputfolder1)
    version2 = Gateway(args.inputfolder2)

    # print results to compare
    print(f"completed comparing '{args.inputfolder1}' and '{args.inputfolder2}'")
    for t in range(min(version1.n_hb.shape[0], version2.n_hb.shape[0])):
        print(f"hbs({t}) = '            {version1.n_hb[t]}'    and   '{version2.n_hb[t]}'")

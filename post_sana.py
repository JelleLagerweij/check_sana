import os
import sys
import shutil
import tempfile
import subprocess
import h5py # pandas
from typing import List, Tuple
import numpy as np
import pandas as pd

class Gateway:
    def __init__(self, folder, name, verbose=False):
        self.folder = self.process_path(folder)

        # read the gateway output files
        self.oh_list = self.grep_fast_filter(name + "_OH_stats.txt", r"\s1\s*$", cols=[0, 2])
        self.hb_list = self.grep_fast_filter(name +"_HBs_stats.txt", r"\bwp\b", cols=[0, 1, 2])
        self.check_timsteps()

    def process_path(self, folder: str) -> str:
        # Construct the full path correctly
        folder = os.path.join(os.getcwd(), folder)
        return folder

    def grep_fast_filter(self, filename: str, pattern: str, cols: List[int]) -> np.ndarray:
        # Construct the command to run repgrep without line number output

        # Check if 'rg' is availab
        rg_available = shutil.which('rg') is not None

        # Construct the command based on availability
        if rg_available:
            command = ['rg', '-N', pattern, os.path.join(self.folder, filename)]
        else:
            command = ['grep', pattern, os.path.join(self.folder, filename)]
        result = subprocess.run(command, capture_output=True, text=True)

        # Debug: Print error output if the command failed
        if result.returncode != 0:
            print(f"Command failed with return code {result.returncode}")
            print(f"Error output: {result.stderr}")
            raise RuntimeError(f"Error running {' '.join(command)}")

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


a = Gateway('origional', name="traj_unprocessed_wrapped")
b = Gateway('recentered', name="traj_unprocessed_wrapped")

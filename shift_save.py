#!/mnt/c/Users/vlagerweij/Documents/TU jaar 6/Project KOH(aq)/Progress_meeting_23/New folder/origional/sana_test/.venv/bin/python
"""
This code 

"""
import argparse
from typing import List
from ase import io, Atoms


def validate_filename(filename : str) -> str:
    """Check if filename ends with .xyz"""
    if not filename.endswith('.xyz'):
        raise argparse.ArgumentTypeError(f"file '{filename}' has to have a .xyz extension.")
    return filename


def read_file(inputfile : str) -> List[Atoms]:
    """Reads the .xyz file to extract types and coordinates"""
    try:
        frames = io.read(inputfile, format='xyz', index=':')
    except Exception as e:
        raise RuntimeError(f"Failed to read the file '{inputfile}'") from e
    return frames


def shift_positions(lbox : float, frames : List[Atoms]) -> List[Atoms]:
    """Shifts the box in such a way that atom n is the one shifted back
    to 0, 0, 0"""
    i = 0
    for frame in frames:
        if i > frame.positions.shape[0]:
            i = 0
        shift = - frame.positions[i]
        frame.positions += shift  # occurs on all indexes of the array
        frame.positions = frame.positions % lbox  # wrapps all back to fit in the pbc box
        i += 1
    return frames


def save_file(outputfile : str, frames : List[Atoms]):
    """Writes outputfile from by half the boxsize shifted inputfile"""
    try:
        io.write(outputfile, frames, format='xyz')
    except Exception as e:
        raise RuntimeError(f"Failed to save the file '{outputfile}'") from e


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Processes an xyz file by shifting it and "+
                                     "saves the output file. It uses the boxsize, input" +
                                     "filename and output file name")

    # Add parser inputs
    parser.add_argument('lbox', type=float, help='boxsize in Angstrom.')
    parser.add_argument('inputfile', type=validate_filename, help='Input file name.')
    parser.add_argument('outputfile', type=validate_filename, help='Output file name.')

    args = parser.parse_args()

    configuration = read_file(args.inputfile)
    configuration = shift_positions(args.lbox, configuration)
    save_file(args.outputfile, configuration)

    # Indicate successful completion of the processing
    print(f"Processing completed successfully, outputfile '{args.outputfile}' written.")

#!/mnt/c/Users/vlagerweij/Documents/TU jaar 6/Project KOH(aq)/Progress_meeting_23/New folder/origional/sana_test/.venv/bin/python
"""
This code 

"""
import argparse
from ase import io, Atoms


def validate_filename(filename : str) -> str:
    """Check if filename ends with .xyz"""
    if not filename.endswith('.xyz'):
        raise argparse.ArgumentTypeError(f"file '{filename}' has to have a .xyz extension.")
    return filename


def read_file(inputfile : str) -> Atoms:
    """Reads the .xyz file to extract types and coordinates"""
    try:
        atoms = io.read(inputfile)
    except Exception as e:
        raise RuntimeError(f"Failed to read the file '{inputfile}'") from e
    return atoms


def shift_positions(lbox : float, atoms : Atoms) -> Atoms:
    """Shifts the box by half a boxsize in all directions,
    but wrapps all back to periodic boundary conditions."""
    shift = lbox/2

    atoms.positions += shift  # occurs on all indexes of the array
    atoms.positions = atoms.positions % lbox  # wrapps all back to fit in the pbc box using modulus
    return atoms


def save_file(outputfile : str, atoms : Atoms):
    """Writes outputfile from by half the boxsize shifted inputfile"""
    try:
        io.write(outputfile, atoms)
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

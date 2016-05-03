#!/usr/bin/env python
"""
Call CORSIKA with the IACT package in a thread safe way

Usage: corsika_iact -c=CORSIKA_EXECUTABLE_PATH -i=INPUT_CARD_PATH [-s]

Options:
    -c --corsika_path=CORSIKA_EXECUTABLE_PATH   Path to corsika executable
    -i --input_card_path=INPUT_CARD_PATH        Path to corsika input card
    -s --save_stdout                            Saves stdout and stderr next to output

Notes:
    Creates a temporary working directory for corsika in the output path.
    Gives temporary working directory 6 random digits in its name.
    Symlinks all Corsika and IACT dependencies into the temporary working directory.
    Calls Corsika in the temporary working directory.
    Removes the temporary working directory.
    Removes the write protection from the corsika iact output file.
    Optionally saves the stdout and stderr of corsika in the output path.
    Returns the corsika return code.

"""
from __future__ import absolute_import, print_function, division

__all__ = ['corsika_iact']

import docopt
import os
from os.path import join
import glob
import subprocess
import sys
import random

def all_files_in(path):
    return glob.glob(join(path, '*'))

def mkdir(path):
    subprocess.call(['mkdir', path])

def rm_dir(path):
    subprocess.call(['rm', '-r', path])

def symlink(src, dest):
    subprocess.call(['ln', '-s', src, dest])

class Path:
    def __init__(self, path):
        self.path = path
        self.basename = os.path.basename(self.path)
        self.basename_wo_extension = os.path.splitext(self.basename)[0]
        self.dirname = os.path.dirname(self.path)

def supposed_to_store_output_path(line):
    if line[0:6] == 'TELFIL':
        return True
    else:
        return False

def extract_output_path_from(line):
    first_quote = line.find('"')
    second_quote = line[first_quote+1:].find('"') + first_quote+1
    return line[first_quote+1:second_quote]

def output_path_taken_from_corsika_input_card(input_card_path):
    with open(input_card_path) as fileobject:
        for line in fileobject:
            if supposed_to_store_output_path(line):
                return extract_output_path_from(line)

def corsika_iact(corsika_path, input_card_path, save_stdout=False):
    """
    Call CORSIKA with the IACT package in a thread safe way

    Parameters
    ----------
    corsika_path : string
        Path to the corsika executable
       
    input_card_path : string    
        Path to the corsika input card

    save_stdout : bool [optional]
        Saves stdout and stderr next to output

    Returns
    -------
    int
        the return value of the CORSIKA executable

    Examples
    --------
        import corsika_iact_caller as cic 
        cic.corsika_iact_call(
            '/home/user/corsika/corsika-74005/run/corsika74005Linux_QGSII_urqmd',
            '/home/user/corsika/corsika_input_card.txt'
        )

    Notes
    -----
        This CORSIKA call wrapper demands CORSIKA beeing build with the IACT
        package by Konrad Bernlohr.
    """
    corsika_path = os.path.abspath(corsika_path)
    input_card_path = os.path.abspath(input_card_path)

    corsika = Path(corsika_path)
    out = Path(output_path_taken_from_corsika_input_card(input_card_path))

    temp_working_dir = out.basename_wo_extension+'_temp_'+str(random.randint(0,1e6))
    
    if join(out.dirname, temp_working_dir) not in all_files_in(out.dirname):
        mkdir(join(out.dirname, temp_working_dir))


        # symlink all Corsika relevant files to temp working dir
        for f in all_files_in(corsika.dirname):
            ff = Path(f)
            symlink(
            	join(ff.dirname, ff.basename), 
                join(out.dirname, temp_working_dir, ff.basename)
            )

        # symlink all IACT Corsika relevant files to temp working dir
        corsika_main_path = os.path.split(corsika.dirname)[0]
        corsika_iact_path = join(corsika_main_path, 'bernlohr')
        
        for iact_path in all_files_in(corsika_iact_path):
            iact_file = Path(iact_path)
            if iact_file.basename_wo_extension[0:7] == 'atmprof':
                symlink(
                    join(iact_file.dirname, iact_file.basename), 
                    join(out.dirname, temp_working_dir, iact_file.basename)
                )

        # call corsika in the temporary working diractory and 
        input_card_file = open(input_card_path)

        if save_stdout:
            # pipe the stdout and stderr into files
            corsika_stdout = open(join(out.dirname, out.basename_wo_extension+'_stdout.txt'), 'w')
            corsika_stderr = open(join(out.dirname, out.basename_wo_extension+'_stderr.txt'), 'w')

            corsika_return_value = subprocess.call(
                join(out.dirname, temp_working_dir, corsika.basename), 
                stdin=input_card_file, 
                stdout=corsika_stdout, 
                stderr=corsika_stderr,
                cwd=join(out.dirname, temp_working_dir)
            )

            corsika_stderr.close()
            corsika_stdout.close()
        else:
            corsika_return_value = subprocess.call(
                join(out.dirname, temp_working_dir, corsika.basename), 
                stdin=input_card_file,
                cwd=join(out.dirname, temp_working_dir)
            )

        input_card_file.close()

        # remove the temporary working directory
        rm_dir(join(out.dirname, temp_working_dir))

        # remove write protection from corsika output
        subprocess.call(['chmod', '+w', join(out.dirname, out.basename)])

        return corsika_return_value

def main():
    try:
        arguments = docopt.docopt(__doc__)

        corsika_return_value = corsika_iact(
            corsika_path=arguments['--corsika_path'], 
            input_card_path=arguments['--input_card_path'],
            save_stdout=arguments['--save_stdout']
        )

        sys.exit(corsika_return_value)

    except docopt.DocoptExit as e:
        print(e.message)

if __name__ == '__main__':
    main()

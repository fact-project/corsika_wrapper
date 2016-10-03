"""
Call the KIT CORSIKA simulation

Usage: corsika_iact -i=STEERING_CARD_PATH [-o=OUTPUT_PATH] [-s]
       corsika_iact -c=CORSIKA_EXECUTABLE_PATH
       corsika_iact -w | --which_corsika

Options:
    -i --input_path=STEERING_CARD_PATH          Path to corsika steering card
    -o --output_path=OUTPUT_PATH                Overwrites the output path in 
                                                the steering card
    -s --save_stdout                            Saves stdout and stderr of 
                                                Corsika next to OUTPUT_PATH
    -c --corsika_path=CORSIKA_EXECUTABLE_PATH   Path to the corsika executable
    -w --which_corsika                          Shows which corsika executable 
                                                is used

Notes:
    How?
    ----------
        1st)
            Specify the corsika executable to be used using the -c option.

        2nd)
            Call Corsika with the -i [and -o] options   

    Threadsafe
    ----------
        Each corsika call runs in its own, fully copied, and temporary 'run' 
        directory.

    Easy
    ----------
        The output path can be specified on the command line [-o].
        The output path specified in the steering card will be overwritten. 
        However, the intial steering card remains untouched. 
        Further, the write protection of the output files is removed.
"""
import docopt
import tempfile
import os
import subprocess
import sys
import shutil
from . import tools


def corsika(
    corsika_path, 
    steering_card_path, 
    output_path=None, 
    save_stdout=False):
    """
    Call corsika in a threadsafe way

    Parameters
    ----------

        corsika_path                    Path the corsika executable in its 'run'
                                        directory environment

        steering_card_path              Path to the steering card for corsika

        output_path                     Path to the output. This option
                                        overwrites the output path specified in 
                                        the steering card.

        save_stdout                     If True, the std out and std error of 
                                        corsika is written into text files next
                                        to the output_path. 
    """
    steering_card = tools.read_text_file(steering_card_path)

    if output_path is None:
        out = tools.Path(tools.output_path_from_steering_card(steering_card))
    else:
        out = tools.Path(output_path)
        steering_card = tools.overwrite_output_path_in_steering_card(
            steering_card, 
            out.absolute)

    corsika = tools.Path(corsika_path)

    with tempfile.TemporaryDirectory() as temp_path:

        tmp_run = tools.Path(os.path.join(temp_path, 'run'))

        shutil.copytree(
            os.path.dirname(corsika_path), 
            tmp_run.absolute,
            symlinks=False)

        steering_card_pipe, pwrite = os.pipe()
        os.write(pwrite, str.encode(''.join(steering_card)))
        os.close(pwrite)

        if save_stdout:
            corsika_stdout = open(
                os.path.join(
                    out.dirname, 
                    out.basename_without_extension+'_stdout.txt'), 
                'w')
            corsika_stderr = open(
                os.path.join(
                    out.dirname, 
                    out.basename_without_extension+'_stderr.txt'), 
                'w')

            corsika_return_value = subprocess.call(
                os.path.join(tmp_run.absolute, corsika.basename),
                stdin=steering_card_pipe, 
                stdout=corsika_stdout, 
                stderr=corsika_stderr,
                cwd=tmp_run.absolute
            )

            corsika_stderr.close()
            corsika_stdout.close()
        else:
            corsika_return_value = subprocess.call(
                os.path.join(tmp_run.absolute, corsika.basename), 
                stdin=steering_card_pipe,
                cwd=tmp_run.absolute
            )

        # User and group are allowed read and write on the output
        if os.path.isfile(out.absolute):
            os.chmod(out.absolute, 0o664)

    return corsika_return_value


def print_current_config():
    """
    Print the corsika executable path from the config file.
    """
    config = tools.read_config(tools.get_config_file_path())
    print(config['corsika_executable_path'])


def set_corsika_executable_in_config(corsika_path):
    """
    Set the corsika executable path in the config file.
    """
    if not os.path.isdir(tools.get_config_dir_path()):
        os.mkdir(tools.get_config_dir_path())
    config = {'corsika_executable_path': corsika_path}    
    tools.write_config(config, tools.get_config_file_path())
    print_current_config()


def main():
    try:
        arguments = docopt.docopt(__doc__)
        if arguments['--which_corsika']:
            try:
                print_current_config()
            except FileNotFoundError:
                print('No corsika executable specified yet.') 
                print('Use -c to specify the corsika executable')

        elif arguments['--corsika_path']:
            set_corsika_executable_in_config(arguments['--corsika_path'])
        else:
            try:
                config = tools.read_config(tools.get_config_file_path())
            except FileNotFoundError:
                print('No corsika executable specified yet.') 
                print('Use -c to specify the corsika executable')
                return

            corsika_path = config['corsika_executable_path']

            corsika_return_value = corsika(
                corsika_path=corsika_path, 
                steering_card_path=arguments['--input_path'],
                output_path=arguments['--output_path'],
                save_stdout=arguments['--save_stdout'],
            )

            sys.exit(corsika_return_value)

    except docopt.DocoptExit as e:
        print(e)

if __name__ == '__main__':
    main()
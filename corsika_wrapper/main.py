"""
Call the KIT CORSIKA simulation

Usage: corsika -i=STEERING_CARD_PATH [-o=OUTPUT_PATH] [-s]
       corsika -c=CORSIKA_EXECUTABLE_PATH
       corsika -w | --which_corsika

Options:
    -i --input_path=STEERING_CARD_PATH          Path to corsika steering card.
    -o --output_path=OUTPUT_PATH                Overwrites the output path in 
                                                the steering card.
    -s --save_stdout                            Saves stdout and stderr of 
                                                Corsika next to OUTPUT_PATH.
    -c --corsika_path=CORSIKA_EXECUTABLE_PATH   Path to the corsika executable.
    -w --which_corsika                          Shows which corsika executable.
                                                is used.
"""
import docopt
import sys
from . import api

def main():
    try:
        arguments = docopt.docopt(__doc__)
        if arguments['--which_corsika']:
            try:
                print(api.get_corsika_executable_from_config())
            except FileNotFoundError:
                print('No corsika executable specified yet.') 
                print('Use -c to specify the corsika executable')

        elif arguments['--corsika_path']:
            api.set_corsika_executable_in_config(arguments['--corsika_path'])
        else:
            steering_card = api.read_steering_card(arguments['--input_path'])

            corsika_return_value = api.corsika(
                steering_card=steering_card,
                output_path=arguments['--output_path'],
                save_stdout=arguments['--save_stdout'],
            )

            sys.exit(corsika_return_value)

    except docopt.DocoptExit as e:
        print(e)

if __name__ == '__main__':
    main()
import tempfile
import os
import subprocess
import shutil
from . import tools


def corsika(
    steering_card,
    output_path=None,
    save_stdout=False
):
    """
    Call corsika in a threadsafe way.

    Parameters
    ----------
        steering_card           An OrderedDict of strings.

        output_path             [Default None] Overwrites the output-path
                                specified in the steering card.

        save_stdout             [Default False] If True, the stdout and stderr
                                is written into text-files next to output_path.
    """
    # CORSIKA EXECUTABLE PATH
    try:
        config = tools.read_config(tools.get_config_file_path())
        corsika_path = config['corsika_executable_path']
    except FileNotFoundError:
        print('No corsika executable specified yet.')
        print('Use -c to specify the corsika executable')
        raise FileNotFoundError
    corsika_path = os.path.abspath(corsika_path)

    # OUTPUT PATH
    if output_path is None:
        out = tools.Path(tools.output_path_from_steering_card(steering_card))
        modified_steering_card = steering_card
    else:
        out = tools.Path(output_path)
        modified_steering_card = tools.overwrite_output_path_in_steering_card(
            steering_card,
            out.absolute)

    # THREAD SAFE
    with tempfile.TemporaryDirectory(prefix='corsika_') as tmp_dir:

        tmp_run = tools.Path(os.path.join(tmp_dir, 'run'))

        shutil.copytree(
            os.path.dirname(corsika_path),
            tmp_run.absolute,
            symlinks=False)

        steering_card_pipe, pwrite = os.pipe()
        os.write(
            pwrite,
            str.encode(tools.steering_card2str(modified_steering_card)))
        os.close(pwrite)

        if save_stdout:
            corsika_stdout = open(
                os.path.join(
                    out.dirname,
                    out.basename+'.stdout'),
                'w')
            corsika_stderr = open(
                os.path.join(
                    out.dirname,
                    out.basename+'.stderr'),
                'w')

            corsika_return_value = subprocess.call(
                os.path.join(tmp_run.absolute, os.path.basename(corsika_path)),
                stdin=steering_card_pipe,
                stdout=corsika_stdout,
                stderr=corsika_stderr,
                cwd=tmp_run.absolute
            )

            corsika_stderr.close()
            corsika_stdout.close()
        else:
            corsika_return_value = subprocess.call(
                os.path.join(tmp_run.absolute, os.path.basename(corsika_path)),
                stdin=steering_card_pipe,
                cwd=tmp_run.absolute
            )

        # User and group are allowed to read and write to the output file
        if os.path.isfile(out.absolute):
            os.chmod(out.absolute, 0o664)

    return corsika_return_value


def get_corsika_executable_from_config():
    """
    Returns the corsika executable path from the config file in the user's
    home.
    """
    config = tools.read_config(tools.get_config_file_path())
    return config['corsika_executable_path']


def set_corsika_executable_in_config(corsika_path):
    """
    Sets the corsika executable path in the config file in the user's home.
    """
    if not os.path.isdir(tools.get_config_dir_path()):
        os.mkdir(tools.get_config_dir_path())
    config = {'corsika_executable_path': corsika_path}
    tools.write_config(config, tools.get_config_file_path())
    print(get_corsika_executable_from_config())


def read_steering_card(path):
    """
    Read a corsika steering card text file into a dictionary.

    Returns
    -------
    steering_card       An ordered dictionary of all the keys and values in a
                        CORSIKA steering card. In the CORSIKA steering card,
                        some keys may apear multiple times e.g. SEED or
                        TELESCOPE. Therefore, for each key in the dictionary
                        there is a list of the lines to this key in the
                        steering card.

    Parameters
    ----------
    path                Path to the CORSIKA steering card text file.

    """
    return tools.read_steering_card(path)

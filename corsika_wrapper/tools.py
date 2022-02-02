import os
import json
from collections import OrderedDict
from tempfile import TemporaryDirectory
import signal

from typing import AnyStr


def read_text_file(path):
    with open(path, "r") as myfile:
        text = myfile.readlines()
    return text


def read_steering_card(path):
    lines = read_text_file(path)
    steering_card = OrderedDict()
    for line in lines:
        key_and_value = line.split(' ', 1)
        if len(key_and_value) == 1:
            key = key_and_value[0]
            value = ['']
        else:
            key = key_and_value[0]
            value = [key_and_value[1].strip()]

        if key in steering_card.keys():
            steering_card[key].append(value[0])
        else:
            steering_card[key] = value
    return steering_card


def steering_card2str(steering_card):
    text = ''
    for key in steering_card:
        for value in steering_card[key]:
            if key != 'EXIT':
                text += key+' '+value+'\n'
            else:
                text += key
    return text


def extract_path_from_line(line):
    first_quote = line.find('"')
    if first_quote == -1:
        return None
    second_quote = line[first_quote+1:].find('"') + first_quote+1
    if second_quote == first_quote:
        return None
    return line[first_quote+1:second_quote]


def output_path_from_steering_card(steering_card):
    output_path = None
    for key in steering_card:
        if 'TELFIL' in key:
            output_path = extract_path_from_line(steering_card[key][0])
    print(output_path)
    return output_path


def overwrite_output_path_in_steering_card(steering_card, output_path):
    modified_steering_card = OrderedDict()
    output_path_is_set_in_original_card = False
    for key in steering_card:
        if 'TELFIL' in key:
            modified_steering_card[key] = ['"'+output_path+'"']
            output_path_is_set_in_original_card = True
        elif 'EXIT' in key:
            if not output_path_is_set_in_original_card:
                modified_steering_card['TELFIL'] = ['"'+output_path+'"']
                modified_steering_card[key] = ['']
        else:
            modified_steering_card[key] = steering_card[key]

    return modified_steering_card


def get_config_dir_path():
    home_path = os.path.expanduser("~")
    return os.path.join(home_path, '.corsika_wrapper')


def get_config_file_path():
    return os.path.join(get_config_dir_path(), 'config.json')


def write_config(config, path):
    with open(path, 'w') as outfile:
        json.dump(config, outfile)


def read_config(path):
    config = {}
    with open(path, 'r') as input_file:
        config = json.load(input_file)
    return config


class SignalResistantTemporaryDirectory(TemporaryDirectory):

    signals = {
        signal.SIGINT, 
        signal.SIGTERM,
    }

    def __enter__(self) -> AnyStr:
        def rm_tmp_dir(signum, frame):
            self.cleanup()
            # resetting signal handler to default and reraising it
            signal.signal(signum, signal.SIG_DFL)
            signal.raise_signal(signum)

        # by default, when the program is aborted, /tmp/corsika_?????? dir is left and must be removed manually
        # here we make sure to catch the signals used to interrupt and execute cleanup before exiting
        for s in self.signals:
            signal.signal(s, rm_tmp_dir)

        return super().__enter__()

    def __exit__(self, *exc_args) -> None:
        super().__exit__(*exc_args)
        # resetting signal handler back to defaults
        for s in self.signals:
            signal.signal(s, signal.SIG_DFL)

import os
import json
from collections import OrderedDict


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


def get_home_path():
    return os.path.expanduser("~")


def get_config_dir_path():
    return os.path.join(get_home_path(), '.corsika_wrapper')


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


class Path:
    def __init__(self, path):
        self.absolute = os.path.abspath(path)
        self.basename = os.path.basename(self.absolute)
        self.basename_without_extension = os.path.splitext(self.basename)[0]
        self.dirname = os.path.dirname(self.absolute)

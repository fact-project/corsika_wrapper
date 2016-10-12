import os
import json

def read_text_file(path):
    with open (path, "r") as myfile:
        text = myfile.readlines()
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

    for line in steering_card:
        if 'TELFIL' in line:
            output_path = extract_path_from_line(line)

    return output_path


def overwrite_output_path_in_steering_card(steering_card, output_path):
    modified_steering_card = steering_card.copy()
    output_path_is_set_in_original_card = False
    for i, line in enumerate(steering_card):
        if 'TELFIL' in line:
            modified_steering_card[i] = 'TELFIL'+' "'+output_path+'"\n'
            output_path_is_set_in_original_card = True 

    if not output_path_is_set_in_original_card:
        modified_steering_card.append('TELFIL'+' "'+output_path+'"\n')

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
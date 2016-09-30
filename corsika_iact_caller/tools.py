import os
import glob
import subprocess

def read_text_file(path):
    with open (path, "r") as myfile:
        text = myfile.readlines()
    return text

def extract_path_from(line):
    first_quote = line.find('"')
    if first_quote == -1:
        return None
    second_quote = line[first_quote+1:].find('"') + first_quote+1
    if second_quote == first_quote:
        return None
    print('s', first_quote, 'e', second_quote)
    return line[first_quote+1:second_quote]

def output_path_from_steering_card(steering_card):
    output_path = None

    for line in steering_card:
        if 'TELFIL' in line:
            output_path = extract_path_from(line)

    return output_path

def overwrite_output_path_in_steering_card(steering_card, output_path):

    modified_steering_card = steering_card.copy()

    output_path_is_set_in_original_card = False
    for i, line in enumerate(steering_card):
        if 'TELFIL' in line:
            modified_steering_card[i] = 'TELFIL'+' "'+output_path+'"'
            output_path_is_set_in_original_card = True 

    if not output_path_is_set_in_original_card:
        modified_steering_card.append('TELFIL'+' "'+output_path+'"')

    return modified_steering_card

def all_files_in(path):
    return glob.glob(os.path.join(path, '*'))

#-------------------------------------------------------------------------------

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
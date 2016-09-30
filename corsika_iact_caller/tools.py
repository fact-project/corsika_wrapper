import os
import glob
import subprocess

def read_text_file(path):
    with open (path, "r") as myfile:
        text = myfile.readlines()
    return text

#-------------------------------------------------------------------------------

def all_files_in(path):
    return glob.glob(os.path.join(path, '*'))

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

class CanNotFindTelfilKeyWordInCorsikaInputCard(Exception):
    pass

def output_path_taken_from_corsika_input_card(input_card_path):
    output_path = ""
    found_TELFIL_keyword = False
    with open(input_card_path) as fileobject:
        for line in fileobject:
            if supposed_to_store_output_path(line):
                found_TELFIL_keyword = True
                output_path = extract_output_path_from(line)

    if found_TELFIL_keyword:
        return output_path
    else:
        raise CanNotFindTelfilKeyWordInCorsikaInputCard
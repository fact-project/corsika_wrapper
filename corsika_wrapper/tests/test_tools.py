import pytest
import corsika_wrapper as cw
import tempfile
import os
import pkg_resources


def test_is_install_folder_a_directory():
    assert os.path.isdir(os.path.dirname(cw.__file__))


def test_read_steering_card_lines_as_plain_text():
    print(os.getcwd())
    text = cw.tools.read_text_file(
        pkg_resources.resource_filename(
            'corsika_wrapper', 
            'tests/resources/example_steering_card.txt'))
    assert 'RUNNR' in text[0]
    assert 'EVTNR' in text[1]
    assert 'NSHOW' in text[2]
    assert 'PRMPAR' in text[3]
    assert len(text) == 25


def test_read_output_path_from_line():
    outpath = cw.tools.extract_path_from_line('TELFIL  "my_file.eventio"')
    assert outpath == 'my_file.eventio'


def test_read_output_path_from_line_with_no_string_in_it():
    outpath = cw.tools.extract_path_from_line('MAGNET 30.3 24.1')
    assert outpath is None


def test_read_output_path_from_line_with_broken_string_in_it():
    outpath = cw.tools.extract_path_from_line('TELFIL  "my_file.eventio')
    assert outpath is None

    outpath = cw.tools.extract_path_from_line('TELFIL  my_file.eventio"')
    assert outpath is None


def test_output_path_from_steering_card():
    steering_card = cw.tools.read_steering_card(
        pkg_resources.resource_filename(
            'corsika_wrapper', 
            'tests/resources/example_steering_card.txt'))
    output_path = cw.tools.output_path_from_steering_card(steering_card)
    assert output_path == 'my_file.eventio'


def test_find_EXIT_in_last_entry_of_steering_card():
    steering_card = cw.tools.read_steering_card(
        pkg_resources.resource_filename(
            'corsika_wrapper', 
            'tests/resources/example_steering_card.txt'))
    assert 'EXIT' == next(reversed(steering_card))


def test_overwrite_output_path_in_steering_card():
    steering_card = cw.tools.read_steering_card(
        pkg_resources.resource_filename(
            'corsika_wrapper', 
            'tests/resources/example_steering_card.txt'))

    new_steering_card = cw.tools.overwrite_output_path_in_steering_card(
        steering_card,
        'new/path/for/output.eventio')

    old_output_path = cw.tools.output_path_from_steering_card(steering_card)
    assert old_output_path == 'my_file.eventio'

    new_output_path = cw.tools.output_path_from_steering_card(new_steering_card)
    assert new_output_path == 'new/path/for/output.eventio'


def test_set_output_path_in_steering_card_when_output_not_defined_in_steering_card():
    steering_card = cw.tools.read_steering_card(
        pkg_resources.resource_filename(
            'corsika_wrapper', 
            'tests/resources/example_steering_card_without_output_path.txt'))

    new_steering_card = cw.tools.overwrite_output_path_in_steering_card(
        steering_card,
        'new/path/for/output.eventio')

    old_output_path = cw.tools.output_path_from_steering_card(steering_card)
    assert old_output_path == None

    new_output_path = cw.tools.output_path_from_steering_card(new_steering_card)
    assert new_output_path == 'new/path/for/output.eventio'


def test_config_dict():
    config = {'corsika_executable_path': 'where_ever_you_want'}

    with tempfile.TemporaryDirectory() as temp_path:
        temp_config_path = os.path.join(temp_path, 'config.json')
        cw.tools.write_config(config, temp_config_path)
        read_config = cw.tools.read_config(temp_config_path)

        assert read_config['corsika_executable_path'] == 'where_ever_you_want'


def test_read_steering_card_dict():
    steering_card = cw.tools.read_steering_card(
        pkg_resources.resource_filename(
            'corsika_wrapper', 
            'tests/resources/example_steering_card.txt'))

    assert steering_card['RUNNR'][0] == '1'
    assert steering_card['NSHOW'][0] == '5'
    assert steering_card['PRMPAR'][0] == '1'
    assert steering_card['ESLOPE'][0] == '-2.7'
    assert steering_card['ERANGE'][0] == '5. 50.'
    assert steering_card['THETAP'][0] == '0. 0.'
    assert steering_card['PHIP'][0] == '0. 360.'
    assert steering_card['SEED'][0] == '121 0 0'
    assert steering_card['SEED'][1] == '122 0 0'
    assert steering_card['OBSLEV'][0] == '220000.0'
    assert steering_card['FIXCHI'][0] == '0.'
    assert steering_card['MAGNET'][0] == '30.3 24.1'
    assert steering_card['ELMFLG'][0] == 'T T'
    assert steering_card['MAXPRT'][0] == '1'
    assert steering_card['TELFIL'][0] == '"my_file.eventio"'
    assert steering_card['PAROUT'][0] == 'F F'
    assert steering_card['TELESCOPE'][0] == '0. 0. 0. 250.0'
    assert steering_card['ATMOSPHERE'][0] == '6 N'
    assert steering_card['CWAVLG'][0] == '290 700'
    assert steering_card['CSCAT'][0] == '1 25000.0 0'
    assert steering_card['CERSIZ'][0] == '1'
    assert steering_card['CERFIL'][0] == 'F'
    assert steering_card['TSTART'][0] == 'T'
    assert steering_card['EXIT'][0] == ''

def test_read_steering_card_dict():
    path = pkg_resources.resource_filename(
            'corsika_wrapper', 
            'tests/resources/example_steering_card.txt')
    steering_card = cw.tools.read_steering_card(path)
    steering_card_string = cw.tools.steering_card2str(steering_card)

    raw = ''
    with open (path, "r") as myfile:
        lines = myfile.readlines()
    for line in lines:
        raw+=line

    assert raw == steering_card_string



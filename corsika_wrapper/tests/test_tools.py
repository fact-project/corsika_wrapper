import pytest
import corsika_wrapper as coc
import tempfile
import os
import pkg_resources


def test_is_install_folder_a_directory():
    assert os.path.isdir(os.path.dirname(coc.__file__))


def test_read_steering_card():
    print(os.getcwd())
    text = coc.tools.read_text_file('corsika_wrapper/tests/resources/example_steering_card.txt')
    assert 'RUNNR' in text[0]
    assert 'EVTNR' in text[1]
    assert 'NSHOW' in text[2]
    assert 'PRMPAR' in text[3]
    assert len(text) == 25


def test_read_output_path_from_line():
    outpath = coc.tools.extract_path_from_line('TELFIL  "my_file.eventio"')
    assert outpath == 'my_file.eventio'


def test_read_output_path_from_line_with_no_string_in_it():
    outpath = coc.tools.extract_path_from_line('MAGNET 30.3 24.1')
    assert outpath is None


def test_read_output_path_from_line_with_broken_string_in_it():
    outpath = coc.tools.extract_path_from_line('TELFIL  "my_file.eventio')
    assert outpath is None

    outpath = coc.tools.extract_path_from_line('TELFIL  my_file.eventio"')
    assert outpath is None


def test_output_path_from_steering_card():
    steering_card = coc.tools.read_text_file(
        'corsika_wrapper/tests/resources/example_steering_card.txt')
    output_path = coc.tools.output_path_from_steering_card(steering_card)
    assert output_path == 'my_file.eventio'


def test_overwrite_output_path_in_steering_card():
    steering_card = coc.tools.read_text_file(
        'corsika_wrapper/tests/resources/example_steering_card.txt')

    new_steering_card = coc.tools.overwrite_output_path_in_steering_card(
        steering_card,
        'new/path/for/output.eventio')

    old_output_path = coc.tools.output_path_from_steering_card(steering_card)
    assert old_output_path == 'my_file.eventio'

    new_output_path = coc.tools.output_path_from_steering_card(new_steering_card)
    assert new_output_path == 'new/path/for/output.eventio'


def test_set_output_path_in_steering_card_when_output_not_defined_in_steering_card():
    steering_card = coc.tools.read_text_file(
        'corsika_wrapper/tests/resources/example_steering_card_without_output_path.txt')

    new_steering_card = coc.tools.overwrite_output_path_in_steering_card(
        steering_card,
        'new/path/for/output.eventio')

    old_output_path = coc.tools.output_path_from_steering_card(steering_card)
    assert old_output_path == None

    new_output_path = coc.tools.output_path_from_steering_card(new_steering_card)
    assert new_output_path == 'new/path/for/output.eventio'


def test_config_dict():
    config = {'corsika_executable_path': 'where_ever_you_want'}

    with tempfile.TemporaryDirectory() as temp_path:
        temp_config_path = os.path.join(temp_path, 'config.json')
        coc.tools.write_config(config, temp_config_path)
        read_config = coc.tools.read_config(temp_config_path)

        assert read_config['corsika_executable_path'] == 'where_ever_you_want'
import pytest
import corsika_iact_caller as coc

def test_read_steering_card():
    text = coc.read_text_file('test/resources/example_steering_card.txt')

    assert 'RUNNR' in text[0]
    assert 'EVTNR' in text[1]
    assert 'NSHOW' in text[2]
    assert 'PRMPAR' in text[3] 

def test_read_output_path_from_line():
    outpath = coc.extract_path_from('TELFIL  "my_file.eventio"')
    assert outpath == 'my_file.eventio'

def test_read_output_path_from_line_with_no_string_in_it():
    outpath = coc.extract_path_from('MAGNET 30.3 24.1')
    assert outpath is None

def test_read_output_path_from_line_with_broken_string_in_it():
    outpath = coc.extract_path_from('TELFIL  "my_file.eventio')
    assert outpath is None

    outpath = coc.extract_path_from('TELFIL  my_file.eventio"')
    assert outpath is None

def test_output_path_from_steering_card():
    steering_card = coc.read_text_file(
        'test/resources/example_steering_card.txt')
    output_path = coc.output_path_from_steering_card(steering_card)
    assert output_path == 'my_file.eventio'

def test_overwrite_output_path_in_steering_card():
    steering_card = coc.read_text_file(
        'test/resources/example_steering_card.txt')

    new_steering_card = coc.overwrite_output_path_in_steering_card(
        steering_card,
        'new/path/for/output.eventio')

    old_output_path = coc.output_path_from_steering_card(steering_card)
    assert old_output_path == 'my_file.eventio'

    new_output_path = coc.output_path_from_steering_card(new_steering_card)
    assert new_output_path == 'new/path/for/output.eventio'

def test_set_output_path_in_steering_card_when_output_not_defined_in_steering_card():
    steering_card = coc.read_text_file(
        'test/resources/example_steering_card_without_output_path.txt')

    new_steering_card = coc.overwrite_output_path_in_steering_card(
        steering_card,
        'new/path/for/output.eventio')

    old_output_path = coc.output_path_from_steering_card(steering_card)
    assert old_output_path == None

    new_output_path = coc.output_path_from_steering_card(new_steering_card)
    assert new_output_path == 'new/path/for/output.eventio'

def test_all_files_in_path():
    files = coc.all_files_in('test/resources/')
    assert len(files) == 2
    assert files[0] == 'test/resources/example_steering_card_without_output_path.txt'
    assert files[1] == 'test/resources/example_steering_card.txt'
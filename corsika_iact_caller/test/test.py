import pytest
import corsika_iact_caller as coc
import os

def test_read_steering_card():
    print(os.getcwd())
    text = coc.read_text_file('test/resources/example_steering_card.txt')

    assert 'RUNNR' in text[0]
    assert 'EVTNR' in text[1]
    assert 'NSHOW' in text[2]
    assert 'PRMPAR' in text[3] 
import libcst
import pytest
from pathlib import Path
from renamer.entry import CodeRenamer, ClassOrFuncMover


@pytest.fixture()
def code_renamer():
    code_renamer = CodeRenamer('tests/fixtures/hangman.py')
    return code_renamer


@pytest.fixture()
def class_or_func_mover():
    class_or_func_mover = ClassOrFuncMover('tests/fixtures/hangman.py', 'tests/fixtures/hangman_class.py')
    return class_or_func_mover


def test_rename_func(code_renamer):
    res = code_renamer.rename_variable('start_game', 'run')

    assert res == Path('tests/fixtures/renamed_hangman_func.py').read_text()


def test_rename_class(code_renamer):
    res = code_renamer.rename_variable('Hangman', 'FunnyGame')

    assert res == Path('tests/fixtures/renamed_hangman_class.py').read_text()


def test_move_class(class_or_func_mover):
    moved_element, old_code_without_element = class_or_func_mover.move('Hangman', 'class')

    assert moved_element == Path('tests/fixtures/moved_hangman_class.py').read_text()
    assert old_code_without_element == Path('tests/fixtures/hangman_without_class.py').read_text()


def test_move_func(class_or_func_mover):
    moved_element, old_code_without_element = class_or_func_mover.move('start_game', 'func')

    assert moved_element == Path('tests/fixtures/moved_hangman_func.py').read_text()
    assert old_code_without_element == Path('tests/fixtures/hangman_without_func.py').read_text()



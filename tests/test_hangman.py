from renamer.hangman.hangman import Hangman, choose_word, user_input
import pytest
from datetime import datetime, timedelta


@pytest.fixture(params=['hello', 'hi', 'testing'])
def game_object(request) -> Hangman:
    return Hangman(request.param)


class FkUserInput(object):
    def __init__(self, return_values: list[str]) -> None:
        self._return_values = return_values
        self._index = 0

    def __call__(self, text: str) -> str:
        value = self._return_values[self._index]
        self._index += 1
        return value


class FkPrint(object):
    def __init__(self) -> None:
        self.container: list[str] = []

    def __call__(self, text: str) -> None:
        self.container.append(text)


def test_underscores(game_object: Hangman):
    """Test length of the word_to_print_str, supposed to be same as the given word."""
    word_length = len(game_object.get_word())
    assert game_object._word_to_print_str == '_' * word_length  # noqa: WPS437 testing purpose


def test_user_input(game_object: Hangman):
    fake_user_input = FkUserInput(['ff', 'a'])
    fake_print = FkPrint()
    user_input(game_object.get_word_to_print_str(), fake_user_input, fake_print)

    assert fake_print.container[-1] == 'try again'


def test_time_up(game_object: Hangman, freezer):
    time = datetime.now() + timedelta(seconds=400)
    freezer.move_to(time)
    print(datetime.now())
    assert game_object.check_time() == True


def test_url(requests_mock):
    requests_mock.get('https://random-word-api.herokuapp.com/word', text='["testing"]')
    assert 'testing' == choose_word()


def test_choosing_word():
    """Test choose_word method."""
    random_word = choose_word()  # noqa: WPS437 testing purpose
    assert random_word != ''


def test_predicted(game_object: Hangman):
    """Test the guesses logic, if letter was predicted right, guesses counter is not decreasing."""
    game_object.guessing(game_object.get_word()[0])
    assert game_object.guesses == 10


def test_gameover(game_object: Hangman):
    """Test if the game is ending right after losing it. Guesses dicrements and becomes 0, which leads to game over."""
    game_object.guesses = 1
    assert game_object.guessing('a') is False

import requests
from hangman_class import Hangman
from typing import Callable
from datetime import datetime


def choose_word() -> str:
    """Return randomly taken word (str) from prepared dictionary file 'words.txt'.

    :returns:
        Word to play with
    """
    response = requests.get('https://random-word-api.herokuapp.com/word')
    return response.json()[0]


def user_input(word, input_function: Callable[[str], str], print_function: Callable[[str], str]) -> str:
    """Read player input and check if it's right. Input have to contain 1 letter only.

    :returns:
        char that user inputs
    """
    char = input_function('{0} guess a character: '.format(word)).lower()  # noqa: WPS421
    while not (len(char) == 1 and char.isalpha()):
        print_function('try again')
        char = input_function('{0} guess a character: '.format(word)).lower()  # noqa: WPS421
    return char


def start_game() -> None:
    """Start hangman game."""
    game = Hangman()
    continuing = True
    while continuing:
        char = user_input(game.get_word_to_print_str(), input, print)
        continuing = game.guessing(char)


if __name__ == '__main__':
    start_game()

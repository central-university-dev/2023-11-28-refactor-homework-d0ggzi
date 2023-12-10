import requests
from start_game_func import start_game
from typing import Callable
from datetime import datetime


class Hangman(object):
    """
    A class for hangman game.

    ...

    Attributes
    ----------
    word : lists
        list of characters of chosen word
    word_to_print : list
        list of characters with unguessed (marks as "_") and guessed letters
    word_to_print_str: str
        string of joined elements of word_to_print list
    guesses : int
        user attempts left before losing

    Methods
    -------
    choose_word():
        Return randomly taken word from prepared dictionary file "words.txt"
    guessing():
        Allow player to input a character and check whether it right or wrong and check if user won or lost
    """

    def __init__(self, word: str = '') -> None:
        """Construct all the necessary attributes for the hangman object.

        :param word:
            the word with which the game will start
            if the word wasn't given it takes it from get_word() method
        """
        self._word = word if word else choose_word()
        self._word_to_print = ['_' for _ in self._word]
        self._word_to_print_str = ''.join(self._word_to_print)
        self.guesses = 10
        self.start_time = datetime.now()
        print('The game has started!')  # noqa: WPS421

    def get_word_to_print_str(self) -> str:
        """ Getter for word_to_print_str to use in user_input function
        
        :returns:
            self._word_to_print_str
        """
        return self._word_to_print_str

    def get_word(self) -> str:
        """ Getter for word
        
        :returns:
            self._word
        """
        return self._word

    def check_time(self):
        current_time = datetime.now()
        if (current_time - self.start_time).seconds >= 300:
            print('Time is up! Game over.')
            return True
        return False

    def guessing(self, char) -> bool:
        """Allow player to input a character and check whether it right or wrong and check if user won or lost.

        :param char:
            the character that player entered

        :returns:
            True if game continues
            False if game ends
        """
        if self.check_time(): return False
        predicted = False
        for index, element in enumerate(self._word):
            if element == char:
                self._word_to_print[index] = char
                predicted = True
        self._word_to_print_str = ''.join(self._word_to_print)
        if not predicted:
            self.guesses -= 1
            if self.guesses == 0:
                print('Wrong! Game over.')  # noqa: WPS421
                print('The answer was {0}'.format(self._word))  # noqa: WPS421
                return False
            print('Wrong \nYou have {0} more guesses'.format(self.guesses))  # noqa: WPS421
        elif '_' not in self._word_to_print:
            print('{0} You won'.format(self._word_to_print_str))  # noqa: WPS421
            return False
        return True


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


if __name__ == '__main__':
    start_game()



def start_game() -> None:
    """Start hangman game."""
    game = Hangman()
    continuing = True
    while continuing:
        char = user_input(game.get_word_to_print_str(), input, print)
        continuing = game.guessing(char)

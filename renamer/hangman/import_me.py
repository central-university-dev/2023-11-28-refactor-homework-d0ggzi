from hangman import Hangman, user_input

game = Hangman()
char = user_input('hi', input, print)
game.guessing(char)

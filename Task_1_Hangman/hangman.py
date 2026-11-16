
import random
from pathlib import Path


# ASCII Hangman stages (0 to 6 incorrect guesses)
HANGMAN_STAGES = [
    r"""
     +---+
     |   |
         |
         |
         |
    =========
    """,
    r"""
     +---+
     |   |
     O   |
         |
         |
    =========
    """,
    r"""
     +---+
     |   |
     O   |
     |   |
         |
    =========
    """,
    r"""
     +---+
     |   |
     O   |
    /|   |
         |
    =========
    """,
    r"""
     +---+
     |   |
     O   |
    /|\  |
         |
    =========
    """,
    r"""
     +---+
     |   |
     O   |
    /|\  |
    /    |
    =========
    """,
    r"""
     +---+
     |   |
     O   |
    /|\  |
    / \  |
    =========
    """
]


# Select a random word from words.txt
def select_word():

    file_path = Path(__file__).with_name("words.txt")

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            words = [
                line.strip().lower()
                for line in file
                if line.strip().isascii()
                and line.strip().isalpha()
            ]

        if not words:
            print("Error: No valid words found in words.txt!")
            return None

        return random.choice(words)

    except FileNotFoundError:
        print("Error: words.txt file not found!")
        return None


# Display current Hangman drawing
def display_hangman(wrong_guesses):

    print(HANGMAN_STAGES[wrong_guesses])


# Display hidden and correctly guessed letters
def display_word(word, correct_guesses):

    return " ".join(
        letter if letter in correct_guesses else "_"
        for letter in word
    )


# Main game function
def play_game():

    word = select_word()

    if word is None:
        return

    correct_guesses = set()
    guessed_letters = set()
    wrong_guesses = 0
    max_attempts = 6

    print("\n================================")
    print("     WELCOME TO HANGMAN!")
    print("================================")

    while wrong_guesses < max_attempts:

        display_hangman(wrong_guesses)

        print("Word:", display_word(word, correct_guesses))
        print(f"Incorrect guesses: {wrong_guesses}/{max_attempts}")
        print("Guessed letters:", sorted(guessed_letters))

        guess = input("\nEnter a letter: ").strip().lower()

        # Validate user input
        if len(guess) != 1 or not guess.isascii() or not guess.isalpha():
            print("Invalid input! Please enter a single English letter.")
            continue

        # Check duplicate guesses
        if guess in guessed_letters:
            print("You already guessed this letter! Try another.")
            continue

        guessed_letters.add(guess)

        # Check correct or incorrect guess
        if guess in word:

            correct_guesses.add(guess)
            print("Correct guess!")

            # Check winning condition
            if all(letter in correct_guesses for letter in word):

                print("\n================================")
                print("       CONGRATULATIONS!")
                print("          YOU WIN!")
                print("================================")
                print("The word was:", word)
                return

        else:

            wrong_guesses += 1
            print("Wrong guess! Try again.")

    # Losing condition
    display_hangman(wrong_guesses)

    print("\n================================")
    print("          GAME OVER!")
    print("================================")
    print("The correct word was:", word)
    print("Better luck next time!")


# Start the game
if __name__ == "__main__":
    play_game()

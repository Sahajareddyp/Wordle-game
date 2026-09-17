import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

with open(BASE_DIR / "words.txt", "r") as file:
    words = file.readlines()
    clean_words=[]
    for word in words:
       word=word.strip()
       clean_words.append(word)

with open(BASE_DIR / "allowed_guesses.txt", "r") as file:
    words = file.readlines()
    clean_guesses=[]
    for word in words:
       word=word.strip()
       clean_guesses.append(word)

def random_word(clean_words):
    secret_word=random.choice(clean_words)
    return secret_word



def compare(guess, secret_word):
    result=[]
    remaining=list(secret_word)
    green_positions = []
    for i in range(len(guess)):
        if guess[i]==secret_word[i]: # check for green letters
            remaining.remove(guess[i]) # remove the letter from remaining letters
            green_positions.append(i)  # store the position of the green letter
    for i in range(len(guess)):
        if i in green_positions:  # check if the position is already marked as green
            result.append("🟩")   # mark as green
        elif guess[i] in remaining:
             remaining.remove(guess[i])
             result.append("🟨")
        else:
            result.append("⬜")
    return " ".join(result)        

def word_length():
    guess= input("Enter a valid 5-letter word:") 

    while len(guess)!=5 or not guess.isalpha() or guess.lower() not in clean_guesses:
        print("This guess is not valid.")
        guess = input("Enter a valid 5-letter word:")
    return guess.lower()

def main():
    secret_word = random_word(clean_words)
    for attempt_num in range(5):
        guess=word_length()
        if guess==secret_word:
            print("you win")
            break
        else:
            print(compare(guess, secret_word))
            if attempt_num == 4:
                print("The Word Garden word was:", secret_word)
            else:
                print("try again")


if __name__ == "__main__":
    main()





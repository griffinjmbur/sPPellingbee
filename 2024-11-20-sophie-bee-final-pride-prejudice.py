#!/usr/bin/env python
# coding: utf-8
# %%
# draft Pride/Prejudice version

import numpy as np
import string
from random import shuffle
import pandas as pd 
import requests
import re

url = "https://www.gutenberg.org/files/1342/1342-0.txt"
response = requests.get(url)
text = response.text.splitlines()

letters = list(string.ascii_lowercase)
messy_words = [word for line in text for word in line.split()]
no_hyphens = [w for w in messy_words if re.search('\-', w) == None]
clean_words = [re.sub('\W', '', w) for w in no_hyphens]
all_valid_words = [word for word in clean_words if len(word) > 3 and word[0].islower()]
valid_words = set(all_valid_words)
pangrams = [word for word in valid_words if len(set(word)) == 7 and word[0].islower()]
pangram = np.random.choice(pangrams)

#print(pangram)
    
# shuffling the letters and displaying to user
l = list(set(pangram))
shuffle(l)
letters = ''.join(l)
center_letter = l[0]
print(f"Letters: {letters}; center letter is {center_letter}")

# Getting today's pangrams and points
correct_answers = [word for word in valid_words 
                   if set(word).issubset(set(pangram)) and set(center_letter).issubset(word)]
todays_pangrams = [word for word in correct_answers if len(set(word))==len(set(pangram))]

game_points = 0
for ca in correct_answers: 
    if len(ca) == 4: 
        game_points += 1 
    elif len(ca) > 4 and ca not in todays_pangrams:
        game_points += len(ca) 
    elif ca in todays_pangrams:
        game_points += len(ca) + 7        

# Verifying
def verify(user_word, letter_set, words_found): 
    user_word_lower = user_word.lower()
    user_letters = set(user_word)
    if not user_letters.issubset(letter_set): 
        return "Letter not in list!", 0, ""
    if len(user_word) < 4: 
        return "Too short!", 0, ""
    if center_letter not in user_word: 
        return "Missing center letter!", 0, ""
    if user_word_lower not in valid_words:
        return "Not in word list!", 0, ""
    if guess in words_found:
        return "Already found!", 0, ""
    else: 
        if guess in words_found:
            return "Already found!", 0, []
        if len(user_word) == 4: 
            points = 1 
            cheer = ""
            pl = ""
            word_found = user_word
        elif len(user_word) > 4 and user_word not in todays_pangrams:
            points = len(user_word) 
            cheer = ""
            pl = "s"
            word_found = user_word
        elif user_word in todays_pangrams:
            points = len(user_word) + 7
            pl = "s"
            cheer = "Pangram!"
            word_found = user_word
        return f"{cheer} {points} point{pl}!", points, word_found
        

# Produce hints
df = pd.DataFrame(correct_answers, columns=["word"])
df["length"] = df["word"].str.len()
df["initial"] = df["word"].str[0]
df["twoinitials"] = df["word"].str[:2]
hints1 = pd.crosstab(index=df["initial"], columns=df["length"],
                     margins=True, margins_name="sum")
hints2 = df["twoinitials"].value_counts(ascending=True)


print(f"WORDS: {len(correct_answers)}, POINTS: {game_points}, PANGRAMS: {len(todays_pangrams)}")
print(hints1)
print(hints2)
#print(correct_answers)

user_points = 0
words_found = []
while user_points <= game_points:
    guess = input("Enter a word (or 'quit' to exit): ").strip()
    if not guess:
        print("Please enter a valid word!")
        continue
    if not guess.isalpha():
        print("Invalid input! Please enter alphabetic characters only.")
        continue
    if guess.lower() == 'quit':
        break

    result, points, word_found = verify(guess, list(set(pangram)), words_found)
    print(result)
    user_points += points
    if word_found != "":
        words_found.append(word_found)
    print(f"Total points = {user_points}")
    print(f"Words found = {words_found}")
    if user_points == game_points:
        print("QUEEN BEE!")
        break


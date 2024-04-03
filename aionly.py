from json import load
from random import choice
from minimax import leads_to_word, is_valid_word, make_move, minimax, load_wordlist

def play_game(wordlist):
    A_turn = True

    with open("./comboutility.json", "r") as f:
        comboutility = load(f)
    current_string = choice(comboutility["winning"])

    print(f"AI A chose the initial string \"{current_string}\"")

    A_turn = not A_turn

    while True:
        if A_turn and not leads_to_word(current_string, wordlist):
            print("Challenge from AI A: no words can be created from this string. AI A wins!")
            return
        if not A_turn and not leads_to_word(current_string, wordlist):
            print("Challenge from AI B: no words can be created from this string. AI B wins!")
            return
        
        if is_valid_word(current_string, wordlist) and len(current_string) > 2:
            if A_turn:
                print("AI B created a word. AI A wins!")
            else:
                print("AI A created a word. AI B wins!")
            return
        
        _, move = minimax(current_string, float('-inf'), float('inf'), A_turn, wordlist)
        letter, position = move
        current_string = make_move(current_string, letter, position)
        if A_turn:
            print(f"AI A adds '{letter}' at the {position}: {current_string}")
        else:
            print(f"AI B adds '{letter}' at the {position}: {current_string}")

        A_turn = not A_turn

wordlist = load_wordlist()
while True:
    play_game(wordlist)
    print()
from json import load
from random import choice
from minimax import leads_to_word, is_valid_word, word_continuation, make_move, minimax, load_wordlist

def play_game(wordlist):
    player_first = input("Do you want to go first? (yes/no): ").strip().lower().startswith('y')
    current_string = ""
    if player_first:
        current_string = input("Enter the initial 2 letters (words allowed): ")
        if len(current_string) != 2 or not current_string.isalpha():
            print("Player gave invalid input. AI wins!")
            return
    else:
        with open("./comboutility.json", "r") as f:
            comboutility = load(f)
        current_string = choice(comboutility["winning"])
        print(f"AI chose the initial string \"{current_string}\"")

    player_turn = not player_first

    while True:
        if not player_turn and not leads_to_word(current_string, wordlist):
            print("Challenge from AI: no words can be created from this string. AI wins!")
            return
        
        if is_valid_word(current_string, wordlist) and len(current_string) > 2:
            if player_turn:
                print("AI created a word. Player wins!")
            else:
                print("Player created a word. AI wins!")
            return

        if player_turn:
            move = input("Your move (format: letter [start/end] OR challenge): ")
            if move.lower() == "challenge":
                if not leads_to_word(current_string, wordlist):
                    print("Challenge successful: no words can be created from this string. Player wins!")
                else:
                    print(f"Challenge failed: {word_continuation(current_string, wordlist)} can be created. AI wins!")
                return
            elif len(move.split()) != 2 or not move.split()[0].isalpha() or move.split()[0].isalpha() and len(move.split()[0]) != 1 or move.split()[1] not in ["start", "end"]:
                print("Player gave invalid input. AI wins!")
                return
            else:
                letter, position = move.split()
                current_string = make_move(current_string, letter, position)
        else:
            _, move = minimax(current_string, float('-inf'), float('inf'), True, wordlist)
            letter, position = move
            current_string = make_move(current_string, letter, position)
            print(f"AI adds '{letter}' at the {position}: {current_string}")
        
        player_turn = not player_turn

wordlist = load_wordlist()
while True:
    play_game(wordlist)
    if input("Play again? (yes/no): ").strip().lower().startswith('n'):
        break
    print()
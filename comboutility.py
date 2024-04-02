from json import dump
from minimax import minimax, load_wordlist

wordlist = load_wordlist()
winning_combinations = []
losing_combinations = []

for letter1 in 'abcdefghijklmnopqrstuvwxyz':
    for letter2 in 'abcdefghijklmnopqrstuvwxyz':
        util = minimax(letter1 + letter2, float('-inf'), float('inf'), True, wordlist)[0]
        if util == 1:
            print(letter1 + letter2 + " is a winning starting combination")
            winning_combinations.append(letter1 + letter2)
        else:
            print(letter1 + letter2 + " is a losing starting combination")
            losing_combinations.append(letter1 + letter2)

txt_content = """If both players play perfectly...
Winning:
""" + '\n'.join(winning_combinations) + """

Losing:
""" + '\n'.join(losing_combinations)

json_content = {
    "winning": winning_combinations,
    "losing": losing_combinations
}

with open("./comboutility.txt", "w") as txt_file:
    txt_file.write(txt_content)

with open("./comboutility.json", "w") as json_file:
    dump(json_content, json_file)
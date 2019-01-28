from flask import Flask, render_template, redirect, url_for, request
import random

app = Flask(__name__)
app.config['SERVER_NAME'] = "localhost:5000"
all_words = [line.rstrip('\n') for line in open("words.txt")]
hangman_word = ""
num_characters = ""
used_letters = set()
guesses_left = 0
game_status = ""

@app.route("/", methods=['GET', 'POST'])
def set_difficulty():
	global hangman_word
	global num_characters
	global game_status
	hangman_word = list(random.choice(all_words).upper())
	num_characters = ["_ " for i in hangman_word]
	used_letters.clear()
	game_status = "Currently Playing..."
	return render_template('set_difficulty.html')

@app.route("/gameplay", methods=['GET', 'POST'])
def gameplay():
	global guesses_left
	global game_status
	if "difficulty" in request.form:
		difficulty = request.form["difficulty"]
		if difficulty == "easy":
			guesses_left = 10
		elif difficulty == "medium":
			guesses_left = 8
		elif difficulty == "hard":
			guesses_left = 6
		return render_template('gameplay.html', num_characters=' '.join(num_characters), used_letters=[], guesses_left=guesses_left, game_status=game_status, answer=' '.join(hangman_word))
	elif "letter" in request.form:
		letter = request.form["letter"]
		found_letter = False
		used_letters.add(letter)
		for char_index in range(len(hangman_word)):
			if hangman_word[char_index] == letter:
				num_characters[char_index] = letter
				found_letter = True
		if found_letter == False:
			guesses_left -= 1
		if guesses_left <= 0 and "_ " in num_characters:
			game_status = "Lost Game :("
		elif guesses_left >= 0 and "_ " not in num_characters:
			game_status = "Won Game :)"
		return render_template('gameplay.html', num_characters=' '.join(num_characters), used_letters=list(used_letters), guesses_left=guesses_left, game_status=game_status, answer=' '.join(hangman_word))
	elif "dummy" in request.form:
		return render_template('gameplay.html', num_characters=' '.join(num_characters), used_letters=list(used_letters), guesses_left=guesses_left, game_status=game_status, answer=' '.join(hangman_word))
	else:
		return render_template('gameplay.html', num_characters=' '.join(num_characters), used_letters=list(used_letters), guesses_left=guesses_left, game_status=game_status, answer=' '.join(hangman_word))

if __name__ == '__main__':
	app.run(debug=True)
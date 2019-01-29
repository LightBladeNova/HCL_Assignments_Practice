import unittest
import os
import Hangman_Game
import tempfile
import string
import random
from flask import Flask, render_template, redirect, url_for, request

class Hangman_Game_Tests(unittest.TestCase):

	def setUp(self):
		"Setup for the test"
		Hangman_Game.app.config['TESTING'] = True
		self.app = Hangman_Game.app.test_client()

	def tearDown(self):
		"Tear down the test"
		pass

	def test_url_status_codes(self):
		get_response = self.app.get('/game')
		self.assertEqual(get_response.status_code, 404)
		get_response = self.app.get('/difficulty')
		self.assertEqual(get_response.status_code, 404)
		get_response = self.app.get('/set_difficulty')
		self.assertEqual(get_response.status_code, 404)
		get_response = self.app.get('/')
		self.assertEqual(get_response.status_code, 200)
		get_response = self.app.get('/gameplay', follow_redirects=True)
		self.assertEqual(get_response.status_code, 200)
		get_response = self.app.get('/gameplay', follow_redirects=False)
		self.assertEqual(get_response.status_code, 302)
		get_response.close()

	def test_main_page_difficulty_setting(self):
		get_response = self.app.get('/')
		assert (b'<input type="radio" name="difficulty" value="easy" checked>' in get_response.data)
		assert (b'<input type="radio" name="difficulty" value="medium">' in get_response.data)
		assert (b'<input type="radio" name="difficulty" value="hard">' in get_response.data)
		self.assertEqual(get_response.mimetype, "text/html")
		self.assertEqual(get_response.status_code, 200)
		get_response.close()

	def test_GET_gameplay_redirects_to_main_page(self):
		# Going directly to /gameplay should redirect back to difficulty page
		get_response = self.app.get('/gameplay', follow_redirects=True)
		assert (b'<input type="radio" name="difficulty" value="easy" checked>' in get_response.data)
		assert (b'<input type="radio" name="difficulty" value="medium">' in get_response.data)
		assert (b'<input type="radio" name="difficulty" value="hard">' in get_response.data)
		self.assertEqual(get_response.mimetype, "text/html")
		self.assertEqual(get_response.status_code, 200)

		# Reloading /gameplay while playing game should redirect back to difficulty page
		post_request = self.app.post('/gameplay', data=self.difficulty("easy"), follow_redirects=True)
		self.assertEqual(post_request.mimetype, "text/html")
		self.assertEqual(post_request.status_code, 200)
		assert (b'Guesses Left: 10' in post_request.data)
		assert (Hangman_Game.get_guesses_left() == 10)
		post_request = self.app.post('/gameplay', data=self.letter("A"), follow_redirects=True)
		get_response = self.app.get('/gameplay', follow_redirects=True)
		assert (b'<input type="radio" name="difficulty" value="easy" checked>' in get_response.data)
		assert (b'<input type="radio" name="difficulty" value="medium">' in get_response.data)
		assert (b'<input type="radio" name="difficulty" value="hard">' in get_response.data)
		self.assertEqual(get_response.mimetype, "text/html")
		self.assertEqual(get_response.status_code, 200)

		post_request.close()
		get_response.close()

	def difficulty(self, mode):
		return {"difficulty": mode}

	def letter(self, letter):
		return {"letter": letter}

	def test_difficulty_num_guesses_left(self):
		# Test that guesses left varies depending on difficulty setting
		post_request = self.app.post('/gameplay', data=self.difficulty("easy"), follow_redirects=True)
		self.assertEqual(post_request.mimetype, "text/html")
		self.assertEqual(post_request.status_code, 200)
		assert (b'Guesses Left: 10' in post_request.data)
		assert (Hangman_Game.get_guesses_left() == 10)
		post_request = self.app.post('/gameplay', data=self.difficulty("medium"), follow_redirects=True)
		self.assertEqual(post_request.mimetype, "text/html")
		self.assertEqual(post_request.status_code, 200)
		assert (b'Guesses Left: 8' in post_request.data)
		assert (Hangman_Game.get_guesses_left() == 8)
		post_request = self.app.post('/gameplay', data=self.difficulty("hard"), follow_redirects=True)
		self.assertEqual(post_request.mimetype, "text/html")
		self.assertEqual(post_request.status_code, 200)
		assert (b'Guesses Left: 6' in post_request.data)
		assert (Hangman_Game.get_guesses_left() == 6)
		post_request.close()

	def test_hangman_word_win_with_max_guesses_left(self):
		get_response = self.app.get('/', follow_redirects=True)
		post_request = self.app.post('/gameplay', data=self.difficulty("medium"), follow_redirects=True)
		self.assertEqual(post_request.mimetype, "text/html")
		self.assertEqual(post_request.status_code, 200)
		assert (b'Guesses Left: 8' in post_request.data)
		hangman_word = Hangman_Game.get_hangman_word()
		num_characters = Hangman_Game.get_num_characters()
		current_index = 0
		while "_ " in num_characters:
			assert (b'Currently Playing...' in post_request.data)
			post_request = self.app.post('/gameplay', data=self.letter(hangman_word[current_index]), follow_redirects=True)
			self.assertEqual(post_request.mimetype, "text/html")
			self.assertEqual(post_request.status_code, 200)
			assert(bytes(' '.join(num_characters), 'utf-8') in post_request.data)
			current_index += 1
		assert (b'Guesses Left: 8' in post_request.data)
		assert (b'Game Status: Won Game :)' in post_request.data)
		assert (Hangman_Game.get_game_status() == "Won Game :)")
		post_request.close()
		get_response.close()

	def test_hangman_word_lose_with_no_guesses_left(self):
		get_response = self.app.get('/', follow_redirects=True)
		post_request = self.app.post('/gameplay', data=self.difficulty("hard"), follow_redirects=True)
		self.assertEqual(post_request.mimetype, "text/html")
		self.assertEqual(post_request.status_code, 200)
		assert (b'Guesses Left: 6' in post_request.data)
		hangman_word = Hangman_Game.get_hangman_word()
		num_characters = Hangman_Game.get_num_characters()
		guesses_left = Hangman_Game.get_guesses_left()
		assert (guesses_left == 6)
		while guesses_left > 0:
			assert (b'Currently Playing...' in post_request.data)
			letter = random.choice([l for l in list(string.ascii_uppercase) if l not in hangman_word])
			post_request = self.app.post('/gameplay', data=self.letter(letter), follow_redirects=True)
			self.assertEqual(post_request.mimetype, "text/html")
			self.assertEqual(post_request.status_code, 200)
			assert(bytes(' '.join(num_characters), 'utf-8') in post_request.data)
			guesses_left = Hangman_Game.get_guesses_left()
		assert (b'Guesses Left: 0' in post_request.data)
		assert (guesses_left == 0)
		assert (b'Game Status: Lost Game :(' in post_request.data)
		assert (Hangman_Game.get_game_status() == "Lost Game :(")
		post_request.close()
		get_response.close()

	def test_hangman_word_MISSISSIPPI_check_multiple_of_same_letter(self):
		get_response = self.app.get('/', follow_redirects=True)
		hangman_word = Hangman_Game.set_hangman_word("MISSISSIPPI")
		num_characters = Hangman_Game.set_num_characters("MISSISSIPPI")
		post_request = self.app.post('/gameplay', data=self.difficulty("hard"), follow_redirects=True)
		self.assertEqual(post_request.mimetype, "text/html")
		self.assertEqual(post_request.status_code, 200)
		assert (b'Guesses Left: 6' in post_request.data)
		guesses_left = Hangman_Game.get_guesses_left()
		assert (guesses_left == 6)
		same_letter_multiples = {"I": 4, "P": 2, "S": 4}
		for same_letter_multiple in same_letter_multiples:
			post_request = self.app.post('/gameplay', data=self.letter(same_letter_multiple), follow_redirects=True)
			assert (num_characters.count(same_letter_multiple) == same_letter_multiples[same_letter_multiple])
			assert (same_letter_multiple in Hangman_Game.get_used_letters())
		assert (len(Hangman_Game.get_used_letters()) == 3)
		post_request = self.app.post('/gameplay', data=self.letter("A"), follow_redirects=True)
		post_request = self.app.post('/gameplay', data=self.letter("Z"), follow_redirects=True)
		assert (len(Hangman_Game.get_used_letters()) == 5)
		assert (b'Guesses Left: 4' in post_request.data)
		guesses_left = Hangman_Game.get_guesses_left()
		assert (guesses_left == 4)
		assert (num_characters == ["_ ", "I", "S", "S", "I", "S", "S", "I", "P", "P", "I"])
		post_request = self.app.post('/gameplay', data=self.letter("M"), follow_redirects=True)
		assert (b'Guesses Left: 4' in post_request.data)
		guesses_left = Hangman_Game.get_guesses_left()
		assert (guesses_left == 4)
		assert (b'Game Status: Won Game :)' in post_request.data)
		assert (Hangman_Game.get_game_status() == "Won Game :)")
		assert (b'Answer: M I S S I S S I P P I' in post_request.data)
		post_request.close()
		get_response.close()


	def test_hangman_word_MISSISSIPPI_win_with_some_guesses_left(self):
		get_response = self.app.get('/', follow_redirects=True)
		hangman_word = Hangman_Game.set_hangman_word("MISSISSIPPI")
		num_characters = Hangman_Game.set_num_characters("MISSISSIPPI")
		post_request = self.app.post('/gameplay', data=self.difficulty("easy"), follow_redirects=True)
		self.assertEqual(post_request.mimetype, "text/html")
		self.assertEqual(post_request.status_code, 200)
		assert (b'Guesses Left: 10' in post_request.data)
		guesses_left = Hangman_Game.get_guesses_left()
		assert (guesses_left == 10)
		incorrect_letters = ["A", "B", "C", "D"]
		correct_letters = [l for l in list(string.ascii_uppercase) if l in hangman_word]
		incorrect_and_correct_letters = incorrect_letters + correct_letters
		current_index = 0
		while "_ " in num_characters:
			assert (b'Currently Playing...' in post_request.data)
			post_request = self.app.post('/gameplay', data=self.letter(incorrect_and_correct_letters[current_index]), follow_redirects=True)
			self.assertEqual(post_request.mimetype, "text/html")
			self.assertEqual(post_request.status_code, 200)
			assert(bytes(' '.join(num_characters), 'utf-8') in post_request.data)
			guesses_left = Hangman_Game.get_guesses_left()
			current_index += 1
		assert (b'Guesses Left: 6' in post_request.data)
		assert (guesses_left == 6)
		assert (b'Game Status: Won Game :)' in post_request.data)
		assert (Hangman_Game.get_game_status() == "Won Game :)")
		assert (b'Answer: M I S S I S S I P P I' in post_request.data)
		post_request.close()
		get_response.close()

if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(Hangman_Game_Tests)
	unittest.TextTestRunner(verbosity=2).run(suite)
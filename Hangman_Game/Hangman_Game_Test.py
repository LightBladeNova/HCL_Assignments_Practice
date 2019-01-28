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

	def test_main_page_difficulty_setting(self):
		get_response = self.app.get('/')
		assert (b'<input type="radio" name="difficulty" value="easy" checked>' in get_response.data)
		assert (b'<input type="radio" name="difficulty" value="medium">' in get_response.data)
		assert (b'<input type="radio" name="difficulty" value="hard">' in get_response.data)
		self.assertEqual(get_response.mimetype, "text/html")
		self.assertEqual(get_response.status_code, 200)
		get_response.close()

	def difficulty(self, mode):
		return {"difficulty": mode}

	def letter(self, letter):
		return {"letter": letter}

	def test_difficulty_num_guesses_left(self):
		post_request = self.app.post('/gameplay', data=self.difficulty("easy"), follow_redirects=True)
		assert (b'Guesses Left: 10' in post_request.data)
		post_request = self.app.post('/gameplay', data=self.difficulty("medium"), follow_redirects=True)
		assert (b'Guesses Left: 8' in post_request.data)
		post_request = self.app.post('/gameplay', data=self.difficulty("hard"), follow_redirects=True)
		assert (b'Guesses Left: 6' in post_request.data)
		post_request.close()

	def test_hangman_word_win_with_max_guesses_left(self):
		get_response = self.app.get('/', follow_redirects=True)
		post_request = self.app.post('/gameplay', data=self.difficulty("easy"), follow_redirects=True)
		assert (b'Guesses Left: 10' in post_request.data)
		hangman_word = Hangman_Game.hangman_word
		num_characters = Hangman_Game.num_characters
		current_index = 0
		while "_ " in num_characters:
			assert (b'Currently Playing...' in post_request.data)
			post_request = self.app.post('/gameplay', data=self.letter(hangman_word[current_index]), follow_redirects=True)
			assert(bytes(' '.join(num_characters), 'utf-8') in post_request.data)
			current_index += 1
		assert (b'Guesses Left: 10' in post_request.data)
		assert (b'Won Game :)' in post_request.data)
		post_request.close()
		get_response.close()

	def test_hangman_word_lose_with_zero_guesses_left(self):
		get_response = self.app.get('/', follow_redirects=True)
		post_request = self.app.post('/gameplay', data=self.difficulty("medium"), follow_redirects=True)
		assert (b'Guesses Left: 8' in post_request.data)
		hangman_word = Hangman_Game.hangman_word
		num_characters = Hangman_Game.num_characters
		guesses_left = Hangman_Game.guesses_left
		assert (guesses_left == 8)
		current_index = 0
		while guesses_left > 0:
			assert (b'Currently Playing...' in post_request.data)
			letter = random.choice([l for l in list(string.ascii_uppercase) if l not in hangman_word])
			post_request = self.app.post('/gameplay', data=self.letter(letter), follow_redirects=True)
			assert(bytes(' '.join(num_characters), 'utf-8') in post_request.data)
			guesses_left = Hangman_Game.guesses_left
		assert (b'Guesses Left: 0' in post_request.data)
		assert (b'Lost Game :(' in post_request.data)
		post_request.close()
		get_response.close()

if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(Hangman_Game_Tests)
	unittest.TextTestRunner(verbosity=2).run(suite)
import unittest
import os
import upload_download_service
import tempfile
import string
import random
from flask import Flask, render_template, redirect, url_for, request
from werkzeug.utils import secure_filename

class Upload_Download_Service_Tests(unittest.TestCase):

	def setUp(self):
		"Setup for the test"
		upload_download_service.app.config['TESTING'] = True
		self.app = upload_download_service.app.test_client()
		for file in os.listdir(upload_download_service.app.config['UPLOAD_FOLDER']):
			os.remove(os.path.join(upload_download_service.app.config['UPLOAD_FOLDER'], file))

	def tearDown(self):
		"Tear down the test"
		for file in os.listdir(upload_download_service.app.config['UPLOAD_FOLDER']):
			os.remove(os.path.join(upload_download_service.app.config['UPLOAD_FOLDER'], file))

	def test_url_status_codes(self):
		get_response = self.app.get('/download')
		self.assertEqual(get_response.status_code, 404)
		get_response = self.app.get('/delete')
		self.assertEqual(get_response.status_code, 404)
		get_response = self.app.get('/')
		self.assertEqual(get_response.status_code, 200)
		get_response = self.app.get('/upload', follow_redirects=True)
		self.assertEqual(get_response.status_code, 200)
		get_response = self.app.get('/upload', follow_redirects=False)
		self.assertEqual(get_response.status_code, 302)
		get_response = self.app.get('/download_or_delete', follow_redirects=True)
		self.assertEqual(get_response.status_code, 200)
		get_response = self.app.get('/download_or_delete', follow_redirects=False)
		self.assertEqual(get_response.status_code, 302)
		get_response.close()

	def test_main_page_file_uploader_downloader(self):
		get_response = self.app.get('/')
		self.assertEqual(get_response.mimetype, "text/html")
		self.assertEqual(get_response.status_code, 200)
		assert (b'<title>File Uploader/Downloader</title>' in get_response.data)
		assert (b'<form action="/upload" method="POST" enctype="multipart/form-data">' in get_response.data)
		assert (b'<input type="file" name="file">' in get_response.data)
		get_response.close()

	def test_GET_upload_and_download_or_delete_redirects_to_main_page(self):
		get_response = self.app.get('/upload', follow_redirects=True)
		assert (b'<title>File Uploader/Downloader</title>' in get_response.data)
		assert (b'<form action="/upload" method="POST" enctype="multipart/form-data">' in get_response.data)
		assert (b'<input type="file" name="file">' in get_response.data)
		get_response = self.app.get('/download_or_delete', follow_redirects=True)
		assert (b'<title>File Uploader/Downloader</title>' in get_response.data)
		assert (b'<form action="/upload" method="POST" enctype="multipart/form-data">' in get_response.data)
		assert (b'<input type="file" name="file">' in get_response.data)
		get_response.close()

	def test_upload_one_simple(self):
		file = open("Vikavolt.png", "rb")
		post_request = self.app.post('/upload', data={"file": file}, follow_redirects=True, content_type='multipart/form-data')
		assert (b'File successfully uploaded!' in post_request.data)
		assert (bytes("File Name: " + file.name, 'utf-8') in post_request.data)
		assert (bytes("File Size (Bytes): " + str(os.path.getsize(
			os.path.join(upload_download_service.app.config['UPLOAD_FOLDER'], secure_filename(file.name)))), 'utf-8') in post_request.data)
		file.close()

	def test_upload_one_change_spaces_to_underscroll(self):
		file = open("ZTD Election Image.jpg", "rb")
		post_request = self.app.post('/upload', data={"file": file}, follow_redirects=True, content_type='multipart/form-data')
		assert (b'File successfully uploaded!' in post_request.data)
		assert (bytes("File Name: " + secure_filename(file.name), 'utf-8') in post_request.data)
		assert (bytes("File Name: ZTD_Election_Image.jpg", 'utf-8') in post_request.data)
		assert (bytes("File Size (Bytes): " + str(os.path.getsize(
			os.path.join(upload_download_service.app.config['UPLOAD_FOLDER'], secure_filename(file.name)))), 'utf-8') in post_request.data)
		file.close()

	def test_upload_multiple_of_same_file(self):
		multiples = ["Valeria_Trifa.png", "Valeria_Trifa_1.png", "Valeria_Trifa_2.png", "Valeria_Trifa_3.png", "Valeria_Trifa_4.png"]
		for i in range(0, 5):
			file = open("Valeria Trifa.png", "rb")
			filename, extension = os.path.splitext(file.name)
			copy_number_string = "1"
			name_multiple = "Valeria Trifa.png"
			while os.path.isfile(os.path.join(upload_download_service.app.config['UPLOAD_FOLDER'], secure_filename(name_multiple))) == True:
				name_multiple = filename + "_" + copy_number_string + extension
				copy_number_string = str(int(copy_number_string) + 1)
			post_request = self.app.post('/upload', data={"file": file}, follow_redirects=True, content_type='multipart/form-data')
			assert (b'File successfully uploaded!' in post_request.data)
			assert (bytes("File Name: " + secure_filename(name_multiple), 'utf-8') in post_request.data)
			assert (bytes(multiples[i], 'utf-8') in post_request.data)
			assert (bytes("File Size (Bytes): " + str(os.path.getsize(
				os.path.join(upload_download_service.app.config['UPLOAD_FOLDER'], secure_filename(name_multiple)))), 'utf-8') in post_request.data)
			file.close()

	def test_download_file(self):
		file = open("Vikavolt.png", "rb")
		post_request = self.app.post('/upload', data={"file": file}, follow_redirects=True, content_type='multipart/form-data')
		assert (b'File successfully uploaded!' in post_request.data)
		assert (bytes("File Name: " + secure_filename(file.name), 'utf-8') in post_request.data)
		assert (bytes("File Size (Bytes): " + str(os.path.getsize(
			os.path.join(upload_download_service.app.config['UPLOAD_FOLDER'], secure_filename(file.name)))), 'utf-8') in post_request.data)
		assert (len(os.listdir(upload_download_service.app.config['UPLOAD_FOLDER'])) == 1)
		file.close()
		file = open("Vikavolt.png", "r")
		post_request = self.app.post('/download_or_delete', data={"file": secure_filename(file.name), "download": "Download"}, follow_redirects=True)
		assert (len(os.listdir(upload_download_service.app.config['UPLOAD_FOLDER'])) == 1)
		file.close()

	def test_delete_file_with_no_space(self):
		assert (len(os.listdir(upload_download_service.app.config['UPLOAD_FOLDER'])) == 0)
		file = open("Vikavolt.png", "rb")
		post_request = self.app.post('/upload', data={"file": file}, follow_redirects=True, content_type='multipart/form-data')
		assert (b'File successfully uploaded!' in post_request.data)
		assert (bytes("File Name: " + secure_filename(file.name), 'utf-8') in post_request.data)
		assert (bytes("File Size (Bytes): " + str(os.path.getsize(
			os.path.join(upload_download_service.app.config['UPLOAD_FOLDER'], secure_filename(file.name)))), 'utf-8') in post_request.data)
		assert (len(os.listdir(upload_download_service.app.config['UPLOAD_FOLDER'])) == 1)
		file.close()
		file = open("Vikavolt.png", "r")
		post_request = self.app.post('/download_or_delete', data={"file": secure_filename(file.name), "delete": "Delete"}, follow_redirects=True)
		assert (len(os.listdir(upload_download_service.app.config['UPLOAD_FOLDER'])) == 0)
		file.close()

	def test_delete_file_with_space(self):
		assert (len(os.listdir(upload_download_service.app.config['UPLOAD_FOLDER'])) == 0)
		file = open("Valeria Trifa.png", "rb")
		post_request = self.app.post('/upload', data={"file": file}, follow_redirects=True, content_type='multipart/form-data')
		assert (b'File successfully uploaded!' in post_request.data)
		assert (bytes("File Name: " + secure_filename(file.name), 'utf-8') in post_request.data)
		assert (bytes("File Size (Bytes): " + str(os.path.getsize(
			os.path.join(upload_download_service.app.config['UPLOAD_FOLDER'], secure_filename(file.name)))), 'utf-8') in post_request.data)
		assert (len(os.listdir(upload_download_service.app.config['UPLOAD_FOLDER'])) == 1)
		file.close()
		file = open("Valeria Trifa.png", "r")
		post_request = self.app.post('/download_or_delete', data={"file": secure_filename(file.name), "delete": "Delete"}, follow_redirects=True)
		assert (len(os.listdir(upload_download_service.app.config['UPLOAD_FOLDER'])) == 0)
		file.close()


if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(Upload_Download_Service_Tests)
	unittest.TextTestRunner(verbosity=2).run(suite)
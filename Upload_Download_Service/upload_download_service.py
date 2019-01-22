import os
from flask import Flask, request, redirect, url_for, render_template, flash, send_file, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = "./uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=['GET', 'POST'])
def file_uploader_downloader():
	return render_template('file_uploader_downloader.html')

@app.route("/upload", methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		if 'file' in request.files:
			file = request.files['file']
			if file.filename == '':
				return redirect(url_for('file_uploader_downloader'))
			file.filename = secure_filename(file.filename)
			filename, extension = os.path.splitext(file.filename)
			copy_number_string = "1"
			while os.path.isfile("./uploads/" + file.filename) == True:
				file.filename = filename + "_" + copy_number_string + extension
				copy_number_string = str(int(copy_number_string) + 1)
			filename_secure = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_secure))
			file_upload_status = "File successfully uploaded!"
			file_size = os.path.getsize("./uploads/" + filename_secure)
			return render_template('file_uploader_downloader.html', file_upload_status = file_upload_status,
				filename="File Name: " + filename_secure, filesize="Fize Size (Bytes): " + str(file_size))
		else:
			return redirect(url_for('file_uploader_downloader'))
	elif request.method == 'GET':
		return redirect(url_for('file_uploader_downloader'))

@app.route("/download", methods=['GET', 'POST'])
def download_file():
	if request.method == 'POST':
		if "download_page" in request.form:
			all_files = [file for file in os.listdir(app.config['UPLOAD_FOLDER']) if file != '.DS_Store']
			all_files.sort()
			return render_template('download_page.html', all_files=all_files)
		elif "download_file" in request.form:
			file = request.form["download_file"]
			return send_from_directory(app.config['UPLOAD_FOLDER'], file, as_attachment=True)
		elif "dummy" in request.form:
			all_files = [file for file in os.listdir(app.config['UPLOAD_FOLDER']) if file != '.DS_Store']
			all_files.sort()
			return render_template('download_page.html', all_files=all_files)
		else:
			return redirect(url_for('file_uploader_downloader'))
	elif request.method == 'GET':
		return redirect(url_for('file_uploader_downloader'))

@app.route("/delete", methods=['GET', 'POST'])
def delete_file():
	if request.method == 'POST':
		if "delete_page" in request.form:
			all_files = [file for file in os.listdir(app.config['UPLOAD_FOLDER']) if file != '.DS_Store']
			all_files.sort()
			return render_template('delete_page.html', all_files=all_files)
		elif "delete_file" in request.form:
			file = request.form["delete_file"]
			os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file))
			all_files = [file for file in os.listdir(app.config['UPLOAD_FOLDER']) if file != '.DS_Store']
			all_files.sort()
			return render_template('delete_page.html', all_files=all_files)
		elif "dummy" in request.form:
			all_files = [file for file in os.listdir(app.config['UPLOAD_FOLDER']) if file != '.DS_Store']
			all_files.sort()
			return render_template('delete_page.html', all_files=all_files)
		else:
			return redirect(url_for('file_uploader_downloader'))
	elif request.method == 'GET':
		return redirect(url_for('file_uploader_downloader'))
 
if __name__ == '__main__':
	app.run(debug=True)
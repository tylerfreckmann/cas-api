from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from werkzeug.utils import secure_filename
import swat
import requests

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
# ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
	if request.method == 'POST':
		# check if the post request has the file part
		if 'file' not in request.files:
			print('No file part')
			return redirect(url_for('index'))
		file = request.files['file']
		if file.filename == '':
			print('No selected file')
			return redirect(url_for('index'))
		if file:
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

			# CAS Image Processing
			s = swat.CAS('localhost', 5570, 'tyfrec', 'tyfrec1')
			s.loadactionset('image')
			path = request.url_root + url_for('uploaded_file', filename=filename)[1:]
			s.loadimages(path=path, casout={'name':'img'})
			s.loadactionset('astore')
			s.score(table={'name':'img'}, out={'name':'score'}, rstore={'name':'lenet'})
			score = s.fetch(table={'name':'score'})
			s.endSession()
			return score
	return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/demo')
def demo():
	return render_template('demo.html')

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
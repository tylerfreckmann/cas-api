from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
import os
from werkzeug.utils import secure_filename
import swat
import requests
from collections import OrderedDict

APP_IP = '0.0.0.0'
APP_PORT = 7050
AUTHINFO = './.authinfo'
UPLOAD_FOLDER = '/imgcaslib'
ASTORE_LIB = 'casuser'
ASTORE = 'lenet'
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
			filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			file.save(filepath)

			# CAS Image Processing
			s = swat.CAS('localhost', 5570, authinfo=AUTHINFO)
			s.loadactionset('image')
			s.loadimages(filepath, casout={'name':'img'})
			s.loadactionset('astore')
			s.score(table={'name':'img'}, out={'name':'score'}, rstore={'name':ASTORE, 'caslib':ASTORE_LIB})
			scores = s.fetch(table={'name':'score'})['Fetch'].loc[0,:].to_dict()
			label = scores.pop('I__label_')
			s.endSession()
			return jsonify({'imgUrl': url_for('uploaded_file', filename=filename),
				'label': label,
				'scores': scores})

	return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
	app.run(debug=True, host=APP_IP, port=APP_PORT)
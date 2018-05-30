from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from werkzeug.utils import secure_filename
import swat

UPLOAD_FOLDER = './uploads'
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
			return render_template('demo.html')
			# return url_for('uploaded_file', filename=filename)
	return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
	s = swat.CAS('tyler-cas.gtp-americas.sashq-d.openstack.sas.com', 5570, 'tyfrec', 'tyfrec1')
	s.loadactionset('image')
	app.run(debug=True, host='0.0.0.0')
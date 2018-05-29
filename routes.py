from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from werkzeug.utils import secure_filename
import swat

UPLOAD_FOLDER = '.'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
	if request.method == 'POST':
		if 'files[]' not in request.files:
			print('did not receive files')
			return redirect(url_for('index'))
		files = request.files.getlist("files[]")
		for file in files:
			if file.filename == '':
				print('no filename')
				return redirect(url_for('index'))
			if file and allowed_file(file.filename):
				filename = secure_filename(file.filename)
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				print('saving file')
				return url_for('uploaded_file', filename=filename)
	print('redirecting to index')
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
from flask import Flask, url_for, send_from_directory, request, jsonify
import logging, os
from werkzeug.utils import secure_filename
import cv2

app = Flask(__name__)
file_handler = logging.FileHandler('server.log')
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
UPLOAD_FOLDER = '{}/uploads/'.format(PROJECT_HOME)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def create_new_folder(local_dir):
	newpath = local_dir
	if not os.path.exists(newpath):
		os.makedirs(newpath)
	return newpath

def allowedFile(filename):
	namefile = filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
	return namefile

def processLpn(img_name):
	pathImage = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
	image = cv2.imread(pathImage)
	cv2.imshow('img', image)
	cv2.waitKey(3000)

@app.route('/api/v1/image-upload', methods = ['POST'])
def uploadImage():
	app.logger.info(PROJECT_HOME)
	if request.method == 'POST':
		try:
			request.files['image']
			app.logger.info(app.config['UPLOAD_FOLDER'])
			img = request.files['image']
			if allowedFile(img.filename):
				img_name = secure_filename(img.filename)
				create_new_folder(app.config['UPLOAD_FOLDER'])
				saved_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
				app.logger.info("saving {}".format(saved_path))
				img.save(saved_path)
				result = processLpn(img_name)
				return jsonify({'message': 'success', 'immage_name': img_name})
			else:
				return jsonify({'message': 'Please Uplod Image file only'})
		except KeyError:
			return jsonify({'message': 'Sample file Image missing in POST request'})
	else:
		return jsonify({'message': 'Sample file Image missing in POST request'})

if __name__ == '__main__':
	app.run(debug=True)
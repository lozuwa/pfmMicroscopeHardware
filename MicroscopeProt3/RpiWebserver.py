''' 
up: 82
down: 84
right: 83 
left: 81
1: 49
2: 50
3: 51
4: 52
5: 53
'''

import os, sys 
import click 
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, Response, jsonify
from werkzeug import secure_filename
import numpy as np 
# Set cors 
from flask_cors import CORS, cross_origin
# Threads 
import eventlet
eventlet.monkey_patch()

# HTML code to post a file to the server 
html_post_file = ''' 
<!DOCTYPE html>
<html lang="en">
  <head>
    <link href="//netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap.min.css"
          rel="stylesheet">
  </head>
  <body>
    <div class="container">
      <div class="header">
        <h3 class="text-muted">How To Upload a File</h3>
      </div>
      <hr/>
      <div>
      
      <form action="post_image" method="post" enctype="multipart/form-data">
        <input type="file" name="file"><br /><br />
        <input type="submit" value="Upload">
      </form>
      </div>
    </div>
  </body>
</html>
'''

html_post_message = ''' 
<!DOCTYPE html>
<html lang="en">
  <head>
    <link href="//netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap.min.css"
          rel="stylesheet">
  </head>
  <body>
    <div class="container">
      <div class="header">
        <h3 class="text-muted">Send a message</h3>
      </div>
      <hr/>
      <div>

      <form action="post_message" method="post">
        <input type="text" name="body"><br /><br />
        <input type="submit" value="Send">
      </form>
      </div>
    </div>
  </body>
</html>
'''

# Initialize the Flask application
app = Flask(__name__)
CORS(app)

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'C:/Users/HP/Dropbox/CLICK_Medical/CLICK/Hardware/images/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# Main page for the webpage 
@app.route('/', methods=['GET'])
def index():
	return '''<b> Welcome to the home page </b>'''

# Route that will post a message
@app.route('/post_message', methods=['POST', 'GET'])
def post_message():
	if request.method == 'GET':
		return html_post_message
	elif request.method == 'POST':
		requested = request.form['body']
		print( str(requested) )
		return jsonify({'result': 'success'})
	else:
		return ''' <b> Welcome to the message page </b> '''

# Route that will process the file upload
@app.route('/post_image', methods=['POST', 'GET'])
def post_image():
	if request.method == 'GET':
		#return render_template('index.html')
		return html_post_file
	elif request.method == 'POST':
		# Get the name of the uploaded file
		file = request.files['file']
		print(file)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			#return redirect(url_for('uploaded_file', filename=filename))
			return jsonify({'result': 'success'})
	else:
		return '''<b> GET method not supported </b>'''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

@app.route('/get_cam_state', methods=['GET'])
def get_cam_state():
	if request.method == 'GET':
		return jsonify({'result': str(state)})

def listen():
	global state
	while True:
    state = 10 

    # Move events 
    key = click.getchar()

    # Arrow event 
    if key == b'\xe0':
      # Wait for second stream  
      key = bytes.decode( click.getchar() )
      if key == 'H': # Up arrow 
        pass 
      elif key == 'K': # Left arrow 
        pass 
      elif key == 'M': # Right arrow 
        pass
      elif key == 'P': # Down arrow 
        pass
      else:
        pass 
    # Other events 
    else:
      key = bytes.decode( key )
      if key == '1': # E.coli 
        pass
      elif key == '2': # Giardia 
        pass 
      else:
        pass
		eventlet.sleep(0.01)

eventlet.spawn(listen)

if __name__ == '__main__':
	app.run(host="192.168.3.214",
			port=int("5000"),
			debug=True)

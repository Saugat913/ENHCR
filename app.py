import io
import time
from flask import Flask, render_template, request, redirect, url_for, flash,Response
from PIL import Image  # For image processing (optional)


ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/help')
def help():
    return render_template('help.html')


@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')


@app.route('/upload', methods=['POST'])
def upload_image():
    
    
    if 'file-input' not in request.files:
        flash('No selected file. Please choose an image to upload.')
        return redirect(url_for('home'))

    uploaded_file = request.files['file-input']
    
    print("I am here")
    
    if uploaded_file and allowed_file(uploaded_file.filename):
       
        filename= uploaded_file.filename
        
        try:
            # Read and validate the image (modify as needed)
            # with io.BytesIO(uploaded_file.read()) as image_buffer:
            #     image = Image.open(image_buffer)
            
            time.sleep(30) 

            return Response(io.BytesIO(uploaded_file.read()).getvalue(), mimetype='image/jpg')

        except (IOError, OSError, ValueError) as e:
            
            flash(f'Error uploading image: {e}')
            return redirect(url_for('home'))

    else:
        flash('Invalid file format. Please upload a  JPEG, or JPG image.')
        return redirect(url_for('home'))
      
    

if __name__ == '__main__':
    app.run(debug=True)

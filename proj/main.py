from flask import Flask, redirect,url_for, render_template, request,jsonify
import random
from tensorflow import keras
import cv2
import numpy as np
import base64

from tensorflow.keras.models import load_model
app = Flask(__name__)

model = keras.models.load_model('./digit_trained.h5')

@app.route("/home")
@app.route("/",methods=['GET'])
def home():
	random_no=random.randint(0, 9)
	return render_template("home.html",random_no=random_no)

@app.route('/', methods=['POST'])
def canvas():
    # Recieve base64 data from the user form
    canvasdata = request.form['canvasimg']
    encoded_data = request.form['canvasimg'].split(',')[1]

    # Decode base64 image to python array
    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    img = np.zeros((512,512,1))

    # Convert 3 channel image (RGB) to 1 channel image (GRAY)
    # gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv2.circle(img, (x,y), 20, (255,255,255), -1)

    # Resize to (28, 28)
    # gray_image = cv2.resize(gray_image, (28, 28), interpolation=cv2.INTER_LINEAR)
    gray_image = cv2.resize(img, (28, 28))

    # Expand to numpy array dimenstion to (1, 28, 28)
    # img = np.expand_dims(gray_image, axis=0)
    # gray = gray.reshape(1, 784)

    gray_image = gray_image.reshape(1, 784)

    try:
        prediction = np.argmax(model.predict(gray_image))
        print(f"Prediction Result : {str(prediction)}")
        return render_template('home.html', response=str(prediction), canvasdata=canvasdata, success=True)
    except Exception as e:
    	print(e)
    	return render_template('home.html', response=str(e), canvasdata=canvasdata)

if __name__ == "__main__":
    app.run(debug=True)
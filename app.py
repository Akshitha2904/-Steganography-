from flask import Flask, render_template, request, send_file, jsonify
from werkzeug.utils import secure_filename
import cv2
import numpy as np
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


# Function to encode message in an image
def encode_message(img, message):
    message += "###"  # End delimiter
    binary_msg = ''.join(format(ord(char), '08b') for char in message)
    data_idx = 0
    img = img.astype(np.uint8)  # Ensure the image uses uint8 format

    for row in img:
        for pixel in row:
            for channel in range(3):
                if data_idx < len(binary_msg):
                    new_value = (pixel[channel] & ~1) | int(binary_msg[data_idx])
                    pixel[channel] = np.clip(new_value, 0, 255)  # Ensure values stay in range
                    data_idx += 1
                else:
                    break
    return img




# Function to decode message from an image
def decode_message(img):
    binary_msg = ""
    for row in img:
        for pixel in row:
            for channel in range(3):
                binary_msg += str(pixel[channel] & 1)
    chars = [binary_msg[i:i + 8] for i in range(0, len(binary_msg), 8)]
    message = ''.join(chr(int(char, 2)) for char in chars)
    return message.split("###")[0] if "###" in message else ""


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/encode', methods=['POST'])
def encode():
    image = request.files['image']
    message = request.form['message']
    filename = secure_filename(image.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(filepath)

    img = cv2.imread(filepath)
    encoded_img = encode_message(img, message)
    encoded_path = os.path.join(app.config['UPLOAD_FOLDER'], 'encoded_' + filename)
    cv2.imwrite(encoded_path, encoded_img)

    return send_file(encoded_path, as_attachment=True)


@app.route('/decode', methods=['POST'])
def decode():
    image = request.files['image']
    filename = secure_filename(image.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(filepath)

    img = cv2.imread(filepath)
    message = decode_message(img)

    return jsonify({'message': message})


if __name__ == '__main__':
    app.run(debug=True)

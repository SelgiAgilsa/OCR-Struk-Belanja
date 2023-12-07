from flask import Flask, render_template, request
import cv2
import pytesseract
import numpy as np
import os

app = Flask(__name__, static_folder='static')

# Konfigurasi Tesseract
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
config = 'digits'

@app.route('/', methods=['GET', 'POST'])
def ocr_page():
    detected_characters = ""
    output_image = None
    if request.method == 'POST':
        uploaded_image = request.files['image']
        if uploaded_image.filename != '':
            # Menyimpan gambar yang diunggah sebagai file temporary
            temp_image_path = os.path.join("static", "input_image.jpg")
            uploaded_image.save(os.path.join(app.root_path, temp_image_path))

            # Membaca gambar yang diunggah
            image = cv2.imread(os.path.join(app.root_path, temp_image_path))
            img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Melakukan OCR
            results = pytesseract.image_to_boxes(img_rgb)
            ih, iw, ic = image.shape

            for box in results.splitlines():
                box = box.split(' ')

                if len(box) == 6:
                    character = box[0]
                    x, y, w, h = int(box[1]), int(box[2]), int(box[3]), int(box[4])

                    cv2.rectangle(image, (x, ih - y), (w, ih - h), (0, 255, 0), 2)
                    cv2.putText(image, character, (x, ih - h), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0), 1)

                    detected_characters += character + " "

            # Menyimpan gambar yang telah diberi marka dengan nama 'output_image.png'
            output_image_path = os.path.join("static", "output_image.jpg")
            cv2.imwrite(os.path.join(app.root_path, output_image_path), cv2.cvtColor(image, cv2.COLOR_RGB2BGR))

    return render_template('index.html', detected_characters=detected_characters, output_image=output_image)

if __name__ == '__main__':
    app.run(debug=True)

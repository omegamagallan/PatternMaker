from flask import Flask, url_for, request, render_template
from patternCreate import create_pattern
from io import BytesIO
from PIL import Image
import base64
import json


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'


@app.route('/')
@app.route('/home')
def return_():
    return render_template('home.html')


@app.route('/patternMaker', methods=['POST', 'GET'])
def return_pattern_maker():
    if request.method == 'GET':
        image = False
        return render_template('patternMaker.html', start_image=True, image=image)
    elif request.method == 'POST':
        # with open("data/pattern_types.json", "r") as read_file:
        #     patterns = json.load(read_file)
        image = request.files['image']
        scale = request.form['scale']
        width = request.form['width']
        pattern_name = request.form['pattern_name']
        image = Image.open(image)
        img = create_pattern(image, width, scale, pattern_name)
        if img == 'fail':
            return render_template('patternMaker.html', start_image=True, image=False)
        img_io = BytesIO()
        img.save(img_io, 'PNG', quality=100)
        img_io.seek(0)
        image = base64.b64encode(img_io.getvalue())
        return render_template('patternMaker.html', start_image=False, image=image.decode('ascii'))


@app.route('/faq')
def return_faq():
    return render_template('faq.html')


@app.route('/about')
def return_about():
    return render_template('about.html')


@app.route('/api/create_pattern', methods=['POST'])
def return_api():
    image = request.form['image']
    width = request.form['width']
    scale = request.form['scale']
    pattern_name = request.form['pattern_name']
    image = Image.open(BytesIO(base64.b64decode(image)))
    img = create_pattern(image, int(width), int(scale), pattern_name)
    img_io = BytesIO()
    img.save(img_io, 'PNG', quality=100)
    img_io.seek(0)
    image = base64.b64encode(img_io.getvalue())
    return image.decode('ascii')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')

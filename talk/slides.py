#!/usr/bin/env python3

import os
import sys

from flask import Flask
from flask import request
from flask import render_template
from flask import make_response

app = Flask(__name__)

# Note, you can't just change this to whatever you want, if you want
# static site to just magically work
SLIDES_LOCATION = "slides.md"


@app.route('/')
def index():
    return render_template('index.html', publishing_root='static/slides.html')


@app.route('/slides.md', methods=['GET'])
def get_slides():
    with open(SLIDES_LOCATION, encoding='utf-8') as fp:
        return fp.read()


@app.route('/slides.md', methods=['PUT'])
def save_slides():
    new_slides = request.get_data().decode('utf-8')
    with open(SLIDES_LOCATION, 'w', encoding='utf-8') as fp:
        fp.write(new_slides)
    return make_response("", 200)

if __name__ == '__main__':
    if not os.path.isfile(SLIDES_LOCATION):
        sys.exit('Please create %s' % SLIDES_LOCATION)
    app.run('127.0.0.1', 8005, debug=True)

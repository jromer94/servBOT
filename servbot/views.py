
from servbot import app
from flask import render_template
import helpers


@app.route('/', methods=['GET', 'POST'])
def index():
	return render_template('landing.html');

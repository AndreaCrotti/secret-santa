from flask import Flask, render_template
from flask_htmx import HTMX

app = Flask(__name__)
htmx = HTMX(app)

@app.route('/')
def hello_fly():
    return render_template('index.html')

@app.route('/partecipants', methods=['GET', 'POST'])
def partecipants():
    pass

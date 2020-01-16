"""Web app and library for regression analysis of provided data files."""

__all__ = ['processing']
__version__ = '0.2.0'
__author__ = 'Paweł Kowalski'

from datetime import datetime
import os

from flask import Flask, redirect, render_template, request, session
from pandas.api.types import is_string_dtype, is_numeric_dtype
from werkzeug.utils import secure_filename

from . import processing

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'SECRET_KEY'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


def allowed_file(filename, extensions=['csv', 'xls', 'xlsx']):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions


@app.route('/', methods=['GET', 'POST'])
def index():
    files = processing.find_files()
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            os.makedirs(app.instance_path, exist_ok=True)
            filename = secure_filename(file.filename).replace(' ', '_')
            now = datetime.now().isoformat(sep='_', timespec='seconds')
            file.save(os.path.join(app.instance_path, now + '_' + filename))
            return redirect(request.url)
    return render_template('index.html', version=__version__, files=files)


@app.route('/process', methods=['GET', 'POST'])
def process():
    if request.method == 'POST':
        session['file'] = request.form['file']
        session.modified = True
        features = processing.get_xy(session['file'])[0]
        categorical = {}
        numerical = []
        for f in features:
            if is_string_dtype(features[f]):
                categorical[f] = features[f].unique()
            elif is_numeric_dtype(features[f]):
                numerical.append(f)
    return render_template('process.html', file=session['file'],
                           categorical=categorical, numerical=numerical)


@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        session['form'] = dict(request.form.items())
        session.modified = True
        file = session['form'].pop('file', None)
        outcome = processing.get_xy(file)[1].name
        if any([not value for value in session['form'].values()]):
            result = ValueError('Failed to collect data.')
        else:
            X, y, sample = processing.process_data(file, session['form'])
            prediction, score = processing.predict_ols(X, y, sample)
            result = f'{prediction:.5g} (R^2 = {score:.2f})'
            if not all(sample.squeeze(axis=0).between(X.min(), X.max())):
                result += ' (out-of-sample)'
    return render_template('result.html', file=file, form=session['form'],
                           outcome=outcome, result=result)

"""Web app for regression analysis of provided data files."""

__all__ = ['processing']
__author__ = 'Paweł Kowalski'

import os

from flask import Flask, redirect, render_template, request, session
from pandas.api.types import is_string_dtype, is_numeric_dtype
from werkzeug.utils import secure_filename

from . import processing
from ._version import get_versions

__version__ = get_versions()['version']
del get_versions

app = Flask(__name__)
app.config.from_pyfile('config.cfg')


def allowed_file(filename):
    extensions = ['csv', 'xls', 'xlsx']
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions


@app.route('/', methods=['GET', 'POST'])
def index():
    files = processing.find_files()
    if 'URL' in app.config: files.update(app.config['URL'])
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename).replace(' ', '_')
            file.save(os.path.join(os.path.dirname(__file__), filename))
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
                           categorical=categorical, numerical=numerical,
                           version=__version__)


@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        session['form'] = dict(request.form.items())
        session.modified = True
        file = session['form'].pop('file', None)
        outcome = processing.get_xy(file)[1].name
        if any([not value for value in session['form'].values()]):
            results = {'Error': ValueError('Failed to collect data')}
        else:
            X, y, sample = processing.process_data(file, session['form'])
            ols, score = processing.predict_ols(X, y, sample)
            gbr = processing.predict_gbr(X, y, sample)
            ols_url = '"https://en.wikipedia.org/wiki/Ordinary_least_squares"'
            gbr_url = '"https://en.wikipedia.org/wiki/Gradient_boosting"'
            results = {
                f'<a href={ols_url}>OLS</a>': f'{ols:.5g} (R² = {score:.2f})',
                f'<a href={gbr_url}>GBR</a>': f'{gbr["mid"]:.5g} ' +
                f'({gbr["lower"]:.5g} ÷ {gbr["upper"]:.5g})',
            }
            if not all(sample.squeeze(axis=0).between(X.min(), X.max())):
                results['Warning'] = 'Out-of-sample prediction'
    return render_template('result.html', form=session['form'],
                           outcome=outcome, results=results,
                           version=__version__)

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
        global categorical
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
        features, outcome = processing.get_xy(file)
        category = ('').join(
            [v for k, v in session['form'].items() if k in categorical])
        cf = features[categorical].sum(axis=1)
        n = cf.value_counts().get(category, 1) if category else len(features)
        if any([not value for value in session['form'].values()]):
            results = {'<font color="red">Error': 'Failed to collect data'}
        else:
            X, y, sample = processing.process_data(file, session['form'])
            ols = processing.predict_ols(X, y, sample, n - 1)
            ols_url = '"https://en.wikipedia.org/wiki/Ordinary_least_squares"'
            se_url = '"https://en.wikipedia.org/wiki/Standard_error"'
            ci_url = '"https://en.wikipedia.org/wiki/Confidence_interval"'
            results = {
                f'<strong><a href={ols_url}>OLS</a> Prediction':
                    f'{ols["mean"]:.5g}',
                f'</strong><a href={se_url}>Standard Error</a>':
                    f'±{ols["mean_se"]:.5g}',
                f'95% <a href={ci_url}>Confidence Interval</a>':
                    f'{ols["mean_ci_lower"]:.5g} ÷ {ols["mean_ci_upper"]:.5g}'
            }
            if category: X = X.loc[(cf[cf == category]).index]
            if not all(sample.squeeze(axis=0).between(X.min(), X.max())):
                results['<font color="orange">Warning'] = 'Out-of-sample'
    return render_template('result.html', form=session['form'],
                           outcome=outcome.name, results=results,
                           version=__version__)

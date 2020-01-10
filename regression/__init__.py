"""Web application for regression analysis of provided data"""

__version__ = '0.1.1'
__author__ = 'Paweł Kowalski'

from flask import Flask, render_template, request, session
from pandas.api.types import is_string_dtype, is_numeric_dtype

from . import processing

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'SECRET_KEY'


@app.route('/')
def index():
    files = processing.find_csv_files()
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
            prediction, score, predstd = processing.predict_ols(X, y, sample)
            result = f'{prediction:.5g} ± {predstd:.5g} (R^2 = {score:.2f})'
            if not all(sample.squeeze(axis=0).between(X.min(), X.max())):
                result += ' (out-of-sample)'
    return render_template('result.html', file=file, form=session['form'],
                           outcome=outcome, result=result)

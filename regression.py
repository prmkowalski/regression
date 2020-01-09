"""
Simple Flask application for regression analysis of provided data.

Copy delimited text files CSV into the app root directory or subdirectory.
Files should be formatted with European syntax - a semicolon as the value
separator and a comma as the decimal separator. First row is headers.
Value rows should follow order - index;features;outcome (item;X;y).
Features can be given as numerical or categorical values.
You can get formatted CSV files by exporting from a spreadsheet.
Run on Flask's built-in server for simple calculations or deploy to
a WSGI server.

"""

__all__ = ['find_csv_files', 'process_data', 'predict_ols']
__version__ = '0.1.1'
__author__ = 'Paweł Kowalski'

from glob import glob
import os
from threading import Timer
import webbrowser

from flask import Flask, render_template, request, session
import pandas as pd
from pandas.api.types import is_string_dtype, is_numeric_dtype
import statsmodels.api as sm
from statsmodels.sandbox.regression.predstd import wls_prediction_std

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'SECRET_KEY'


def find_csv_files():
    """Return a list of all CSV files in the application directories."""
    try:
        here = os.path.dirname(__file__)
    except NameError:
        here = os.path.abspath('')
    csv_files = [filename
                 for dirpath, _, filenames in os.walk(here)
                 for filename in glob(os.path.join(dirpath, '*.csv'))]
    return csv_files


def _is_float(value):
    """Return True if value is a floating point number, False otherwise."""
    try:
        float(value)
        return True
    except ValueError:
        return False


def _get_xy(csv_filepath):
    """Return features and outcomes from CSV file."""
    filepath = os.path.join(os.path.dirname(__file__), csv_filepath)
    df = pd.read_csv(filepath, sep=';', header=0, index_col=0, decimal=',')
    df.columns = [label.replace(' ', '_') for label in df.columns]
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]
    return X, y


def process_data(csv_filepath, sample):
    """
    Ingest and format data from the input for regression analysis.

    Parameters
    ----------
    csv_filepath : str
        Path to a CSV file.
    sample : dict of {str: str}
        The {feature: value} pairs for which we want to predict.

    Returns
    -------
    X : DataFrame
        Formatted features with categorical variables converted into dummy.
    y : Series
        Outcomes - target values.
    sample : DataFrame
        Data to predict with columns matched to the formatted features (X).

    """
    X, y = _get_xy(csv_filepath)
    sample = {feature: float(value.replace(',', '.', 1))
              if _is_float(value.replace(',', '.', 1)) else value
              for feature, value in sample.items()}
    X = X.append(pd.Series(sample, name='sample'))
    X = pd.get_dummies(X)
    sample = X.loc['sample'].to_frame().T
    X = X.drop('sample')
    return X, y, sample


def predict_ols(X, y, sample):
    """
    Run a simple ordinary least squares model for data from the input.

    Parameters
    ----------
    X, y, sample
        Data prepared by process_data function.

    Returns
    -------
    prediction : float
        Linear predicted value from a model.
    score : float
        Coefficient of determination R-squared of a prediction model.
    predstd : float
        Standard error of prediction with confidence level alpha = 0.05.

    """
    model = sm.OLS(y, X).fit()
    prediction = float(model.predict(sample))
    score = model.rsquared
    predstd = wls_prediction_std(model)[0].mean()
    return prediction, score, predstd


@app.route('/')
def index():
    files = find_csv_files()
    return render_template('index.html', version=__version__, files=files)


@app.route('/process', methods=['GET', 'POST'])
def process():
    if request.method == 'POST':
        session['file'] = request.form['file']
        session.modified = True
        features = _get_xy(session['file'])[0]
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
        outcome = _get_xy(file)[1].name
        if any([not value for value in session['form'].values()]):
            result = ValueError('Failed to collect data.')
        else:
            X, y, sample = process_data(file, session['form'])
            prediction, score, predstd = predict_ols(X, y, sample)
            result = f'{prediction:.5g} ± {predstd:.5g} (R^2 = {score:.2f})'
    return render_template('result.html', file=file, form=session['form'],
                           outcome=outcome, result=result)


if __name__ == '__main__':
    Timer(1, webbrowser.open_new('http://127.0.0.1:5000/')).start()
    app.run(debug=False)

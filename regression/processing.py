__all__ = ['find_files', 'get_xy', 'process_data', 'predict_ols']

import csv
from glob import glob
import os

import pandas as pd
from sklearn.linear_model import LinearRegression


def find_files(extensions=['csv', 'xls', 'xlsx']):
    """Return all supported files with paths from app directories."""
    try:
        root = os.path.join(os.path.dirname(__file__), '..')
    except NameError:
        root = os.path.abspath('')
    files = {
        ''.join(filename.rsplit(root))[1:]: filename
        for dirpath, _, filenames in os.walk(root) for filename in [
            item for sublist in
            [glob(os.path.join(dirpath, f'*.{ext}')) for ext in extensions]
            for item in sublist
        ]
    }
    return files


def get_xy(filepath):
    """Return features and outcomes from the file."""
    if filepath.rsplit('.', 1)[1] == 'csv':
        with open(filepath) as f:
            dialect = csv.Sniffer().sniff(f.read(1024))
            sep = dialect.delimiter
        decimal = ',' if sep == ';' else '.'
        df = pd.read_csv(filepath, sep=sep, index_col=0, decimal=decimal)
    if filepath.split('.')[-1] in ['xls', 'xlsx']:
        df = pd.read_excel(filepath, index_col=0)
    df.columns = [label.replace(' ', '_') for label in df.columns]
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]
    return X, y


def _is_float(value):
    """Return True if value is a floating point number, False otherwise."""
    try:
        float(value)
        return True
    except ValueError:
        return False


def process_data(filepath, sample):
    """
    Ingest and format data from the input for regression analysis.

    Parameters
    ----------
    filepath : str
        Path to the file.
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
    X, y = get_xy(filepath)
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
        Data prepared by ``process_data`` function.

    Returns
    -------
    prediction : float
        Linear predicted value from a model.
    score : float
        Coefficient of determination R-squared of a prediction model.

    """
    model = LinearRegression()
    model.fit(X, y)
    prediction = float(model.predict(sample))
    score = model.score(X, y)
    return prediction, score

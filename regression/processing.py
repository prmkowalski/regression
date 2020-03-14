"""Module with a library of data processing functions."""

__all__ = [
    'find_files', 'get_xy', 'process_data', 'predict_ols', 'predict_gbr'
]


import csv
from glob import glob
import os

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import GradientBoostingRegressor


def find_files(where=None):
    """
    Return all supported files with paths.

    Parameters
    ----------
    where: str, optional
        Path to the starting directory.

    """
    extensions = ['csv', 'xls', 'xlsx']
    try:
        root = os.path.join(os.path.dirname(__file__), '..')
    except NameError:
        root = os.path.abspath('')
    top = root if not where else where
    files = {
        ''.join(filename.rsplit(top))[1:].replace('\\', '/'): filename
        for dirpath, _, filenames in os.walk(top) for filename in [
            item for sublist in
            [glob(os.path.join(dirpath, f'*.{ext}')) for ext in extensions]
            for item in sublist
        ]
    }
    return files


def get_xy(filepath):
    """Return features and outcomes from the file."""
    try:
        with open(filepath) as f:
            dialect = csv.Sniffer().sniff(f.read(1024))
            sep = dialect.delimiter
        decimal = ',' if sep == ';' else '.'
        df = pd.read_csv(filepath, sep=sep, index_col=0, decimal=decimal)
    except:
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
    
    https://en.wikipedia.org/wiki/Ordinary_least_squares

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


def predict_gbr(X, y, sample):
    """
    Run Gradient Boosting for regression model for data from the input.
    
    https://en.wikipedia.org/wiki/Gradient_boosting

    Parameters
    ----------
    X, y, sample
        Data prepared by ``process_data`` function.

    Returns
    -------
    predictions : dict of {str: float}
        The {alpha: prediction} pairs, where alpha is the significance
        level of the quantile loss function and prediction is the predicted
        value from a model.

    """
    alphas = {'lower': .1, 'mid': .5, 'upper': .9}
    predictions = {}
    for a in alphas:
        model = GradientBoostingRegressor(loss='quantile', alpha=alphas[a])
        model.fit(X, y)
        predictions[a] = float(model.predict(sample))
    return predictions

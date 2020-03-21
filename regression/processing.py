"""Module with a library of data processing functions."""

__all__ = ['find_files', 'get_xy', 'process_data', 'predict_ols']

import csv
from glob import glob
import itertools
import os

import pandas as pd
import statsmodels.api as sm


def find_files(where=None):
    """
    Return all supported files with paths.

    Parameters
    ----------
    where: str, optional
        Path to the starting directory.

    """
    extensions = ['csv', 'xls', 'xlsx']
    top = os.path.dirname(__file__) if not where else where
    files = {}
    for dirpath, _, _ in os.walk(top):
        paths = [glob(os.path.join(dirpath, f'*.{ext}')) for ext in extensions]
        for path in itertools.chain.from_iterable(paths):
            files[''.join(path.rsplit(top))[1:].replace('\\', '/')] = path
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
    df.index = df.index.fillna('Unlabeled')
    df.columns = [label.replace(' ', '_') for label in df.columns]
    df.replace(' ', '_', regex=True, inplace=True)
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


def predict_ols(X, y, sample, dof):
    """
    Run a simple ordinary least squares model for data from the input.

    https://en.wikipedia.org/wiki/Ordinary_least_squares

    Parameters
    ----------
    X, y, sample
        Data prepared by ``process_data`` function.
    dof : int
        The t-distribution degrees of freedom (observations - 1).

    Returns
    -------
    prediction_results : Series
        Contains prediction and prediction variance, confidence intervals
        for the prediction of the mean and of new observations and adjusted
        coefficient of determination.

    """
    model = sm.OLS(y, X)
    results = model.fit()
    prediction = results.get_prediction(sample)
    prediction.dist_args = [dof]
    prediction_results = prediction.summary_frame().squeeze()
    prediction_results['rsquared_adj'] = results.rsquared_adj
    return prediction_results

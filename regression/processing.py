__all__ = ['find_csv_files', 'process_data', 'predict_ols']

import csv
from glob import glob
import os

import pandas as pd
import statsmodels.api as sm
from statsmodels.sandbox.regression.predstd import wls_prediction_std


def find_csv_files():
    """Return a list of all CSV files in the application directories."""
    try:
        root = os.path.join(os.path.dirname(__file__), '..')
    except NameError:
        root = os.path.abspath('')
    csv_files = {''.join(filename.rsplit(root))[1:]: filename
                 for dirpath, _, filenames in os.walk(root)
                 for filename in glob(os.path.join(dirpath, '*.csv'))}
    return csv_files


def is_float(value):
    """Return True if value is a floating point number, False otherwise."""
    try:
        float(value)
        return True
    except ValueError:
        return False


def get_xy(csv_filepath):
    """Return features and outcomes from CSV file."""
    try:
        here = os.path.dirname(__file__)
    except NameError:
        here = os.path.abspath('')
    filepath = os.path.join(here, csv_filepath)
    with open(csv_filepath) as csv_file:
        dialect = csv.Sniffer().sniff(csv_file.read(1024))
        sep = dialect.delimiter
    decimal = ',' if sep == ';' else '.'
    df = pd.read_csv(filepath, sep=sep, header=0, index_col=0, decimal=decimal)
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
    X, y = get_xy(csv_filepath)
    sample = {feature: float(value.replace(',', '.', 1))
              if is_float(value.replace(',', '.', 1)) else value
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

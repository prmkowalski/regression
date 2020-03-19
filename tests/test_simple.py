import os

import numpy as np
import pandas as pd

from regression import app
from regression import processing as lib


def test_app():
    response = app.test_client().get('/')
    assert response.status_code == 200


def test_lib():
    alfa, beta, n = np.random.normal(), np.random.normal(), 50
    noise = np.random.normal(0, 3, n)
    X = np.linspace(-2 * n, 2 * n)
    y = alfa * X + beta + noise
    df = pd.DataFrame({'X': X, 'y': y})
    df.to_csv(os.path.join(os.path.dirname(__file__), 'data.csv'))

    files = lib.find_files(where='tests')
    element = np.random.randint(0, n)
    sample, actual = {'X': f'{X[element]}'}, y[element]

    X, y, sample = lib.process_data(files['data.csv'], sample)
    prediction = lib.predict_ols(X, y, sample, n - 1)['mean']
    assert np.isclose(actual, prediction, atol=.1 * n)

import os

import numpy as np
import pandas as pd

from regression import app
from regression import processing as lib


def test_app():
    response = app.test_client().get('/')
    assert response.status_code == 200


def test_lib():
    alfa, beta = np.random.normal(), np.random.normal()
    noise = np.random.normal(0, 3, 50)
    X = np.linspace(-100, 100)
    y = alfa * X + beta + noise
    df = pd.DataFrame({'X': X, 'y': y})
    df.to_csv(os.path.join(os.path.dirname(__file__), 'data.csv'))

    files = lib.find_files(where='tests')
    element = np.random.randint(0, 50)
    sample, actual = {'X': f'{X[element]}'}, y[element]

    X, y, sample = lib.process_data(files['data.csv'], sample)
    predictions = [
        lib.predict_ols(X, y, sample)[0],
        lib.predict_gbr(X, y, sample)['mid'],
    ]
    assert any([np.isclose(actual, p, atol=10) for p in predictions])

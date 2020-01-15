import os
import sys

import numpy as np
import pandas as pd

from regression import processing as lib

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


def test_regression():
    alfa, beta = np.random.normal(), np.random.normal()
    noise = np.random.normal(0, 3, 50)
    X = np.linspace(-100, 100)
    y = alfa * X + beta + noise
    df = pd.DataFrame({'X': X, 'y': y})
    df.to_csv(os.path.join(os.path.dirname(__file__), 'data.csv'))

    files = lib.find_files()
    element = np.random.randint(0, 50)
    sample, actual = {'X': f'{X[element]}'}, y[element]

    X, y, sample = lib.process_data(files['tests\\data.csv'], sample)
    predictions = [
        lib.predict_ols(X, y, sample)[0],
        lib.predict_gbr(X, y, sample)['mid'][0],
    ]
    assert any([np.isclose(actual, p, atol=10) for p in predictions])

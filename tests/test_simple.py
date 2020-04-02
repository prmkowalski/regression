from io import BytesIO
import os

import numpy as np
import pandas as pd

from regression import app
from regression import processing as lib


def test_lib():
    alfa, beta, n = np.random.normal(), np.random.normal(), 50
    noise = np.random.normal(0, 3, n)
    X = np.linspace(-100, 100)
    category = np.random.choice(['a', 'b'], n)
    y = alfa * X + beta + noise
    df = pd.DataFrame({'X': X, 'category': category, 'y': y})
    df.to_csv(os.path.join(os.path.dirname(__file__), 'test.csv'))
    df.to_excel(os.path.join(os.path.dirname(__file__), 'test.xlsx'))

    files = lib.find_files(os.path.dirname(__file__))
    assert [lib._allowed_file(f) for f in files]

    element = np.random.randint(0, n)
    form = {'X': f'{X[element]}', 'category': f'{category[element]}'}
    actual = y[element]
    X, y, sample = lib.process_data(files['test.xlsx'], form)
    prediction = lib.predict_ols(X, y, sample, n - 1)['mean']
    assert np.isclose(actual, prediction, atol=10)

    assert not lib._is_float('string')


def test_app():
    app.testing = True
    file = os.path.join('tests', 'test.csv')
    with app.test_client() as c:
        responses = [
            c.get('/'),
            c.post('/', content_type='multipart/form-data',
                   data=dict(file=(BytesIO(b'content'), 'upload.csv'))),
            c.post('/process', data={'file': f"('test', '{file}')"}),
            c.post('/result', data={'name': 'test', 'path': file,
                                    'X': '', 'category': ''}),
            c.post('/result', data={'name': 'test', 'path': file,
                                    'X': '120', 'category': 'a'})
        ]
        assert [r.status_code == 200 for r in responses]

"""Run on Flask's built-in server"""

from threading import Timer
import webbrowser

from regression import app

Timer(1, webbrowser.open_new('http://127.0.0.1:5000/')).start()
app.run(debug=False)

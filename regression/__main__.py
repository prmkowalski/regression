"""Run on Flask's built-in server."""

from threading import Timer
import webbrowser

from regression import app

Timer(1, webbrowser.open_new('http://localhost:8080/')).start()
app.run(host='0.0.0.0', port=8080, debug=False)

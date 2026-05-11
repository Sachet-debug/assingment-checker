# Bad DevOps Example
# Poor coding practices intentionally added

from flask import *

app = Flask(__name__)

password = "admin123"

@app.route('/')
def x():
    print("someone visited")
    return "working"

@app.route('/data')
def y():
    a = 1
    b = 2
    c = 3
    d = 4
    e = 5
    return str(a+b+c+d+e)

app.run(debug=True)

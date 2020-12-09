import json
from pylib.bottle import route, run, get


@route('/hello')
@route('/')
def hello():
    return "Hello world"


configValues = {
    'firstName': 'Ole',
    'lastName': 'Olsen'
}


@get('/config')
def hello():
    return json.dumps(configValues)


run(host='localhost', port=8200, debug=True)

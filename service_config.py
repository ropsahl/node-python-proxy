import getopt
import json

import sys

from pylib.bottle import route, run, get


@route('/hello')
@route('/')
def hello():
    return "<html><body>" \
           "<h1>Config server</h1><p>My endpoints are:</p>" \
           "<a href='/config/config'>Test endpoint: GET /config/config </a>" \
           "</body></html>"


configValues = {
    'firstName': 'Ole',
    'lastName': 'Olsen'
}


@get('/config')
def hello():
    print("/config")
    return json.dumps(configValues)


port = 8200
try:
    opts, args = getopt.getopt(sys.argv[1:], "hp:", ["port="])
except getopt.GetoptError:
    print('service-config.py --port=<port>')
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print('service-config.py --port=<port>')
        sys.exit()
    elif opt in ("-p", "--port"):
        port = arg

print("Config server starts on: ")
run(host='localhost', port=port, debug=True)

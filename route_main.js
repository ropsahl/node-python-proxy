const http = require('http')
const httpProxy = require('http-proxy')
const yargs = require('yargs')
const argv = yargs
  .option('port', {
    alias: 'p',
    description: 'Port for the this server'
  })
  .option('service', {
    alias: 's',
    description: 'Services to serve. Example --service.config.port=453845 -s.static.port=765'
  })
  .help()
  .alias('help', 'h')
  .argv

function getService (name) {
  return argv.service[name]
}

function getServiceLinks () {
  let ret = '<html><body><h1>Router with following services</h1><ul>'
  for (let s in argv.service) {
    ret += '<li><a href="/' + s + '">' + s + '</a></li>'
  }
  return ret + '</body></html>'

}

const route_main = httpProxy.createProxyServer({})

console.log('Staring on port:' + argv.port)

for (let s in argv.service) {
  console.log('Service:' + s)
}

const server = http.createServer((req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*')
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, OPTIONS')
  res.setHeader('Access-Control-Allow-Headers', 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token')

  console.log('Request: ' + req.url)
  var url = req.url
  var serviceName = url.split('/')[1]
  var service = getService(serviceName)
  req.url = url.substr(serviceName.length + 1)
  if (service !== undefined) {
    route_main.web(req, res, { target: 'http://localhost:' + service.port })
  } else {
    res.setHeader('Content-type', 'text/html')
    res.statusCode = 200
    res.end(getServiceLinks())
  }
}).listen(argv.port)

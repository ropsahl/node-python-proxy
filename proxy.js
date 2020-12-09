const http = require('http')
const httpProxy = require('http-proxy')
const proxy = httpProxy.createProxyServer({})

const server = http.createServer(function (req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*')
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, OPTIONS')
  res.setHeader('Access-Control-Allow-Headers', 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token')

  if (req.url.indexOf('/config') === 0) {
    proxy.web(req, res, { target: 'http://localhost:8200' })
  } else if (req.method === 'GET') {
    proxy.web(req, res, { target: 'http://localhost:8300' })
  }
}).listen(8100)

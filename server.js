const http = require('http');
const nodeStatic = require('node-static');
const fileServer = new nodeStatic.Server('./public');

http.createServer(function (req, res) {
  req.addListener('end', function () {
    fileServer.serve(req, res)
  }).resume()
}).listen(8300)

# Mini do it your self microservice example
This repo contains a minimal example for 
- node webserver for static files  microservice
- a pyhon rest service
- a node router
- a python convention based microservice controller

##up - microservice infrastructure
###up.sh 
Bash launcher 
###up.py 
The microservice controller, scans current directory and launch any .js, .py or .sh script with names starting 
  with service_ giving them a --port=<free port> argument and sending all stdout & stderr to up_log.sh.
 
  After launching the services it looks for a route_ script and lauches that with arguments to locate all services.
  
###up-log.sh 
Logs output from the different services in a consistent way

##service_config.py
A python REST server
- GET / response with link to all known services
##service_static_server.js
A node server serving static files
##route_main.js
A router for the services.
- GET / response with link to all known services


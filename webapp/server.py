from gevent.pywsgi import WSGIServer
from src import app

http_server = WSGIServer(("0.0.0.0", 3000), app)
http_server.serve_forever()
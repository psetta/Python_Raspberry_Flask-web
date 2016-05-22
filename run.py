#!flask/bin/python
from app import app

app.debug=True

applogger = app.logger

import logging
logging.basicConfig(filename='run.log',level=logging.DEBUG)

app.run(host='0.0.0.0',port=8001)

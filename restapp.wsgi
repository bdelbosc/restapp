activate_this = '/var/www/restapp/env/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
import sys
import os
sys.stdout = sys.stderr
os.environ['RESTAPP_CONF'] = '/var/www/restapp/restapp.conf'
from restapp import app as application
from restapp import db
db.create_all()
app.logger.info('Application started')

from flask import Flask, request, send_from_directory

from home import home
from viewer import viewer
from writer import writer
from whitelist import whitelist
from tags import tags
#from admin import admin
#from cookies import cook
from atom import atom

import os
import time
import daemon
import refresh
import pagemaker as p
import settings as s

_port = s._port
app = Flask(__name__,
            static_url_path = "",
            static_folder = "static",)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

app.register_blueprint(home)
app.register_blueprint(viewer)
app.register_blueprint(writer)
app.register_blueprint(whitelist)
app.register_blueprint(tags)
# app.register_blueprint(admin)
# app.register_blueprint(cook)
app.register_blueprint(atom)

if not os.path.isdir("./static/cap/"):
    os.mkdir("./static/cap/")
if not os.path.isdir("./archive/"):
    os.mkdir("./archive/")

@app.errorhandler(404)
def not_found(e):
    return p.mk(p.html("404"))

@app.route('/api/')
@app.route('/raw/')
def api_help():
    return base_static("help.html")
    
@app.route('/api/<path:filename>')
@app.route('/raw/<path:filename>')
def base_static(filename):
        return send_from_directory(app.root_path + '/threads/', filename)

if __name__ == '__main__':
    refresh.main()
    daemon.run()    
    app.run(host="0.0.0.0", port=_port)
    print(time.time.now())
    print(request.headers)

app.run()

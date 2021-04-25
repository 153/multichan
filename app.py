from flask import Flask, request, send_from_directory

from viewer import viewer
from writer import writer
from whitelist import whitelist
from tags import tags
from admin import admin
import os
import time
import daemon
import pagemaker as p
import settings as s

_port = s._port
app = Flask(__name__,
            static_url_path = "",
            static_folder = "static",)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

app.register_blueprint(viewer)
app.register_blueprint(writer)
app.register_blueprint(whitelist)
app.register_blueprint(tags)
app.register_blueprint(admin)

if not os.path.isdir("./static/cap/"):
    os.mkdir("./static/cap/")
if not os.path.isdir("./archive/"):
    os.mkdir("./archive/")

@app.errorhandler(404)
def not_found(e):
    return e

@app.route('/', strict_slashes=False)
def hello_world():
    print(request.headers)
    return p.mk(p.html("home").format(s.name))

@app.route('/rules')
def rules():
    return p.mk(p.html("rules"))

@app.route('/about')
def about():
    return p.mk(p.html("about"))

@app.route('/friends')
def friends():
    title = "<h1>Friends of " + s.name
    title += "</h1><h4>" + s.url + "</h4>"
    title +=  "Friends are other multichan websites that "
    title += "this server downloads threads and comments from."
    flist = []
    fstring = "<li> <a href='{1}'>{0}</a> {1}"
    for f in s.friends:
        flist.append(fstring.format(f, s.friends[f]))
    flist = "<ul>" + "\n".join(flist) + "</ul>"
    page = title + flist
    return p.mk(page)
    

@app.route('/api/')
@app.route('/raw/')
def api_help():
    return base_static("help.txt")
    
@app.route('/api/<path:filename>')
@app.route('/raw/<path:filename>')
def base_static(filename):
        return send_from_directory(app.root_path + '/threads/', filename)


if __name__ == '__main__':
    daemon.run()    
    app.run(host="0.0.0.0", port=_port)
    print(time.time.now())
    print(request.headers)

#app.run(debug=True)

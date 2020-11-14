from flask import Flask, request, send_from_directory

from viewer import viewer
from writer import writer
from whitelist import whitelist
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

@app.errorhandler(404)
def not_found(e):
    return e

@app.route('/', strict_slashes=False)
def hello_world():
    print(request.headers)
    links = """
<h2>{0}</h2>
<hr>
<center><img src="hands.png"></center>
<ul>
<li><a href="/about">About this website</a>
<li><a href="/rules">Rules of this website</a>
</ul><p><ul>
<li><a href="/threads/">Conversation index</a>
</ul> 
""".format(s.name)
    return p.mk(links)

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
    

@app.route('/raw/<path:filename>')
def base_static(filename):
        return send_from_directory(app.root_path + '/threads/', filename)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=_port, debug=True)
    print(request.headers)

app.run(debug=True)

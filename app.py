from flask import Flask
from flask import request

from viewer import viewer
from writer import writer
import pagemaker as p
import settings as s

app = Flask(__name__,
            static_url_path = "",
            static_folder = "static",)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

app.register_blueprint(viewer)
app.register_blueprint(writer)

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

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
    print(request.headers)

app.run(debug=True)

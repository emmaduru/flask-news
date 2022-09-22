from gevent import monkey
monkey.patch_all()
import os
import requests
import json

from gevent.pywsgi import WSGIServer
from flask import Flask, render_template, abort
from flask_compress import Compress


app = Flask(__name__)
compress = Compress()
compress.init_app(app)

def get_url(category):
    r = requests.get(
        f"https://newsapi.org/v2/top-headlines?country=us&category={category}&apiKey={os.environ.get('API_KEY')}"
    )
    headlines = json.loads(r.text)["articles"]
    return render_template("index.html", headlines=headlines)

@app.route("/")
def index():
  return get_url("")


@app.route("/<category>")
def category(category):
    if category == "business" or \
      category == "technology" or \
      category == "sports":
        return get_url(category)

    else:
        abort(404)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title='404'), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html', title='500'), 500

if __name__ == "__main__":
  http_server = WSGIServer(("0.0.0.0", 81), app)
  http_server.serve_forever()

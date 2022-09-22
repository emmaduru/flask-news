import os
import requests
import json
from flask import Flask, render_template, abort

app = Flask(__name__)


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


app.run(host='0.0.0.0', port=81)

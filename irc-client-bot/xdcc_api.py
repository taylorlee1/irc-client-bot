

from flask import Flask
from flask import jsonify
from flask import request
import GetListing
import html
import subprocess

app = Flask(__name__)

@app.route("/api/get-listing")
def hello():
  data = GetListing.get_listing()
  return jsonify(data)

@app.route("/api/get-file")
def get_file():
  filename = request.args.get('filename')
  filename = html.unescape(filename)
  proc = subprocess.run(['./screenit.sh', filename])
  d = {
    'msg' : 'started download of {}'.format(filename)
    }
  return jsonify(d)



import os
from flask import Flask
from flask import jsonify
from flask import request
import GetTopDl
import RemoveFile
import html
import subprocess

app = Flask(__name__)

@app.route("/api/get-top-dl")
def hello():
  data = GetTopDl.get_top_dl()
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

@app.route("/api/remove-file")
def remove_file():
    filename = request.args.get('filename')
    filename = html.unescape(filename)
    filename = os.path.basename(filename)
    r = RemoveFile.RemoveFile(filename)
    msg = r.remove_file()
    return jsonify(msg)

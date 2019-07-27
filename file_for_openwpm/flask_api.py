import getmap
from subprocess import call
from threading import Thread
import threading
import os
import sys
import platform
from subprocess import Popen
import subprocess
import time
from flask import Flask, jsonify, request
import requests
import json
from flask import abort
from flask import make_response


app = Flask(__name__)

num_workers = 2
output = "../database/sitemap.xml"

def subctrlthread():
    os.system("rm -rf ../database/requestdata1/*")
    os.system("rm -rf ../database/requestdata2/*")
    os.system("rm -rf ../database/requestdata3/*")
    os.system("rm -rf ../database/sites/*")
    # os.system("rm -rf ../database/apichecked/*")
    os.system("rm -rf ../database/sitemap.xml")
    subprocess.Popen('gnome-terminal -e "python getsites1.py"', shell=True)

def subctrlthread1(domain):
    subprocess.Popen('gnome-terminal -e "python3 main_control.py --domain ' + domain + '"', shell=True)


@app.route('/', methods=['POST'])
def run():
    if not request.json or not 'domain' in request.json:
        abort(400)
    thread = threading.Thread(target=subctrlthread)
    thread.start()

    domain = request.json['domain']
    thread = threading.Thread(target=subctrlthread1, args=(domain,))
    thread.start()

    return jsonify({'domain': domain})

@app.route('/api', methods=['POST'])
def get_api():
    # if not request.json:
    #     abort(400)

    # print(request.json)

    # task = {
    #     'content': request.json['content']
    # }
    return jsonify({'status': "200 OK"})
    

if __name__ == '__main__':
	app.run(host="localhost",port=5000,debug=True)
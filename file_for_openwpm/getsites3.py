from __future__ import absolute_import

from six.moves import range

from automation import CommandSequence, TaskManager

import os

import re

import time

from subprocess import call

from threading import Thread

import threading

import platform

from subprocess import Popen

import subprocess

import json

import sqlite3

from sqlite3 import Error

import requests

import sys
sys.path.append("../checkapi/")
import checkapi






siteslist = list()
with open('../database/sites/sites3.txt') as f:
    for line in f:
        siteslist.append(line)

NUM_BROWSERS = 1




def callWPM(NUM_BROWSERS, siteslist):
    print("Thread-----------thread-------------thread-----")
    manager_params, browser_params = TaskManager.load_default_params(NUM_BROWSERS)
    browser_params[0]['http_instrument'] = True
    browser_params[0]['disable_flash'] = False
    browser_params[0]['headless'] = True
    manager_params['data_directory'] = '../database/requestdata3/'
    manager_params['log_directory'] = '../database/requestdata3/'
    manager = TaskManager.TaskManager(manager_params, browser_params)
    for site in siteslist:
        command_sequence = CommandSequence.CommandSequence(site, reset=True)
        command_sequence.get(sleep=0, timeout=10)
        manager.execute_command_sequence(command_sequence, index='**')
    manager.close()

thread1 = threading.Thread(target=callWPM(NUM_BROWSERS, siteslist))
thread1.start()

###################################
def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None

startid = 1
stopid = 10

database = "../database/requestdata3/crawl-data.sqlite"
connt = create_connection(database)
cursor = connt.cursor()
checkapi = checkapi.checkapi("../database/requestdata3/crawl-data.sqlite", "../database/apichecked/result3.sqlite", startid, stopid)
checkapi.run()
###################################
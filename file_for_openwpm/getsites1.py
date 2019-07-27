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


def follow(file):
    file.seek(0,2)

    while True:
        line = file.readline()
        if not line:
            time.sleep(0.001)
            continue
        yield line

time.sleep(5)

sites = []


pathXML = os.path.join(os.path.expanduser('..'), 'database', 'sitemap.xml')
f = open(pathXML, mode ='r')


loglines = follow(f)
print('Begin')
for line in loglines:
    data = re.findall('<loc>((?:http|https):\/\/.+)<\/loc>',line)
    print("data: {0}".format(data))
    try:
        sites.append(data[0])
    except:
        print("-----------------------------------------")
        print("line: {0}".format(line))
        print("sites len: {0}".format(len(sites)))
        # print("sites: {0}".format(sites))
        print("-----------------------------------------")
        break

step = len(sites)//3

sites1 = sites[0:step]
with open('../database/sites/sites1.txt', 'w') as file_handler:
    for item in sites1:
        file_handler.write("{}\n".format(item))
sites2 = sites[step : step*2]
with open('../database/sites/sites2.txt', 'w') as file_handler:
    for item in sites2:
        file_handler.write("{}\n".format(item))
sites3 = sites[step*2 : ]
with open('../database/sites/sites3.txt', 'w') as file_handler:
    for item in sites3:
        file_handler.write("{}\n".format(item))

print(sites1)
print("--------------endsite1-----------")
print(sites2)
print("--------------endsite2-----------")
print(sites3)
print("--------------endsite3-----------")


NUM_BROWSERS = 1

def subctrlthread1():
    subprocess.Popen('gnome-terminal -e "python getsites2.py"', shell=True)

def subctrlthread2():
    subprocess.Popen('gnome-terminal -e "python getsites3.py"', shell=True)


thread2 = threading.Thread(target=subctrlthread1)
thread2.start()

thread3 = threading.Thread(target=subctrlthread2)
thread3.start()



def callWPM(NUM_BROWSERS, sites):
    print("Thread-----------thread-------------thread-----")
    manager_params, browser_params = TaskManager.load_default_params(NUM_BROWSERS)
    browser_params[0]['http_instrument'] = True
    browser_params[0]['disable_flash'] = False
    browser_params[0]['headless'] = True
    manager_params['data_directory'] = '../database/requestdata1/'
    manager_params['log_directory'] = '../database/requestdata1/'
    manager = TaskManager.TaskManager(manager_params, browser_params)
    for site in sites:
        command_sequence = CommandSequence.CommandSequence(site, reset=True)
        command_sequence.get(sleep=0, timeout=60)
        manager.execute_command_sequence(command_sequence, index='**')
    manager.close()

thread1 = threading.Thread(target=callWPM(NUM_BROWSERS, sites))
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

database = "../database/requestdata1/crawl-data.sqlite"
connt = create_connection(database)
cursor = connt.cursor()
checkapi = checkapi.checkapi("../database/requestdata1/crawl-data.sqlite", "../database/apichecked/result1.sqlite", startid, stopid)
checkapi.run()
###################################
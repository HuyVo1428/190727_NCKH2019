from __future__ import absolute_import

from six.moves import range

from automation import CommandSequence, TaskManager

from threading import Thread
import threading

import os

import re

import time

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

startiddb = 1
stopiddb = 10

pathXML = os.path.join(os.path.expanduser('..'), 'database', 'sitemap.xml')
f = open(pathXML, mode ='r')
loglines = follow(f)
for line in loglines:
    data = re.findall('<loc>((?:http|https):\/\/.+)<\/loc>',line)
    sites.append(data[0])

    NUM_BROWSERS = 1


    manager_params, browser_params = TaskManager.load_default_params(NUM_BROWSERS)

    for i in range(NUM_BROWSERS):
        browser_params[0]['http_instrument'] = True
        browser_params[0]['disable_flash'] = False
        browser_params[0]['headless'] = True

    manager_params['data_directory'] = '../database/requestdata'
    manager_params['log_directory'] = '../database/openwpmlog'

    manager = TaskManager.TaskManager(manager_params, browser_params)

    for site in sites:
        command_sequence = CommandSequence.CommandSequence(site)

        command_sequence.get(sleep=0, timeout=60)

        command_sequence.dump_profile_cookies(120)

        manager.execute_command_sequence(command_sequence, index='**')


    manager.close()

thread = threading.Thread(target=subctrlthread)
thread.start()

def subctrlthread():
    database = "../database/requestdata/crawl-data.sqlite"
    connt = create_connection(database)
    cursor = connt.cursor()
    stopiddb = cursor.execute("SELECT MAX(id) FROM http_requests;")


    startid = stopiddb - startiddb
    stopid = stopiddb

    startiddb = stopid + 1
    checkapi = checkapi.checkapi("../database/requestdata/crawl-data.sqlite", "../database/apichecked/result.sqlite", startid, stopid)
    checkapi.run()
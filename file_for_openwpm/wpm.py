from __future__ import absolute_import

from six.moves import range

from automation import CommandSequence, TaskManager

import os
import re
import time
def follow(file):
    file.seek(0,2)
    while True:
        line = file.readline()
        if not line:
            time.sleep(0.001)
            continue
        yield line

sites = []

pathXML = os.path.join(os.path.expanduser('..'), 'database', 'sitemap.xml')
f = open(pathXML, mode ='r')
loglines = follow(f)
for line in loglines:
        #print("hello word")
        data = re.findall('<loc>((?:http|https):\/\/.+)<\/loc>',line)
        sites.append(data[0])
        NUM_BROWSERS = 1
        manager_params, browser_params = TaskManager.load_default_params(NUM_BROWSERS)

        for i in range(NUM_BROWSERS):
                browser_params[i]['http_instrument'] = True
                browser_params[i]['disable_flash'] = False
                browser_params[0]['headless'] = True  

        manager_params['data_directory'] = '../db'
        manager_params['log_directory'] = '../log'

        manager = TaskManager.TaskManager(manager_params, browser_params)

        for site in sites:
                command_sequence = CommandSequence.CommandSequence(site)

        command_sequence.get(sleep=0, timeout=60)

        command_sequence.dump_profile_cookies(120)

        manager.execute_command_sequence(command_sequence, index='**')

        manager.close()

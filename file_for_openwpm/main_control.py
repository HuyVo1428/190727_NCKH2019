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
import argparse



parser = argparse.ArgumentParser(description='Crawler pour la creation de site map')
group = parser.add_mutually_exclusive_group()
group.add_argument('--domain', action="store", default="", help="Target domain (ex: http://blog.lesite.us)")

arg = parser.parse_args()
dict_arg = arg.__dict__



domain= dict_arg['domain']
num_workers = 2
output = "../database/sitemap.xml"

mysys = getmap.getmap(domain, num_workers, output)
mysys.run() 
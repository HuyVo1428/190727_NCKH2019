#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import os

import json

import sys
sys.path.append("../sitemap/")
import crawler_sitemap


class getmap():
	# Gestion des parametres
	parser = argparse.ArgumentParser(description='Crawler pour la creation de site map')

	parser.add_argument('--skipext', action="append", default=[], required=False, help="File extension to skip")
	parser.add_argument('-n', '--num-workers', type=int, default=1, help="Number of workers if multithreading")
	#parser.add_argument('--timeout', type=int, default=30)
	parser.add_argument('--parserobots', action="store_true", default=False, required=False, help="Ignore file defined in robots.txt")
	parser.add_argument('--debug', action="store_true", default=False, help="Enable debug mode")
	parser.add_argument('-v', '--verbose', action="store_true", help="Enable verbose output")
	parser.add_argument('--output', action="store", default=None, help="Output file")
	parser.add_argument('--exclude', action="append", default=[], required=False, help="Exclude Url if contain")
	parser.add_argument('--drop', action="append", default=[], required=False, help="Drop a string from the url")
	parser.add_argument('--report', action="store_true", default=False, required=False, help="Display a report")
	parser.add_argument('--images', action="store_true", default=False, required=False, help="Add image to sitemap.xml (see https://support.google.com/webmasters/answer/178636?hl=en)")

	group = parser.add_mutually_exclusive_group()
	group.add_argument('--config', action="store", default=None, help="Configuration file in json format")
	group.add_argument('--domain', action="store", default="", help="Target domain (ex: http://blog.lesite.us)")

	arg = parser.parse_args()

	def __init__(self, domain, num_workers, output):
		self.domain = domain
		self.num_workers = num_workers
		self.output = output
	
	def run(self):
		# Read the config file if needed
		if self.arg.config is not None:
			try:
				config_data = open(self.arg.config,'r')
				config = json.load(config_data)
				config_data.close()
			except Exception as e:
				config = {}
		else:
			config = {}

		# Overload config with flag parameters
		dict_arg = self.arg.__dict__
		dict_arg["domain"] = self.domain
		dict_arg["num_workers"] = self.num_workers
		dict_arg["output"] = self.output

		print(dict_arg)
		for argument in config:
			if argument in dict_arg:
				if type(dict_arg[argument]).__name__ == 'list':
					dict_arg[argument].extend(config[argument])
				elif type(dict_arg[argument]).__name__ == 'bool':
					if dict_arg[argument]:
						dict_arg[argument] = True
					else:
						dict_arg[argument] = config[argument]
				else:
					dict_arg[argument] = config[argument]
		del(dict_arg['config'])

		if dict_arg["domain"] == "":
			print ("You must provide a domain to use the crawler.")
			exit()

		crawl = crawler_sitemap.Crawler(**dict_arg)
		crawl.run()

		if self.arg.report:
			crawl.make_report()

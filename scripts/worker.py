#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import shutil
from spider import Spider

class Worker(object):
	def __init__(self, subs_path):
		super(Worker, self).__init__()
		self.subs_path = subs_path
		self.parse_json()

	def parse_json(self):
		subs_json = {}
		with open(self.subs_path, 'r') as f:
			subs_json = f.read()
		self.subs = json.loads(subs_json)

	def start_spider(self, target_folder):
		if os.path.exists(target_folder):
			shutil.rmtree(target_folder)
		os.mkdir(target_folder)
		for cat in self.subs:
			for title in self.subs[cat]:
				spider = Spider(cat, title, self.subs[cat][title])
				spider.write_htmls(target_folder)

def main():
	subs_path = './scripts/subscribe.json'
	target_folder = './_posts/'

	worker = Worker(subs_path)
	worker.start_spider(target_folder)

if __name__ == '__main__':
	main()
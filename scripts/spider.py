#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import hashlib
import feedparser
from bs4 import BeautifulSoup

class Spider(object):
	def __init__(self, cat, title, url):
		super(Spider, self).__init__()
		self.cat = cat
		self.title = title
		self.url = url
		self.parse_url()
		print('Crawling', self.title)
		
	def parse_url(self):
		self.src = feedparser.parse(self.url)

	def get_feed_title(self):
		return self.title

	def get_article_category(self):
		return self.cat;

	def get_article_title(self, idx):
		return self.src.entries[idx].title

	def get_article_link(self, idx):
		return self.src.entries[idx].link

	def get_article_date(self, idx):
		date_parsed = self.src.entries[idx].published_parsed
		return time.strftime("%Y-%m-%d %H:%M:%S", date_parsed)

	def get_article_description(self, idx):
		description = self.src.entries[idx].summary.replace('\n', ' ')
		raw_description = BeautifulSoup(description, 'lxml').get_text()
		if len(raw_description) >= 150:
			raw_description = raw_description[:150]
		return raw_description.replace(':', ' ')

	def get_article_content(self, idx):
		content = ''
		if 'content' in self.src.entries[idx]:
			content = self.src.entries[idx].content[0].value
		else:
			content = self.src.entries[idx].summary.replace('\n', ' ')
		return content

	def clean_html(self, html):
		html = html.replace('\n', ' ')
		html = html.replace(':', ' ')
		html = html.replace('https//', 'https://')

	def write_html(self, idx, target_folder):
		target_name = self.get_article_date(idx).split()[0] + '-' + \
			hashlib.md5(self.get_article_title(idx).encode('utf-8')).hexdigest() + '.html'
		header = u'---\n'\
				 u'layout:      post\n'\
				 u'title:       {}\n'\
				 u'link:        {}\n'\
				 u'date:        {}\n'\
				 u'category:    {}\n'\
				 u'source:      {}\n'\
				 u'description: {}\n'\
				 u'---\n\n'.format(self.get_article_title(idx),
				  	          	 self.get_article_link(idx),
				  	          	 self.get_article_date(idx),
				  	          	 self.get_article_category(),
				  	          	 self.get_feed_title(),
				  	          	 self.get_article_description(idx))
		with open(os.path.join(target_folder, target_name), 'w') as f:
			f.write(header + self.get_article_content(idx))

	def write_htmls(self, target_folder):
		for idx in range(len(self.src.entries)):
			self.write_html(idx, target_folder)

def main():
	cat = '新兴媒体'
	source = '虎嗅网'
	rss_url = 'https://www.huxiu.com/rss/0.xml'
	target_folder = './_posts/'

	spider = Spider(cat, source, rss_url)
	spider.write_htmls(target_folder)

if __name__ == '__main__':
	main()
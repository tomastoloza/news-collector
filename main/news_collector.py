import configparser
import time
import xml
from urllib import request
from urllib.error import URLError
from xml.etree.ElementTree import ElementTree

import feedparser


class NewsCollector(object):
    def __init__(self):
        self.parser = configparser.ConfigParser()
        self.parser.read("../config.ini")

    def get_rss_urls(self):
        rss_list = []
        items = []
        for section in self.parser.sections():
            items.append(self.parser.items(section))
        for item in items:
            for rss in [item[x][1] for x in range(4, len(item))]:
                rss_list.append(item[3][1] + rss)
        return rss_list

    def get_entries(self):
        entries = []
        for rss in (self.get_rss_urls()):
            feed = feedparser.parse(rss)
            for entry in feed["entries"]:
                entries.append(entry)
        return entries

    def create_xml(self):
        # TODO: create xml files from @urlopen
        for url in self.get_rss_urls():
            try:
                urlopen = request.urlopen(url)
                parse = ElementTree().parse(urlopen)
                print(parse.tag)
            except URLError:
                pass


if __name__ == '__main__':
    nc = NewsCollector()
    nc.create_xml()

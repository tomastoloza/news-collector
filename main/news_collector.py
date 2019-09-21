import configparser
import time
import xml
from urllib import request
from urllib.error import URLError
from xml.etree.ElementTree import ElementTree, tostring, fromstring, Element
from xml.dom import minidom
from urllib.request import urlopen

import feedparser


class NewsCollector(object):
    def __init__(self):
        self.parser = configparser.ConfigParser()
        self.parser.read("../config.ini")

    # TODO: return tuple of (url, name) pairs
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

    def create_element_tree(self):
        try:
            for url in self.get_rss_urls():
                resource = request.urlopen(url)
                element = fromstring(resource.read())
                with open("../resources/rss/" + str(element) + ".xml", 'w+') as file:
                    root = Element("news")
                    tree = ElementTree(root)
                    print(tree.getroot())
                    for a in element:
                        for b in a:
                            new = Element("news_item")
                            for c in b:
                                if c.tag == "title" or c.tag == "description" or c.tag == "pubDate":
                                    new.append(c)
                                root.append(new)
                    # tree.write(file, encoding="unicode")
        except URLError as e:
            print(e)


if __name__ == '__main__':
    nc = NewsCollector()
    nc.create_element_tree()
    # nc.create_xml()

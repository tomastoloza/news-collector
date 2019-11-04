import configparser
import os
from urllib import request
from xml.etree import ElementTree
from xml.etree.ElementTree import ElementTree, fromstring, Element
import xml.etree.ElementTree as ET


class NewsCollector(object):
    def __init__(self):
        self.parser = configparser.ConfigParser()
        self.parser.read("../config.ini")

    def get_rss_urls(self):
        rss_list = []
        default_size = len(self.parser.defaults())
        for section in self.parser.sections():
            item = self.parser.items(section)
            for num in range(default_size + 1, len(item)):
                rss_list.append((section, item[num][0], item[default_size][1] + item[num][1]))
        return rss_list

    def collect_news(self, rss):
        print(rss)
        file_name = "../resources/rss/" + rss[0] + "/" + rss[1] + ".xml"
        header = {
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"}
        req = request.Request(url=rss[2], headers=header)
        result = request.urlopen(req)
        element = fromstring(result.read())
        try:
            xml_parsed = ET.parse(file_name)
        except FileNotFoundError:
            root = Element("news")
            xml_parsed = ElementTree(root)
            if not os.path.isdir('../resources/rss/' + rss[0]):
                os.makedirs("../resources/rss/" + rss[0])
            open(file_name, 'w+')

        for item in element.findall(".//item"):
            news_item = Element("item")
            for tag in item:
                if tag.tag == "title" or tag.tag == "description" or tag.tag == "pubDate":
                    news_item.append(tag)
            if not self.find_item(news_item, file_name):
                xml_parsed.getroot().append(news_item)
        xml_parsed.write(file_name, encoding='UTF-8')

    def find_item(self, item, file_name):
        try:
            if open(file_name, 'r').read() != '':
                xml_parsed = ET.parse(file_name)
                for x in xml_parsed.getroot():
                    # TODO: verificacion por fecha
                    if x[0].text == item[0].text:
                        return True
            return False
        except ET.ParseError as e:
            e.with_traceback()

    def iterate_rss(self):
        for rss in self.get_rss_urls():
            try:
                self.collect_news(rss)
            except Exception as e:
                print('Oops! Something out of reach happened: ' + str(e))


if __name__ == '__main__':
    nc = NewsCollector()
    nc.iterate_rss()

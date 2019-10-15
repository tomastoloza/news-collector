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

    # TODO: return tuple of (url, name) pairs
    def get_rss_urls(self):
        rss_list = []
        default_size = len(self.parser.defaults())
        for section in self.parser.sections():
            item = self.parser.items(section)
            for num in range(default_size + 1, len(item)):
                rss_list.append((section, item[num][0], item[default_size][1] + item[num][1]))
        return rss_list

    def save_rss_from_url(self):
        for rss in self.get_rss_urls():
            header = {
                'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"}
            req = request.Request(url=rss[2], headers=header)
            result = request.urlopen(req)
            path = "../resources/temp/rss/" + rss[0]
            element = fromstring(result.read())
            root = Element("news")
            tree = ElementTree(root)
            print(rss[2])
            for item in element.findall(".//item"):
                new = Element("item")
                for tag in item:
                    if tag.tag == "title" or tag.tag == "description" or tag.tag == "pubDate":
                        new.append(tag)
                root.append(new)
            if not os.path.exists(path):
                os.makedirs(path)
            with open(path + "/" + rss[1] + ".xml", 'w+') as file:
                tree.write(file, encoding="unicode", xml_declaration=False)

    def read_and_compare(self):
        for rss in self.get_rss_urls():
            path = "../resources/rss/" + rss[0]
            path_temp = "../resources/temp/rss/" + rss[0]
            with open(path_temp + "/" + rss[1] + ".xml", 'r') as file:
                if file.read() != '':
                    try:
                        xml_parsed = ET.parse(path_temp + "/" + rss[1] + ".xml")
                        for item_element in xml_parsed.getroot():
                            for x in item_element:
                                if x.tag == 'title':
                                    print(x.text)
                    except ET.ParseError as e:
                        e.with_traceback()
                else:
                    xml_parsed
                if not os.path.exists(path):
                    os.makedirs(path)
                with open(path + "/" + rss[1] + ".xml", 'w+') as file_read:
                    xml_parsed.write(file_read, encoding='unicode')


if __name__ == '__main__':
    nc = NewsCollector()
    # nc.create_element_tree()
    # nc.get_rss_urls()
    # nc.fuckin_tree()
    # nc.save_rss_from_url()
    nc.read_and_compare()

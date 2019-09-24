import configparser
import os
from urllib import request
from urllib.error import URLError
from xml.etree.ElementTree import ElementTree, tostring, fromstring, Element, SubElement
from xml.etree import ElementTree


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

    def fuckin_tree(self):
        for rss in self.get_rss_urls():
            header = {
                'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"}
            req = request.Request(url=rss[2], headers=header)
            result = request.urlopen(req)
            element = fromstring(result.read())
            if not os.path.exists("../resources/rss/" + rss[0]):
                os.makedirs("../resources/rss/" + rss[0])
            with open("../resources/rss/" + rss[0] + "/" + rss[1] + ".xml", 'w+') as file:
                print("../resources/rss/" + rss[0] + "/" + rss[1] + ".xml")
                root = Element("news")
                tree = ElementTree.ElementTree(root)
                for item in element.findall(".//item"):
                    new = Element("item")
                    for tag in item:
                        if tag.tag == "title" or tag.tag == "description" or tag.tag == "pubDate":
                            new.append(tag)
                    root.append(new)
                tree.write(file, encoding="unicode")

    # def tuher(self):
    #     with open("../resources/rss/TN/la viola.xml", "r") as file:
    #         xml_parsed = ElementTree.ElementTree().parse(file, parser=None)
    #     print(xml_parsed)


if __name__ == '__main__':
    nc = NewsCollector()
    # nc.create_element_tree()
    # nc.get_rss_urls()
    nc.fuckin_tree()
    # nc.tuher()

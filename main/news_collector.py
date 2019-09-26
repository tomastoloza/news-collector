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

    def fuckin_tree(self):
        for rss in self.get_rss_urls():
            header = {
                'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"}
            req = request.Request(url=rss[2], headers=header)
            result = request.urlopen(req)
            element = fromstring(result.read())
            path = "../resources/rss/" + rss[0]

            print(rss[2])
            root = Element("news")
            tree = ElementTree(root)
            if not os.path.exists(path):
                os.makedirs(path)
            with open(path + "/" + rss[1] + ".xml", 'w+') as file:
                read = file.read()
                for item in element.findall(".//item"):
                    new = Element("item")
                    for tag in item:
                        if tag.tag == "title" or tag.tag == "description" or tag.tag == "pubDate":
                            new.append(tag)
                    root.append(new)
                try:
                    xml_parsed = fromstring((path + "/" + rss[1] + ".xml"))
                    print(xml_parsed)
                except ET.ParseError as e:
                    print(e)
                finally:
                    tree.write(file, encoding="unicode", xml_declaration=True)

    def tuher(self):
        with open("../resources/rss/TN/la viola.xml", "r") as file:
            xml_parsed = ElementTree().parse(file, parser=None)
            print(xml_parsed[0][0].text)


if __name__ == '__main__':
    nc = NewsCollector()
    # nc.create_element_tree()
    # nc.get_rss_urls()
    nc.fuckin_tree()
    # nc.tuher()

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

    def create_element_tree(self):
        try:
            print(self.get_rss_urls())
            for url in self.get_rss_urls():
                print(url)
                resource = request.urlopen(url[2])
                element = fromstring(resource.read())
                print(url[0])
                if not os.path.exists("../resources/rss/" + url[0]):
                    os.mkdir("../resources/rss/" + url[0])
                with open("../resources/rss/" + url[0] + "/" + url[1] + ".xml", 'w+') as file:
                    root = Element("news")
                    tree = ElementTree(root)
                    for a in element:
                        for b in a:
                            new = Element("news:item")
                            for c in b:
                                if c.tag == "title" or c.tag == "description" or c.tag == "pubDate":
                                    new.append(c)
                                root.append(new)
                    tree.write(file, encoding="unicode")
        except URLError as e:
            print(e)

    def fuckin_tree(self):
        for rss in self.get_rss_urls():
            resource = request.urlopen(rss[2])
            element = fromstring(resource.read())
            # if not os.path.exists("../resources/rss/" + rss[0]):
            #     os.makedirs("../resources/rss/" + rss[0])
            # with open("../resources/rss/" + rss[0] + "/" + rss[1] + ".xml", 'w+') as file:
            feed = element.findall(".//item/")
            news = Element("news")
            news_item = SubElement(news, "news:item")
            title = feed.(".//title")
            print(title)


if __name__ == '__main__':
    nc = NewsCollector()
    # nc.create_element_tree()
    # nc.get_rss_urls()
    nc.fuckin_tree()

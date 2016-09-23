import os
from xml.dom.minidom import parse

sample_config_file = "../config/config.xml"
feed_tag_name = "feed"
link_tag_name = "link"
parser_tag_name = "parser"

def get_keyword_from_xml(config_file = sample_config_file):
    if os.path.isfile(config_file):
        keywords = []
        xml_dom = parse(config_file)
        root = xml_dom.documentElement
        items = root.getElementsByTagName(kw_tag_name)
        for item in items:
            one_keyword = item.childNodes[0].data
            keywords.append(one_keyword)
        return keywords
    else:
        return []

def get_feeds_from_xml(config_file = sample_config_file):
    if os.path.isfile(config_file):
        feeds = []
        xml_dom = parse(config_file)
        root = xml_dom.documentElement
        feed_nodes = root.getElementsByTagName(feed_tag_name)
        for feed_node in feed_nodes:
            one_feed = { 
                           'link': feed_node.getElementsByTagName(link_tag_name)[0].firstChild.data,
                           'parser': feed_node.getElementsByTagName(parser_tag_name)[0].firstChild.data,
                       }
            feeds.append(one_feed)
        return feeds
    else:
        return []
 
if __name__ == '__main__':
    feeds = get_feeds_from_xml(sample_config_file)
    if len(feeds) > 0:
        print len(feeds), "feeds are fetched from the file <" + sample_config_file + ">" 
        for feed in feeds:
            print feed


import feedparser
import my_log
import re
import string
import urllib2
import timestamp_fetcher
from GeneralParser import GeneralParser

class WallOutsideParser(GeneralParser):

    def get_full_description(self, entry):
        ret_str = entry.description
        pattern = re.compile('<.+>')
        ret_str = pattern.sub('', ret_str)
        pattern = re.compile('\n')
        ret_str = pattern.sub('</p><p>', ret_str)
        return '<p>' + ret_str + '</p>'

if __name__ == "__main__":
    feed_info = {} 
    feed_info['link'] = 'http://feeds.feedburner.com/letscorp/aDmw'
    feed_info['parser'] = 'WallOutsideParser'
    feed_info['nick'] = 'WallOutside'
    feed_info['keywords'] = []
    parser = eval("WallOutsideParser(feed_info)")
    feed_data = parser.parse()
    print ' '*1 + 'feed_title: ' + feed_data['title']
    print ' '*1 + 'entries: '
    for entry in feed_data['entries']:
        print ' '*3 + 'entry_title: ' + entry['title']
        print ' '*3 + 'entry_des: ' + entry['description']
        #print ' '*3 + 'entry_content: ' + entry['content']

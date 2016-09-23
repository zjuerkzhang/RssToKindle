import feedparser
import my_log
import re
import string
import urllib2

class WallOutsideParser(object):
    def __init__(self, link):
        self.feed_link = link

    def __get_full_description(self, entry):
        ret_str = entry.description
        pattern = re.compile('<.+>')
        ret_str = pattern.sub('', ret_str)
        pattern = re.compile('\n')
        ret_str = pattern.sub('\n<p></p>', ret_str)
        return ret_str        

    def parse(self): 
        feed = feedparser.parse(self.feed_link)
        feed_data = {
                        'title': feed.feed.title,
                        'entries': [],
                    }
        for entry in feed.entries:
            entry_data = {
                             'title': entry.title,
                             'description': self.__get_full_description(entry),
                             #'content': entry.content[0].value,
                         }
            feed_data['entries'].append(entry_data)
        return feed_data

if __name__ == "__main__":
    parser = eval("WallOutsideParser('http://feeds.feedburner.com/letscorp/aDmw')")
    feed_data = parser.parse()
    print ' '*1 + 'feed_title: ' + feed_data['title']
    print ' '*1 + 'entries: '
    for entry in feed_data['entries']:
        print ' '*3 + 'entry_title: ' + entry['title']
        print ' '*3 + 'entry_des: ' + entry['description']
        #print ' '*3 + 'entry_content: ' + entry['content']

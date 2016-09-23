import feedparser
import my_log
import re
import string
import urllib2
import timestamp_fetcher

class GeneralParser(object):
    def __init__(self, link):
        self.feed_link = link

    def get_full_description(self, entry):
        ret_str = entry.description
        return ret_str        

    def __is_entry_new(self, entry, last_time):
        entry_time = "%04d%02d%02d%02d%02d%02d" % entry.published_parsed[:6]
        my_log.debug_print("entry %s published at %s" % (entry.title, entry_time))
        if cmp(entry_time, last_time) > 0:
            my_log.debug_print("===> New item")
            return (True, entry_time)
        else:
            my_log.debug_print("===> [old one]")
            return (False, '')

    def parse(self): 
        last_time = timestamp_fetcher.getStoredTimestamp(self.__class__.__name__)
        update_time = last_time
        my_log.debug_print("last_time for %s %s" % (self.__class__.__name__, last_time))
        feed = feedparser.parse(self.feed_link)
        feed_data = {
                        'title': feed.feed.title,
                        'entries': [],
                    }
        for entry in feed.entries:
            (b_newer, entry_time) = self.__is_entry_new(entry, last_time)
            if b_newer:
                if cmp(entry_time, update_time) > 0:
                    update_time = entry_time
                entry_data = {
                                 'title': entry.title,
                                 'description': self.get_full_description(entry),
                                 #'content': entry.content[0].value,
                             }
                feed_data['entries'].append(entry_data)
        if len(feed_data['entries']) > 0:
            timestamp_fetcher.updateStoredTimestamp(self.__class__.__name__, update_time)
        return feed_data
'''
if __name__ == "__main__":
    parser = eval("WallOutsideParser('http://feeds.feedburner.com/letscorp/aDmw')")
    feed_data = parser.parse()
    print ' '*1 + 'feed_title: ' + feed_data['title']
    print ' '*1 + 'entries: '
    for entry in feed_data['entries']:
        print ' '*3 + 'entry_title: ' + entry['title']
        #print ' '*3 + 'entry_des: ' + entry['description']
        #print ' '*3 + 'entry_content: ' + entry['content']
'''

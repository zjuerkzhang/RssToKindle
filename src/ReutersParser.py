import feedparser
import my_log
import re
import string
import urllib2

class ReutersParser(object):
    def __init__(self, link):
        self.feed_link = link

    def fetch_content_from_link(self,link):
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
               'Accept-Encoding': 'none',
               'Accept-Language': 'en-US,en;q=0.8',
               'Connection': 'keep-alive'}
        req = urllib2.Request(link, headers=hdr)
        try:
            page = urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            my_log.write_to_log_file(e.fp.read())
            return ''
        html = page.read()
        pattern = re.compile('<span id="article-text">.*?</span></span>', re.S)
        strs = pattern.findall(html)
        content = strs[0]
        re_add_nl = re.compile('<span[^>]+>')
        content = re_add_nl.sub('', content)
        re_filter = re.compile('</span>')
        content = re_filter.sub('', content)
        return content
    
    def parse(self): 
        feed = feedparser.parse(self.feed_link)
        feed_data = {
                        'title': feed.feed.title,
                        'entries': [],
                    }
        for entry in feed.entries:
            entry_data = {
                             'title': entry.title,
                             'description': self.fetch_content_from_link(entry.link),
                             #'content': entry.content[0].value,
                         }
            feed_data['entries'].append(entry_data)
        return feed_data

if __name__ == "__main__":
    parser = eval("ReutersParser('http://cn.reuters.com/rssFeed/CNAnalysesNews/')")
    feed_data = parser.parse()
    print ' '*1 + 'feed_title: ' + feed_data['title']
    print ' '*1 + 'entries: '
    for entry in feed_data['entries']:
        print ' '*3 + 'entry_title: ' + entry['title']
        print ' '*3 + 'entry_des: ' + entry['description']
        #print ' '*3 + 'entry_content: ' + entry['content']

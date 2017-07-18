import feedparser
import my_log
import re
import string
import urllib2
import timestamp_fetcher
from GeneralParser import GeneralParser

class ReutersParser(GeneralParser):
    def get_full_description(self,entry):
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
               'Accept-Encoding': 'none',
               'Accept-Language': 'en-US,en;q=0.8',
               'Connection': 'keep-alive'}
        req = urllib2.Request(entry.link, headers=hdr)
        try:
            page = urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            my_log.write_to_log_file(e.fp.read())
            return ''
        html = page.read()
        pattern = re.compile('<div class="ArticleBody_body_2ECha" data-reactid="\d+">.*?</div></div>', re.S)
        strs = pattern.findall(html)
        content = ""
        if len(strs) > 0:
            content = strs[0]
            re_add_nl = re.compile('<div[^>]+>')
            content = re_add_nl.sub('', content)
            re_filter = re.compile('</div>')
            content = re_filter.sub('', content)
            re_filter = re.compile('data-reactid="\d+"')
            content = re_filter.sub('', content)
            my_log.debug_print(content)
        return content

if __name__ == "__main__":
    feed_info = {}
    feed_info['link'] = 'http://cn.reuters.com/rssFeed/CNAnalysesNews/'
    feed_info['parser'] = 'ReutersParser'
    feed_info['nick'] = 'ReutersParser'
    feed_info['keywords'] = []
    parser = eval("ReutersParser(feed_info)")
    feed_data = parser.parse()
    print ' '*1 + 'feed_title: ' + feed_data['title']
    print ' '*1 + 'entries: '
    for entry in feed_data['entries']:
        print ' '*3 + 'entry_title: ' + entry['title']
        print ' '*3 + 'entry_des: ' + entry['description']
        #print ' '*3 + 'entry_content: ' + entry['content']

from datetime import date, timedelta, datetime
from shutil import copy
from os import path, listdir, system
import feedparser
from jinja2 import Environment, PackageLoader
import codecs
import get_feed_config
from ReutersParser import ReutersParser
from WallOutsideParser import WallOutsideParser
from FTParser import FTParser
import my_log
import sys


templates_env = Environment(loader=PackageLoader('RSSToKindle', 'templates'))
ROOT = path.dirname(path.abspath(__file__))
reload(sys)  
sys.setdefaultencoding('utf8')  



def build(config_file, output_dir ):
    """
    Given a list of feeds URLs and the path of a directory, writes the necessary
    for building a MOBI document.

    max_old must be either None or a timedelta. It defines the maximum age of
    posts which should be considered.
    """

    # Give the feeds URLs to Feedparser to have nicely usable feed objects.
    feeds_config = get_feed_config.get_feeds_from_xml(config_file) 
    # Parse the feeds and grave useful information to build a structure
    # which will be passed to the templates.
    data = []
    for feed_info in feeds_config:
        parser_instance_str = feed_info['parser'] + "(feed_info)"
        my_log.debug_print(parser_instance_str)
        parser = eval(parser_instance_str)
        feed_data = parser.parse()
        if len(feed_data['entries']) > 0:
            data.append(feed_data)
    
    if len(data) <= 0:
        my_log.write_to_log_file("<--Info-->: no new items for sending")
        return False
    ## Initialize some counters for the TOC IDs.
    ## We start counting at 2 because 1 is the TOC itself.
    feed_number = 1
    play_order = 1

    for feed in data:
        feed_number += 1
        play_order += 1
        feed['number'] = feed_number
        feed['play_order'] = play_order
        
        entry_number = 0
        for entry in feed['entries']:
            play_order += 1
            entry_number += 1
            entry['number'] = entry_number
            entry['play_order'] = play_order

    # Wrap data and today's date in a dict to use the magic of **.
    wrap = {
        'date': datetime.today().strftime("%Y-%m-%d-%H-%M"),
        'feeds': data,
    }
    
    my_log.debug_print( '='*10)
    my_log.debug_print( ' '*1 + 'date: ' + wrap['date'])
    my_log.debug_print( ' '*1 + 'feeds: ')
    for feed_data in wrap['feeds']:
        my_log.debug_print( ' '*3 + 'feed_title: ' + feed_data['title'])
        my_log.debug_print( ' '*3 + 'feed_num: %d' % (feed_data['number']))
        my_log.debug_print( ' '*3 + 'order: %d' % (feed_data['play_order']))
        my_log.debug_print( ' '*3 + 'entries: ' )
        for entry in feed_data['entries']:
            my_log.debug_print( ' '*5 + 'entry_title: ' + entry['title'])
            my_log.debug_print (' '*5 + 'entry_num: %d' % (entry['number']))
            my_log.debug_print (' '*5 + 'order: %d' % (entry['play_order']))



    # Render and output templates

    ## TOC (NCX)
    render_and_write('toc.xml', wrap, 'toc.ncx', output_dir)
    ## TOC (HTML)
    render_and_write('toc.html', wrap, 'toc.html', output_dir)
    ## OPF
    render_and_write('opf.xml', wrap, 'daily.opf', output_dir)
    ## Content
    for feed in data:
        render_and_write('feed.html', feed, '%s.html' % feed['number'], output_dir)

    # Copy the assets
    for name in listdir(path.join(ROOT, 'assets')):
        copy(path.join(ROOT, 'assets', name), path.join(output_dir, name))
    # copytree(path.join(ROOT, 'assets'), output_dir)
    return True

def render_and_write(template_name, context, output_name, output_dir):
    """Render `template_name` with `context` and write the result in the file
    `output_dir`/`output_name`."""

    template = templates_env.get_template(template_name)
    f = codecs.open(path.join(output_dir, output_name), "w", "utf-8")
    ##f = open(path.join(output_dir, output_name), "w")
    f.write(template.render(**context))
    f.close()


def mobi(input_file, exec_path):
    """Execute the KindleGen binary to create a MOBI file."""
    system("%s %s" % (exec_path, input_file))

if __name__ == "__main__":
    
    system("rm -rf temp/*")

    my_log.debug_print("Running RSSToKindle...")
    my_log.debug_print("-> Generating files...")
    medium_files_created = build('../config/config.xml', 'temp')

    if medium_files_created:
        my_log.debug_print("-> Build the MOBI file using KindleGen...")
        mobi('temp/daily.opf', '../kindlegen/kindlegen')
    my_log.debug_print("Done")


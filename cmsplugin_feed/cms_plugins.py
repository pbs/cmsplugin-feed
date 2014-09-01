import feedparser
from xml.sax import SAXException

from django.utils.translation import ugettext as _
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, InvalidPage

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from cmsplugin_feed.models import Feed
from cmsplugin_feed.forms import FeedForm
from cmsplugin_feed.settings import CMSPLUGIN_FEED_CACHE_TIMEOUT

import cmsplugin_feed.processors
from HTMLParser import HTMLParser
import BeautifulSoup


def get_cached_or_latest_feed(instance):
    """Get the feed from cache if it exists else fetch it."""
    feed_key = "feed_%s" % instance.id

    def cached_feed():
        return cache.get(feed_key)

    def updated_feed():
        valid_parsed_feed = fetch_parsed_feed(instance.feed_url)
        cache.set(feed_key, valid_parsed_feed, CMSPLUGIN_FEED_CACHE_TIMEOUT)
        return valid_parsed_feed
    return cached_feed() or updated_feed()


@cmsplugin_feed.processors.apply
def fetch_parsed_feed(feed_url):
    """Returns the parsed feed if not malformed,"""
    feed = feedparser.parse(feed_url)
    parse_error = hasattr(feed, 'bozo_exception') and (
        isinstance(feed.bozo_exception, SAXException))
    if not feed.bozo or not parse_error:
        return feed

def gimme_credit(summary):
    import pickle
    from BeautifulSoup import BeautifulSoup  
    from textblob import TextBlob
    from urlparse import urlparse                                                   
    from HTMLParser import HTMLParser                                               
    from itertools import chain  
    import re

    class MLStripper(HTMLParser):                                                   
        def __init__(self):                                                         
            self.reset()                                                            
            self.fed = []                                                           
                                                                                    
        def handle_data(self, d):                                                   
            self.fed.append(d)                                                      
                                                                                    
        def get_data(self):                                                         
            return ''.join(self.fed)                                                
                                                                                    
                                                                                    
    def strip_tags(html):                                                           
        s = MLStripper()                                                            
        s.feed(html.decode('ascii', 'ignore'))                                      
        return s.get_data()   

    def mini(x):                                                                    
        if not x:                                                                   
            return ""                                                               
        x = re.sub("\n+", " ", x)                                                   
        x = re.sub("\r+", " ", x)                                                   
        x = filter(lambda x: x not in "\n\t\r", x)                                  
        x = re.sub(" +", " ", x).strip()                                            
        return x                                                                    

    def minib(branch):                                                              
        ret = mini(strip_tags(str(branch)))                                         
        return ret                                                                  
            
    def valid_img_ext(path):                                                        
        return (path[-3:].lower() in ['jpg', 'bmp', 'gif', 'png'] or                
                path[-4:].lower() == "jpeg")                                        
                                                                                    
    def has_verb(stuff):                                                            
        blob = TextBlob(stuff)                                                      
        return len([a for a, b in blob.tags if b[:2] == "VB"]) >= 1  # improve  
        return "asd"

    def hotkey(stuff):                                                              
        crap = ["via ",                                                             
                "illustrated ", "photo ", "image credit:", "credit:", "image "]     
        for c in crap:                                                              
            pos = stuff.lower().find(c)                                             
            if pos != -1:                                                           
                stuff = stuff[pos:]                                                 
                break                                                               
        return stuff

    def propget(stuff):                                                             
        if has_verb(stuff):                                                         
            stuff = hotkey(stuff)                                                   
            if has_verb(stuff):                                                     
                return ""                                                           
        return stuff   

    tree = BeautifulSoup(summary)                                                        

    img = None                                                                      
    for x in tree.findAll('img'):                                                   
        if valid_img_ext(urlparse(x.get('src')).path):                              
            img = x                                                                 
        break                                                                       
    if img:                                                                         
        branch = img                                                                
        while (not (minib(branch)) and                                              
                   (branch.nextSibling or                                           
                    branch.parent)):                                                
            while not (minib(branch)) and branch.nextSibling:                       
                branch = branch.nextSibling                                         
            if not (minib(branch)) and branch.parent:                               
                branch = branch.parent                                              
        stuff = minib(branch)                                                       
        if stuff:                                                                   
            while minib(''.join(map(str, img.nextSiblingGenerator()))).find(stuff) == -1 and img.parent:
                img = img.parent                                                    
            pos = minib(''.join(map(str, img.nextSiblingGenerator()))).find(stuff)  
            if pos != 0:                                                            
                return ""                                                           
        if not stuff:                                                               
            return ""                                                               
        stuff = propget(stuff)                                                      
        stuff = stuff.lstrip(" ;")                                                  
        return stuff                                                                
    return ""   

class FeedPlugin(CMSPluginBase):
    model = Feed
    name = _('RSS Feed')
    form = FeedForm
    render_template = 'cmsplugin_feed/feed.html'

    def render(self, context, instance, placeholder):
        feed = get_cached_or_latest_feed(instance)
        if not feed:
            entries = []
            is_paginated = False
        else:
            if instance.paginate_by:
                is_paginated = True
                request = context['request']
                feed_page_param = "feed_%s_page" % str(instance.id)
                feed_paginator = Paginator(
                    feed['entries'], instance.paginate_by)
                # Make sure page request is an int. If not, deliver first page.
                try:
                    page = int(request.GET.get(feed_page_param, '1'))
                except ValueError:
                    page = 1
                # If page request (9999) is out of range, deliver last page of
                # results.
                try:
                    entries = feed_paginator.page(page)
                except (EmptyPage, InvalidPage):
                    entries = feed_paginator.page(feed_paginator.num_pages)
            else:
                entries = feed["entries"]
                is_paginated = False

        for e in entries:
            e['image'] = get_image(e['summary'])
            e['credit'] = gimme_credit(e['summary'])
            e['summary'] = strip_tags(e['summary'])
            

        context.update({
            'instance': instance,
            'feed_entries': entries,
            'is_paginated': is_paginated,
            'placeholder': placeholder,
        })
        return context


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def get_image(raw_html):
    tree = BeautifulSoup.BeautifulSoup(raw_html)
    img = tree.find('img')
    return img.get('src') if img else None

plugin_pool.register_plugin(FeedPlugin)

import json
import datetime
import PyRSS2Gen
import dateutil.parser
import requests

def to_datetime(date):
    """ Regularize long_parsed_date and return it as datetime.

    >>> to_datetime('Today, August 12th 9:55pm')
    datetime.datetime(2011, 8, 12, 21, 55)
    >>> to_datetime('Yesterday, August 12th 9:55pm')
    datetime.datetime(2011, 8, 12, 21, 55)
    >>> to_datetime(', December, 2nd 2010 12:01AM')
    datetime.datetime(2010, 12, 2, 0, 1)
    >>> to_datetime('Tuesday, November, 29, 2011 3:00AM')
    datetime.datetime(2011, 11, 29, 3, 0)
    """
    # remove problematic junk
    for day in ["Today", "Yesterday"]:
        date = date.replace(day, '')
    return dateutil.parser.parse(date)


base_url = "http://www.newsblur.com/"
auth_data = { "username": "johnnyuser", "password": "verynicePW123" }

s = requests.session()
# login to Newsblur
s.post(base_url + "api/login", data=auth_data)
# get starred items
b = s.get( base_url + "reader/starred_stories")
starred = json.loads(b.content)

# write rss
feed_items = []
if starred['authenticated'] == True and starred['result'] == 'ok':
    #make each item
    for story in starred['stories']:
        print story['story_title']
        item = PyRSS2Gen.RSSItem(
            title = story['story_title'],
            link = story['story_permalink'],
            description = story['story_content'],
            guid = PyRSS2Gen.Guid(story['story_permalink']),
            pubDate = to_datetime(story['long_parsed_date'])
        )
        feed_items.append(item)
    # then make the feed
    rss = PyRSS2Gen.RSS2(
        title = "My Great Shared Reader Items",
        link = "http://www.newsblur.com",
        description = "My Starred Items from NewsBlur",
        lastBuildDate = datetime.datetime.utcnow(),
        items = feed_items
        )
    # and write it
    rss.write_xml(open("feed.xml", "w"))

else:
    print starred['authenticated']
    print starred['result']

s.post(base_url + "api/logout")

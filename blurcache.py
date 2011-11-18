from newsblur import NewsBlur
import json
import PyRSS2Gen
import datetime

def today():
    dayoftheweek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    return dayoftheweek[datetime.date.weekday(datetime.date.today())]

def this_year():
    return str(datetime.date.today().year)

def to_datetime(long_parsed_date):
    date = long_parsed_date.replace('Today', today()).replace('th ', "th, {0} ".format(this_year()))
    date2 = date.replace('th', '')
    return datetime.datetime.strptime(date2, "%A, %B %d, %Y %I:%M%p")

# login to Newsblur
b = NewsBlur("user", "pa$$word")
b.login()

# get starred items
response = b.starred()
starred = json.loads(response)

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
        title = "Evan's Shared Reader Items",
        link = "http://www.newsblur.com",
        description = "Evan's Starred Items from NewsBlur",
        lastBuildDate = datetime.datetime.utcnow(),
        items = feed_items
        )
    # and write it
    rss.write_xml(open("feed.xml", "w"))

else:
    print starred['authenticated']
    print starred['result']

b.logout()

from newsblur import NewsBlur
import json
import PyRSS2Gen
import datetime

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
            #pubDate = story['shot_parsed_date'] #need to convert to datetime
            pubDate = datetime.datetime.utcnow()
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

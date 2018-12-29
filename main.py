import feedparser
import re
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

symbols = (u"абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
           u"abvgdeejzijklmnoprstufhzcss_y'euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y'EUA")
           
tr = {ord(a):ord(b) for a, b in zip(*symbols)}

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

NewsFeed = feedparser.parse("http://gorod.dp.ua/export/rss.php")

count = 0
db = myclient["rssFeeds"]
collection = db["gorodRss"]

while count < len(NewsFeed.entries):
  entry = NewsFeed.entries[count]
  doc = ({'name':entry.title.translate(tr),'desc': cleanhtml(entry.description).translate(tr)})
  db.collection.update_one(doc, {'$set':doc}, upsert=True)
  count += 1

for doc in db.collection.find({}):
   print(doc.get('name',None))
   print('  ' , doc.get('desc',None))

print(db.collection.count_documents({}))
#db.collection.remove()
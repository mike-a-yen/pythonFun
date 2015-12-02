import urllib
import json

#url = 'http://python-data.dr-chuck.net/comments_42.json'
url = 'http://python-data.dr-chuck.net/comments_187980.json'
html = urllib.urlopen(url).read()
table = json.loads(html)
comments = table['comments']
total = 0
for c in comments:
    total += c['count']
print total

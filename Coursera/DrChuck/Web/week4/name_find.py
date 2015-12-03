import urllib
from bs4 import *
import re

def GetName(url):
    name = re.findall('by_([a-zA-Z].*).html',url)
    return name[0]
position = 18
times = 7
position -= 1
#url = 'http://pr4e.dr-chuck.com/tsugi/mod/python-data/data/known_by_Fikret.html'
url = 'http://pr4e.dr-chuck.com/tsugi/mod/python-data/data/known_by_Ridwan.html'
html = urllib.urlopen(url).read()
soup = BeautifulSoup(html)

tags = soup('a')
print GetName(url)
for t in range(times):
    url = tags[position].get('href')
    print GetName(url)
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html)
    tags = soup('a')

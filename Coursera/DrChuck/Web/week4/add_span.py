import urllib
from bs4 import *

#url = 'http://pr4e.dr-chuck.com/tsugi/mod/python-data/data/comments_42.html'
url = 'http://pr4e.dr-chuck.com/tsugi/mod/python-data/data/comments_187979.html'
html = urllib.urlopen(url).read()

soup = BeautifulSoup(html)

tags = soup('span')
nums = [float(tag.contents[0]) for tag in tags]
print sum(nums)

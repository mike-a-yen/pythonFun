import urllib
import xml.etree.ElementTree as ET

#url = 'http://pr4e.dr-chuck.com/tsugi/mod/python-data/data/comments_42.xml'
url = 'http://pr4e.dr-chuck.com/tsugi/mod/python-data/data/comments_187976.xml'
xml = urllib.urlopen(url).read()
tree = ET.fromstring(xml)
count = tree.findall('.//count')
nums = [float(c.text) for c in count]
print sum(nums)

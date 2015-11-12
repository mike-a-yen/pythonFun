from bag import Bag

b = Bag(contents=['Yasaman',
                  'Guy',
                  'Ninh',
                  'Benjamin',
                  'Khadija',
                  'Adam',
                  'Yong',
                  'Ali',
                  'William',
                  'Jon',
                  'Daniel',
                  'Curtis',
                  'Jason',
                  'Mike',
                  'Chenkun'])

b.Shuffle()
for i in xrange(len(b.contents)):
    b.Draw()
    b.Shuffle()

print b.itemsDrawn
print '*'*60
print b.itemsDrawn[::-1]

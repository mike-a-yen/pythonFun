# test the sub pixel algoirthm:
# a small object whose size is
# less than one pixel will be
# shown on the image as one
# pixel. If a multiple images
# are taken at slightly different
# offsets (x,y) it is possible to
# resolve the small object to its
# actual size

import numpy as np

# creat a fake image 375x500 pixels in RGB
# values must be between zero and one
# 1.0 = white 0.0 = black
realImg = np.zeros((400,400,3))
realImg[200,200,:]= 1.0

# put pixArray on top of realImg and
# average real pix values over pixArray
# each pixArray entry is a 4x4 in realImg
def TakePicture(realImg,shiftX,shiftY):
    pixArray = np.zeros((100,100,3))
    for (x,y,z),value in np.ndenumerate(pixArray):
        xStart, yStart = int(4*x+4*shiftX), int(4*y+4*shiftY)
        xEnd, yEnd = int(xStart+4), int(yStart+4)

        if xEnd > realImg.shape[0] and yEnd > realImg.shape[1]:
            reals = realImg[ xStart:realImg.shape[0],yStart:realImg.shape[1],:]
        elif xEnd > realImg.shape[0]:
            reals = realImg[ xStart:realImg.shape[0], yStart:yEnd+1,:]
        elif yEnd > realImg.shape[1]:
            reals = realImg[ xStart:xEnd+1, yStart:realImg.shape[1],:]
        else:
            reals = realImg[ xStart:xEnd+1, yStart:yEnd+1,:]

        if np.sum(reals) > 0:
            pixArray[x,y,:] = np.sum(reals)/(4.*3.)
    return pixArray
    
pictures = []
for i in xrange(2):
    pictures.append(TakePicture(realImg,0.25*i,0))


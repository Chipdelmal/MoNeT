

# import cv2 library
import cv2
import sys
from glob import glob
import tGD_aux as aux


(USR, DRV, AOI) = ('dsk', 'tGD', 'HLT')
(PT_ROT, PT_IMG, PT_DTA, PT_PRE, PT_OUT, PT_MTR) = aux.selectPath(USR, DRV, exp)


# read the images
img1 = cv2.imread('sea.jpg')
img2 = cv2.imread('man.jpeg')


# vertically concatenates images
# of same width
im_v = cv2.vconcat([img1, img1])

# show the output image
cv2.imshow('sea_image.jpg', im_v)

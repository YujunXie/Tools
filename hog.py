from skimage.feature import hog
from skimage import io
import cv2 as cv

im = io.imread('Aaron.jpg', as_gray=True)
normalised_blocks, hog_image = hog(im ,orientations=9, pixels_per_cell=(8,8), cells_per_block=(8,8), block_norm = 'L2-Hys', visualize=True)
cv.imshow("image", hog_image)
cv.waitKey(0)

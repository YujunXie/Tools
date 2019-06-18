import cv2

def blur_quality(im, crop_size, threshold):
	""" compute the blur ratio of the image.

	Parameters
    ----------
	im: ndarray
		image read by cv2, matplotlib, skimage or just two-dimensional array
	crop_size: int
		size of sub-area of im for Laplacian edge detector
	threshold: float
		under this threshold, image can't be blur

	Returns
	-------
	blur_ratio: float

	"""
	h, w = im.shape
	img_list = []
    for i in range(0,int(h/crop_size)):
        for j in range(0,int(w/crop_size)):
            x1,y1,x2,y2 = (crop_size*j,crop_size*i,crop_size*(j+1),crop_size*(i+1))
            cropped_im = im[y1:y2, x1:x2]
            img_list.append(cropped_im)
    m = 0
    index = 0    
    for image in img_list:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        score = cv2.Laplacian(gray, cv2.CV_64F).var()
        if score >= threshold:
            m += 1
        index += 1
    blur_ratio  = float(m/index)
    return blur_rati

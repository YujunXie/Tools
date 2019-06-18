import numpy as np

def to_tlwh(bbox):
	"""
    Parameters
    ----------
	bbox: List(int)
		(top left x, top left y, bottom right x, bottom right y)

    Returns
    -------
	bbox: List(int)
		(top left x, top left y, width, height)

	"""
	bbox[2], bbox[3] = bbox[2]-bbox[0], bbox[3]-bbox[1]
	return bbox

def to_tlbr(bbox):
	"""
    Parameters
    ----------
	bbox: List(int)
		(top left x, top left y, width, height)

    Returns
    -------
	bbox: List(int)
		(top left x, top left y, bottom right x, bottom right y)

	"""
	bbox[2], bbox[3] = bbox[0]+bbox[2], bbox[1]+bbox[3]
	return bbox

def iou(bbox_1, bbox_2):
	""" compute the iou of two bounding boxes.

	Parameters
	----------
	bbox_1, bbox_2: List[int]
		represent two pair coordinates in the left corner and right corner like [x1, y1, x2, y2]
	
	Returns
	-------
	area: float

	"""
	x1 = max(bbox_1[0], bbox_2[0])
	y1 = max(bbox_1[1], bbox_2[1])
	x2 = min(bbox_1[2], bbox_2[2])
	y2 = min(bbox_1[3], bbox_2[3])
	inter = (x2 - x1 + 1) * (y2 - y1 + 1)

	area_1 = (bbox_1[1] - bbox_1[0] + 1) * (bbox_1[3] - bbox_1[2] + 1)
	area_2 = (bbox_2[1] - bbox_2[0] + 1) * (bbox_2[3] - bbox_2[2] + 1)
	union = area_1 + area_2 - inter

	return inter / union

def crop(im, bbox):
	""" crop the bbox area of the image.

	Parameters
    ----------
	im: ndarray
		image read by cv2, matplotlib, skimage or just two-dimensional array
	bbox: List[int]
		represent coordinates like [x1, y1, x2, y2], make sure x1 < x2, y1 < y2
	
	Returns
	-------
	im: ndarray

	"""
	h, w, c = im.shape
	x1, y1, x2, y2 = bbox
	
	x1 = max(0, x1)
	y1 = max(0, y1)
	x2 = min(w, x2)
	y2 = min(h, y2)

	return im[y1:y2, x1:x2]

import numpy as np

def nms(dets, threshold):
	""" non-maximun supress for detections
	
	Parameters
	----------
	dets: List[List[float]]
		two-dimentional list, each row contains one detection like [x1, x2, y1, y2, score]
	threshold: float
	
	Returns
	-------
	pick: List[int]
		indexes of remaining detections

	"""
	if len(dets) == 0:
		return []

	x1, y1, x2, y2 = dets[:, 0], dets[:, 1], dets[:, 2], dets[:, 3]
	scores = dets[:, 4]
	area = (x2 - x1 + 1) * (y2 - y1 + 1)
	idxs = np.argsort(scores)

	pick = []
	while len(idxs) > 0:

		last = len(idxs) - 1
		i = idxs[last]
		pick.append(i)

		xx1 = np.maximum(x1[i], x1[idxs[:last]])
        yy1 = np.maximum(y1[i], y1[idxs[:last]])
        xx2 = np.minimum(x2[i], x2[idxs[:last]])
        yy2 = np.minimum(y2[i], y2[idxs[:last]])

        iou = (xx2 - xx1 + 1) * (yy2 - yy1 + 1) / area[idxs[:last]]

        idxs = np.delete(
            idxs, np.concatenate(
            	([last], np.where(iou > threshold)[0])))

    return pick

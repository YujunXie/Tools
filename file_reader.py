import os

for root, dirs, files in os.walk('/Users/yujun/Desktop/mx/'):
	for d in dirs:
		dirpath = os.path.join(root, d)
		for root1, dirs1, files1 in os.walk(dirpath):
			for f in files1:
				oldname = os.path.join(dirpath, f)
				filepath = oldname.split('.', 1)
				newname=filepath[0]+'.jpg'
				os.rename(oldname, newname)
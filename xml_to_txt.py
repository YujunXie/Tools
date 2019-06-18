import os
import sys
import xml.etree.ElementTree as ET

def xml_to_txt(indir,outdir):
	''' transfer the content in xml file to data form in txt file 
	params:
		indir: path to xml file
		outdir: path to txt file
	'''
    annotations = os.listdir(indir)
    dets = []

    for i, file in enumerate(annotations):

        frame = file.split('.')[0]
        in_file = open(os.path.join(indir, file))
        tree = ET.parse(in_file)
        root = tree.getroot()

        for obj in root.iter('object'):
            current = list()

            xmlbox = obj.find('bndbox')
            x1 = xmlbox.find('xmin').text
            x2 = xmlbox.find('xmax').text
            y1 = xmlbox.find('ymin').text
            y2 = xmlbox.find('ymax').text
            w = int(x2) - int(x1)
            h = int(y2) - int(y1)

            det = [int(frame), -1, float(x1), float(y1), float(w), float(h), 1.0, -1, -1, -1]
            dets.append(det)

    dets = sorted(dets, key=(lambda x:x[0]))
    file_txt = os.path.join(outdir,'det.txt')
    f_w = open(file_txt,'w')

    for det in dets:
        for d in det[0:9]:
            f_w.write(str(d) + ',')
        f_w.write(str(det[9]))
        f_w.write('\n')

    f_w.close()

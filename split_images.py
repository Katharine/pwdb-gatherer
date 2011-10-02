#!/usr/bin/env python
from PIL import Image
import sys

def get_filename_list(inp):
	return [("%s.png" % x.decode('gbk').encode('utf8').strip()[:-4]) for x in open(inp)][4:]

def get_dimensions(inp):
	return [int(x) for x in [x.decode('gbk').encode('utf8').strip() for x in open(inp)][:4]]

def create_images(collage, filenames):
	dimensions = get_dimensions(filenames)
	filenames = get_filename_list(filenames)
	h = dimensions[0]
	w = dimensions[1]
	y = dimensions[2]
	x = dimensions[3]
	tiles = Image.open(collage)
	for i in xrange(y):
		for j in xrange(x):
			index = i*x + j
			if index >= len(filenames):
				break
			section = tiles.crop((w*j, h*i, w*(j+1), h*(i+1)))
			section.save(filenames[index])

def main(argv):
	if len(argv) < 3:
		print "Usage: split_images.py <collage.png> <filenames.txt>"
	else:
		create_images(argv[1], argv[2])

if __name__ == '__main__':
	main(sys.argv)

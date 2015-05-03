import sys, os
import cv2
import numpy as np
import tile as T
import base as B
import similarity as S
from PIL import Image

"""
1. open target image
2. 30 x 30 images now
3. new = souce width x cell width
4. resize new width
5. for every cell width calculate histogram
6. find most similar cell
7. place cell in new pic
8. next
"""

def entitle(impath, path, format):
    start = len(path)+1
    end = len(format)*-1
    title = impath[start:end]
    return title

def main():
	# Check if user has provided a base image and tile library
    if len(sys.argv) < 2:
        sys.exit("Usage: python main.py base-image-path tile-directory-path\n \
        		  Example: python main.py nyan.png 151")

    # Parse command line args
    base_path = sys.argv[1]
    format = sys.argv[1][-4:]
    tile_path = sys.argv[2]
    if len(sys.argv) is 4:
    	format = sys.argv[3]

	# Read tile library images first
    if os.path.exists(base_path) and os.path.exists(tile_path):
        imfilelist=[os.path.join(tile_path,f) for f in os.listdir(tile_path) if f.endswith(format)]
        if len(imfilelist) < 1: # number of tile images
            sys.exit ("Need to specify a path containing " + format + " files")
        tiles = {} # init dictionary of tile objects
        for impath in imfilelist:
            print(impath)
            imtitle = entitle(impath, tile_path, format)
            tile = T.Tile(impath, imtitle)
            tiles[imtitle] = tile
    else:
        sys.exit("The path name does not exist")

    # Next, generate base image
    base = B.Base(base_path, 300)

    # TODO: improve poor efficiency of this algorithm
    # Find best tiles to compose base image
    the_chosen = []
    history = {} # store histogram-best tile matches
    for row in base.histograms:
        the_row = []
        for histogram in row:
	        closest = 100.0
	        if str(histogram) in history:
	        	closest_tile = history[str(histogram)]
	        	# This constant-time lookup saves a lot of calculations
	        	# print "Reused tile from history"
	        else:
		        for key in tiles:
		            tile = tiles[key]
		            distance = S.l1_color_norm(histogram, tile.histogram)
		            # Why are so many 0.5?
		            if (distance < closest):
		                closest = distance
		                closest_tile = tile
		        # print closest_tile
		        history[str(histogram)] = closest_tile
	        the_row.append(closest_tile.title)
        print the_row
        the_chosen.append(the_row)

    # Generate mosaic
    size = 30, 30
    mosaic = Image.new('RGBA', (base.cols*30, base.rows*30))
    rowcount = 0
    #print "row: " + str(rowcount)
    for row in xrange(base.rows):
	colcount = 0
	#print "column: " + str(colcount)
	for col in xrange(base.cols):
	    idx = the_chosen[row][col]
       	    #img = tiles[idx].image
	    #print str(sys.argv[2]) + "/" + str(tiles[idx].title) + str(sys.argv[3])
	    path = os.path.abspath(str(sys.argv[2]) + "/" + str(tiles[idx].title) + str(sys.argv[3]))
	    img = Image.open(path)
	    #premultiply(img)
            img = img.resize((30, 30), Image.ANTIALIAS)
	    #unmultiply(img)
	    mosaic.paste(img, (30*colcount, 30*rowcount))
	    colcount += 1
	rowcount += 1
    mosaic.save("mosaic.png")

    # print "Okay we're done for now"
    # print the_chosen

if __name__ == "__main__": main()

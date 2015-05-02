import sys, os
import cv2
import numpy as np
import tile as T
import base as B
import similarity as S

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
    base = B.Base(base_path)

    # Find best tiles to compose base image
    the_chosen = []
    for row in base.histograms:
        the_row = []
        for histogram in row:
	        closest = 100.0
	        for key in tiles:
	            tile = tiles[key]
	            distance = S.l1_color_norm(histogram, tile.histogram)
	            # Why are so many 0.5?
	            if (distance < closest):
	                closest = distance
	                closest_tile = tile
	        # print closest_tile
	        the_row.append(closest_tile.title)
        print the_row
        the_chosen.append(the_row)
    # the_chosen = [['133', '133', '133', '133', '133', '133', '133', '133', '133', '133', '133', '133', '133', '133', '133', '97', '97', '97', '97', '97', '97', '97', '97', '97', '97', '133', '133', '133', '133'], ['133', '133', '133', '133', '133', '133', '133', '133', '133', '133', '133', '133', '133', '133', '58', '59', '59', '59', '59', '59', '59', '59', '59', '59', '59', '59', '10', '133', '133'], ['133', '133', '133', '133', '133', '133', '133', '133', '133', '133', '133', '133', '133', '133', '59', '59', '58', '133', '133', '53', '53', '53', '133', '85', '59', '59', '97', '133', '133'], ['133', '133', '133', '133', '133', '133', '133', '133', '133', '133', '133', '133', '133', '133', '59', '59', '53', '133', '133', '133', '133', '150-mega-y', '150-mega-y', '150-mega-y', '113', '59', '97', '118', '50'], ['133', '133', '133', '133', '133', '133', '133', '133', '133', '133', '133', '133', '133', '133', '59', '59', '133', '133', '133', '133', '133', '95', '95', '95', '113', '59', '95', '95', '95'], ['133', '133', '133', '133', '133', '133', '133', '133', '133', '133', '133', '133', '133', '133', '59', '59', '53', '53', '133', '133', '133', '95', '95', '95', '95', '95', '95', '95', '95'], ['133', '133', '133', '133', '133', '133', '133', '133', '133', '133', '133', '97', '97', '97', '59', '59', '53', '53', '133', '53', '150-mega-x', '95', '95', '95', '95', '95', '87', '95', '95'], ['133', '133', '133', '133', '133', '133', '133', '133', '133', '133', '104', '95', '95', '95', '59', '59', '53', '53', '53', '133', '150-mega-x', '95', '95', '95', '95', '95', '95', '95', '95'], ['133', '133', '133', '133', '150-mega-x', '150-mega-x', '150-mega-x', '150-mega-x', '150-mega-x', '150-mega-x', '104', '95', '95', '100', '59', '59', '133', '53', '53', '133', '150-mega-x', '95', '95', '95', '95', '95', '95', '95', '35'], ['133', '133', '133', '133', '133', '133', '133', '133', '133', '133', '133', '133', '133', '133', '59', '59', '59', '59', '59', '59', '59', '59', '95', '95', '95', '95', '95', '95', '112'], ['133', '133', '133', '133', '133', '133', '133', '133', '133', '133', '133', '133', '133', '133', '95', '95', '97', '95', '95', '97', '97', '97', '97', '95', '95', '97', '95', '142', '133'], ['133', '133', '133', '133', '133', '133', '133', '133', '133', '133', '133', '133', '133', '133', '97', '97', '133', '97', '97', '133', '133', '133', '133', '97', '97', '133', '97', '97', '133']]

    # Generate mosaic
    for row in xrange(base.rows):
        for col in xrange(base.cols):
            idx = the_chosen[row][col]
            img = tiles[idx].image
            if col is 0:
                imgs = img
            else:
	        	imgs = np.concatenate((imgs, img), axis=1)
        if row is 0:
            mosaic = imgs
        else:
            mosaic = np.concatenate((mosaic, imgs), axis=0)
    cv2.imwrite("mosaic.png", mosaic)
    cv2.imshow("Mosaic", mosaic)

    # print "Okay we're done for now"
    # print the_chosen

if __name__ == "__main__": main()
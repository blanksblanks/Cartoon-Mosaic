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
    tile_path = sys.argv[2]
    format = ".png"

	# Read tile library images first
    if os.path.exists(tile_path):
        imfilelist=[os.path.join(tile_path,f) for f in os.listdir(tile_path) if f.endswith(format)]
        if len(imfilelist) < 1: # number of tile images
            sys.exit ("Need to specify a path containing .ppm files")
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
    for histogram in base.histograms:
        closest = 1.0
        for key in tiles:
            tile = tiles[key]
            distance = S.l1_color_norm(histogram, tiles[key].histogram)
            if (distance < closest):
                closest = distance
                closest_tile = tile
        the_chosen.append(closest_tile.title)

    print "Okay we're done for now"
    print the_chosen


if __name__ == "__main__": main()
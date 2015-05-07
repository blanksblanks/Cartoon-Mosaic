from __future__ import division
import sys, os
import random
import cv2
import numpy as np
import tile as T
import base as B
import similarity as S
from PIL import Image

TILE_WIDTH = 30
ALPHA = 0.0

def entitle(impath, path, format):
    start = len(path)+1
    end = len(format)*-1
    title = impath[start:end]
    return title

def main():
    # Check if user has provided a base image and tile library
    if len(sys.argv) < 2:
        sys.exit("Usage: python main.py base-image-path tile-directory-path tile-format\n \
                  Example: python main.py nyan.png 151 .png")

    # Parse command line args
    base_path = sys.argv[1]
    format = sys.argv[1][-4:]
    tile_path = sys.argv[2]

    if len(sys.argv) is 4:
        format = sys.argv[3]

    # Read tile library images first
    print "Analyzing tile library images..."
    if os.path.exists(base_path) and os.path.exists(tile_path):
        imfilelist=[os.path.join(tile_path,f) for f in os.listdir(tile_path) if f.endswith(format)]
        if len(imfilelist) < 1: # number of tile images
            sys.exit ("Need to specify a path containing " + format + " files")
        tiles = {} # init dictionary of tile objects
        dominants = {} # init dictionary of list of tiles by dominant color
        num_images = len(imfilelist)
        if num_images > 500:
            num_images = 500 # only look up first 500 images
        for i in xrange(num_images):
            impath = imfilelist[i]
            # print(impath)
            if ( (i+1)%50 == 0 or i == num_images-1 ):
                print i+1, "out of", num_images, "images"
            imtitle = entitle(impath, tile_path, format)
            tile = T.Tile(impath, imtitle)
            tiles[imtitle] = tile
            """for color in tile.dominants:
                if color in dominants:
                    dominants[color].append(tile)
                else:
                    dominants[color] = [tile]"""
    else:
        sys.exit("The path name does not exist")

    print ""
    # Next, generate base image
    print "Analyzing base image..."
    base = B.Base(base_path)

    # TODO: improve poor efficiency of this algorithm
    # Find best tiles to compose base image
    print ""
    print "Generating mosaic..."
    the_chosen = []
    history = {} # store histogram-best tile matches
    count = base.rows * base.cols
    dom_count = 0
    history_count = 0
    expensive_count = 0

    for i in xrange(base.rows):
        hist_row = base.histograms[i]
        grayscales = base.grayscales[i]
        #dom_row = base.dominants[i]
        the_row = []
        for j in xrange(base.cols):
            skip = False
            histogram = hist_row[j]
            graygram = grayscales[j]
            """for dom in dom_row[j]:
                if dom in dominants:
                    closest_tile = random.choice(dominants[dom])
                    skip = True
                    dom_count += 1
                    break"""
            if (skip == False):
                closest = 100
                if str(histogram) in history:
                    closest_tile = history[str(histogram)]
                    # This constant-time lookup saves a lot of calculations
                    history_count += 1
                else:
                    for key in tiles:
                        tile = tiles[key]
                        dcolor = S.l1_color_norm(histogram, tile.histogram)
                        dgray = S.l1_gray_norm(graygram, tile.gray)
                        distance = ALPHA*dcolor + (1-ALPHA)*dgray
                        # Why are so many 0.5?
                        if (distance < closest):
                            closest = distance
                            closest_tile = tile
                    # print closest_tile
                    history[str(histogram)] = closest_tile
                    expensive_count += 1
            the_row.append(closest_tile.title)
        the_chosen.append(the_row)
        # print the_row
        print "%d out of %d rows" %(len(the_chosen), base.rows)

    # Generate mosaic
    size = TILE_WIDTH, TILE_WIDTH
    print ALPHA
    if ALPHA == 0:#grayscale mosaic
        print "GRAY"
        mosaic = Image.new('L', (base.cols*TILE_WIDTH, base.rows*TILE_WIDTH))
    else:
        print "COLOR"
        mosaic = Image.new('RGBA', (base.cols*TILE_WIDTH, base.rows*TILE_WIDTH))
    rowcount = 0
    #print "row: " + str(rowcount)
    for row in xrange(base.rows):
        colcount = 0
    #print "column: " + str(colcount)
        for col in xrange(base.cols):
            idx = the_chosen[row][col]
            tile = tiles[idx]
            img = tile.display
            mosaic.paste(img, (TILE_WIDTH*colcount, TILE_WIDTH*rowcount))
            colcount += 1
        rowcount += 1
    mosaic.save("mosaic.png")

    f = open('mosaic_keys.txt', 'w')
    f.write(str(the_chosen))

    print ""
    print "Expensive operations:", expensive_count, "of", count, ":", expensive_count/count
    print "Dominant operations:", dom_count, "of", count, ":", dom_count/count
    print "History operations:", history_count, "of", count, ":", history_count/count

if __name__ == "__main__": main()

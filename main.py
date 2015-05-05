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
        for impath in imfilelist:
            print(impath)
            imtitle = entitle(impath, tile_path, format)
            tile = T.Tile(impath, imtitle)
            tiles[imtitle] = tile
            for color in tile.dominants:
                if color in dominants:
                    dominants[color].append(tile)
                else:
                    dominants[color] = [tile]
    else:
        sys.exit("The path name does not exist")

    # Next, generate base image
    print "Analyzing base image..."
    base = B.Base(base_path)

    # TODO: improve poor efficiency of this algorithm
    # Find best tiles to compose base image
    print "Matching tile images with base image quadrants..."
    the_chosen = []
    history = {} # store histogram-best tile matches
    count = base.rows * base.cols
    dom_count = 0
    history_count = 0
    expensive_count = 0

    for i in xrange(base.rows):
        hist_row = base.histograms[i]
        dom_row = base.dominants[i]
        the_row = []
        for j in xrange(base.cols):
            skip = False
            histogram = hist_row[j]
            for dom in dom_row[j]:
                if dom in dominants:
                    closest_tile = random.choice(dominants[dom])
                    skip = True
                    dom_count += 1
                    break
            if (skip == False):
                closest = 100.0
                if str(histogram) in history:
                    closest_tile = history[str(histogram)]
                    # This constant-time lookup saves a lot of calculations
                    # print "Reused tile from history"
                    history_count += 1
                else:
                    for key in tiles:
                        tile = tiles[key]
                        distance = S.l1_color_norm(histogram, tile.histogram)
                        # Why are so many 0.5?
                        if (distance < closest):
                            closest = distance
                            closest_tile = tile
                    # print closest_tile
                    expensive_count += 1
                    history[str(histogram)] = closest_tile
            the_row.append(closest_tile.title)
        the_chosen.append(the_row)
        # print the_row
        print "Row %d of %d" %(len(the_chosen), base.rows)

    # the_chosen = [['i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23'], ['i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23'], ['i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i39', 'i39', 'i39', 'i39', 'i39', 'i39', 'i39', 'i39', 'i39', 'i39', 'i39', 'i39', 'i39', 'i39', 'i39', 'i39', 'i39', 'i39', 'i39', 'kiss', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23'], ['i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i02', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i02', 'i02', 'i02', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23'], ['i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'autumn', 'autumn', 'autumn', 'autumn', 'autumn', 'autumn', 'autumn', 'autumn', 'autumn', 'autumn', 'autumn', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'tree', 'pinktree', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'pinktree', 'pinktree', 'purple', 'pinktree', 'pinktree', 'purple', 'purple', 'purple', 'pinktree', 'tree', 'i23', 'i23', 'i02', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23'], ['autumn', 'autumn', 'autumn', 'autumn', 'autumn', 'autumn', 'autumn', 'autumn', 'autumn', 'autumn', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'autumn', 'autumn', 'autumn', 'autumn', 'autumn', 'autumn', 'autumn', 'autumn', 'autumn', 'autumn', 'i23', 'tree', 'purple', 'pinktree', 'pinktree', 'purple', 'purple', 'purple', 'purple', 'purple', 'pinktree', 'pinktree', 'purple', 'pinktree', 'pinktree', 'purple', 'purple', 'purple', 'purple', 'purple', 'i23', 'i23', 'i02', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23'], ['kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'i23', 'purple', 'purple', 'pinktree', 'pinktree', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'pinktree', 'pinktree', 'purple', 'purple', 'i23', 'i02', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23'], ['kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'i23', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'lilies', 'lady', 'lilies', 'pinktree', 'pinktree', 'purple', 'purple', 'i23', 'i02', 'i23', 'i23', 'lady', 'lady', 'lady', 'i23', 'i23'], ['i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'kiss', 'i23', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'pinktree', 'pinktree', 'pinktree', 'purple', 'purple', 'shattered', 'lady', 'gray', 'gray', 'lady', 'purple', 'purple', 'purple', 'i23', 'i02', 'i23', 'lady', 'gray', 'gray', 'lady', 'i23', 'i23'], ['i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i23', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'pinktree', 'magenta', 'pinktree', 'purple', 'purple', 'shattered', 'lady', 'gray', 'gray', 'lady', 'i23', 'purple', 'purple', 'i23', 'i02', 'i23', 'gray', 'gray', 'gray', 'lady', 'i23', 'i23'], ['i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i23', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'pinktree', 'pinktree', 'purple', 'purple', 'shattered', 'lady', 'gray', 'gray', 'gray', 'gray', 'i23', 'i02', 'i02', 'i02', 'gray', 'gray', 'gray', 'gray', 'lady', 'i23', 'i23'], ['i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i23', 'purple', 'purple', 'purple', 'pinktree', 'pinktree', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'shattered', 'lady', 'gray', 'gray', 'gray', 'gray', 'gray', 'gray', 'gray', 'gray', 'gray', 'gray', 'gray', 'gray', 'lady', 'i23', 'i23'], ['i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i01', 'i23', 'purple', 'purple', 'purple', 'pinktree', 'pinktree', 'purple', 'purple', 'purple', 'purple', 'pinktree', 'pinktree', 'lilies', 'lilies', 'gray', 'gray', 'gray', 'gray', 'gray', 'gray', 'gray', 'gray', 'gray', 'gray', 'gray', 'gray', 'gray', 'gray', 'lady', 'i23'], ['i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i01', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'purple', 'pinktree', 'pinktree', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'pinktree', 'pinktree', 'i23', 'lady', 'gray', 'gray', 'gray', 'hudson', 'hudson', 'gray', 'gray', 'gray', 'gray', 'gray', 'lady', 'hudson', 'hudson', 'gray', 'lady', 'i23'], ['i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i32', 'i32', 'armchair', 'lady', 'lady', 'lady', 'lady', 'lady', 'lady', 'i23', 'purple', 'pinktree', 'pinktree', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'i23', 'lady', 'gray', 'gray', 'hudson', 'i01', 'lady', 'gray', 'gray', 'gray', 'lady', 'gray', 'lady', 'i01', 'lady', 'gray', 'lady', 'i23'], ['i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i32', 'lady', 'gray', 'gray', 'gray', 'gray', 'lady', 'lady', 'lady', 'i23', 'purple', 'purple', 'purple', 'purple', 'purple', 'pinktree', 'pinktree', 'purple', 'purple', 'purple', 'purple', 'i23', 'lady', 'pinktree', 'lady', 'lady', 'lady', 'lady', 'gray', 'gray', 'gray', 'lady', 'gray', 'lady', 'lady', 'lady', 'lady', 'lady', 'i23'], ['i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'starry', 'lady', 'lady', 'lady', 'lady', 'lady', 'lady', 'i23', 'starry', 'i23', 'purple', 'purple', 'pinktree', 'pinktree', 'purple', 'pinktree', 'pinktree', 'purple', 'purple', 'purple', 'purple', 'i23', 'lady', 'lady', 'i09', 'lady', 'gray', 'gray', 'gray', 'venus', 'lady', 'gray', 'gray', 'gray', 'gray', 'lady', 'i09', 'i06', 'i23'], ['i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i23', 'starry', 'starry', 'starry', 'starry', 'starry', 'starry', 'starry', 'kiss', 'i23', 'tree', 'purple', 'pinktree', 'pinktree', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'lady', 'lady', 'lady', 'lady', 'lady', 'lady', 'lady', 'lady', 'i23', 'lady', 'lady', 'lady', 'gray', 'lady', 'lady', 'i07', 'i23'], ['i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i23', 'i02', 'i23', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'i39', 'venus', 'gray', 'gray', 'gray', 'lady', 'lady', 'lady', 'lady', 'lady', 'lady', 'lady', 'gray', 'gray', 'lady', 'i23', 'i23'], ['i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'lady', 'venus', 'i02', 'i02', 'i02', 'i02', 'i02', 'i02', 'i02', 'i02', 'i02', 'i02', 'i02', 'i02', 'i39', 'lady', 'gray', 'gray', 'gray', 'gray', 'gray', 'gray', 'gray', 'gray', 'gray', 'gray', 'lady', 'i23', 'i23', 'i23'], ['i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'gray', 'lady', 'lady', 'i23', 'i23', 'lady', 'lady', 'lady', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'lady', 'lady', 'lady', 'i23', 'i23', 'i23', 'lady', 'lady', 'lady', 'i23', 'i23', 'i23', 'i23'], ['i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'gray', 'gray', 'lady', 'i23', 'i23', 'lady', 'gray', 'gray', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'lady', 'gray', 'gray', 'i23', 'i23', 'i23', 'gray', 'gray', 'lady', 'i23', 'i23', 'i23', 'i23'], ['i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23'], ['i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23']]

    # Generate mosaic
    size = TILE_WIDTH, TILE_WIDTH
    mosaic = Image.new('RGBA', (base.cols*TILE_WIDTH, base.rows*TILE_WIDTH))
    rowcount = 0
    #print "row: " + str(rowcount)
    for row in xrange(base.rows):
        colcount = 0
    #print "column: " + str(colcount)
        for col in xrange(base.cols):
            idx = the_chosen[row][col]
            # Reopen image in PIL format
            tile = tiles[idx]
            img = tile.display
            # path = os.path.abspath(str(sys.argv[2]) + "/" + str(tiles[idx].title) + str(sys.argv[3]))
            # img = Image.open(path)
            # img = crop_square(img, size)
            # img = img.resize(size, Image.ANTIALIAS)
            # Optional:
            # img = fill(img, tiles[idx].title)
            mosaic.paste(img, (TILE_WIDTH*colcount, TILE_WIDTH*rowcount))
            colcount += 1
        rowcount += 1
    mosaic.save("mosaic.png")

    print "Okay we're done for now"
    print the_chosen
    print "Expensive operations:", expensive_count, "of", count, ":", expensive_count/count
    print "Dominant operations:", dom_count, "of", count, ":", dom_count/count
    print "History operations:", history_count, "of", count, ":", history_count/count


if __name__ == "__main__": main()

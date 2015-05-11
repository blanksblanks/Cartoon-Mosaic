from __future__ import division
try:
   import cPickle as pickle
except:
   import pickle
import sys
import os
import random
from PIL import Image
import cv2
import numpy as np
import tile as T
import base as B
import similarity as S

# Toggle between 1.0 and 0.0 for linear sum ratio of best match
# 1.0 is all color, 0.0 is pure grayscale
ALPHA = 1
DOM_ON = 0

def entitle(impath, path, format):
    start = len(path)+1
    end = len(format)*-1
    title = impath[start:end]
    return title

def main():
    # Check if user has provided a base image and tile library
    if len(sys.argv) < 2:
        sys.exit("Usage: python main.py base-image-path tile-directory-path tile-format\n \
                  Note: base-image-path should not end in / \n \
                  Example: python main.py Low.jpg _db/justinablakeney .png")

    # Parse command line args
    base_path = sys.argv[1]
    tile_path = sys.argv[2]
    format = sys.argv[3]

    # Pickle path names
    base_ppath = base_path[:-4]+".p"
    tile_ppath = tile_path+".p"
    dom_ppath = tile_path+"_dom.p"
    # Warning: if experimenting with changing constants other than ALPHA, better
    # to delete these pickle files and try again
    # Saving history doesn't make sense as alpha values often shift
    # history_ppath = tile_path+"-"+os.path.basename(base_path)[:-4]+".p"

    # Read tile library images first
    print "Analyzing tile library images..."

    # Check if pickle file exists
    if os.path.exists(tile_ppath) and os.path.exists(dom_ppath):
        base_pickle = open(tile_ppath, "rb")
        tiles = pickle.load( base_pickle )
        base_pickle.close()
        dom_pickle = open(dom_ppath, "rb")
        dominants = pickle.load( dom_pickle)
        dom_pickle.close()
        print "Reloaded pickled file."
    else:
        if os.path.exists(tile_path):
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
                # Optional: use dominant colors method
                if (DOM_ON):
                    for color in tile.dominants:
                        if color in dominants:
                            dominants[color].append(tile)
                        else:
                            dominants[color] = [tile]
            # Save tiles in pickle file for future use
            pickle.dump( tiles, open( tile_ppath, "wb" ) )
            pickle.dump( dominants, open( dom_ppath, "wb" ) )
        else:
            sys.exit(tile_path + " does not exist")

    # Next, analyze base image
    print ""
    print "Analyzing base image..."
    # Check if pickle file exists first
    if os.path.exists(base_ppath):
        base_pickle = open(base_ppath, "rb")
        base = pickle.load( base_pickle )
        base_pickle.close()
        print "Reloaded pickled file."
    elif os.path.exists(base_path):
        base = B.Base(base_path)
        pickle.dump( base, open( base_ppath, "wb" ) )
    else:
            sys.exit(base_path + " does not exist")

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
        if (DOM_ON):
            dom_row = base.dominants[i]
        the_row = []
        for j in xrange(base.cols):
            skip = False
            histogram = hist_row[j]
            graygram = grayscales[j]
            # Optional: use dominant colors method
            if (DOM_ON and ALPHA == 1):
                for dom in dom_row[j]:
                    if dom in dominants:
                        closest_tile = random.choice(dominants[dom])
                        skip = True
                        dom_count += 1
                        break
            if (skip == False):
                closest = 100
                if str(histogram) in history:
                    closest_tile = history[str(histogram)]
                    # This constant-time lookup saves a lot of calculations
                    history_count += 1
                else:
                    for key in tiles:
                        tile = tiles[key]
                        if ALPHA == 1: # All color
                            distance = S.l1_color_norm(histogram, tile.histogram)
                        elif ALPHA == 0: # All grayscale
                            distance = S.l1_gray_norm(graygram, tile.gray)
                        else: # Linear sum of ratio between the two
                            dcolor = S.l1_color_norm(histogram, tile.histogram)
                            dgray = S.l1_gray_norm(graygram, tile.gray)
                            distance = ALPHA*dcolor + (1-ALPHA)*dgray
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
    print ""
    size = tile.display.size # any tile will have the same size
    if ALPHA == 0: #grayscale mosaic
        print "Your GRAYSCALE MOSAIC will be done soon."
        mosaic = Image.new('L', (base.cols*size[0], base.rows*size[1]))
    else:
        print "Your COLOR MOSAIC will be done soon."
        mosaic = Image.new('RGBA', (base.cols*size[0], base.rows*size[1]))
    rowcount = 0
    # print "row: " + str(rowcount)
    for row in xrange(base.rows):
        colcount = 0
    # print "column: " + str(colcount)
        for col in xrange(base.cols):
            idx = the_chosen[row][col]
            tile = tiles[idx]
            img = tile.display
            mosaic.paste(img, (colcount*size[0], rowcount*size[1]))
            colcount += 1
        rowcount += 1
    mosaic.save(base_path[:-4]+"-Mosaic"+str(ALPHA)+".png")

    print "Successfully saved to "+base_path[:-4]+"-Mosaic"+str(ALPHA)+".png"

    f = open('mosaic_keys.txt', 'w')
    f.write(str(the_chosen))

    # Calculate percentage of database used and print stats
    print ""
    n = len(set([img for sublist in the_chosen for img in sublist]))
    print "Percent of possible tiles used: %.3f, %d out %d images from tile library used" %(round((float(n)/len(tiles)), 3), n, len(tiles))
    print ""
    print "Expensive operations:", expensive_count, "of", count, ":", expensive_count/count
    print "Dominant operations:", dom_count, "of", count, ":", dom_count/count
    print "History operations:", history_count, "of", count, ":", history_count/count

if __name__ == "__main__": main()




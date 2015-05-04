from __future__ import division

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

TILE_WIDTH = 30

#fill background of image with dominant image color
def fill(img, title):
    img = img.convert("RGBA")
    print "title: " + str(title)
    poll = img.getcolors() #most frequently used colors
    print "poll: " + str(poll)
    max = 0
    dom = None
    for i in range(len(poll)):
        colors = poll[i]
        print "compare: " + str(colors)
        if colors[1][3] != 255: #transparent
            continue
        if colors[1][0] == 49 and colors[1][1] == 49 and colors[1][2] == 49:
            continue
        if colors[0] > max:
            max = colors[0]
            dom = colors[1]
    color = dom #dominant color
    print "color: " + str(color)
    pixels = img.load()
    fill = Image.new('RGB', (15, 15))
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            r, g, b, a = pixels[x, y]
        if a != 255: #transparent
            r = color[0]
            g = color[1]
            b = color[2]
            pixels[x,y] = (r,g,b,a)
            fill.putpixel((x, y), pixels[x,y])
    fill.save(str(title) + "-rgb.png") #save the image
    folder = os.path.dirname(os.path.realpath(__file__)) #now load it back in
    files = os.listdir(folder)
    for stuff in files:
        if not os.path.isdir(stuff):
            if stuff == str(title)+"-rgb.png":
                path = str(title)+"-rgb.png"
                img = Image.open(path)
                return img

def flat( *nums ):
    return tuple( int(round(n)) for n in nums )

def crop_square(img, size):
    original = img.size
    target = size
    # Calculate aspect ratios
    original_aspect = original[0] / original[1]
    target_aspect = target[0] / target[1]

    # Image is too tall: take some off the top and bottom
    if target_aspect > original_aspect:
        scale_factor = target[0] / original[0]
        crop_size = (original[0], target[1] / scale_factor)
        top_cut_line = (original[1] - crop_size[1]) / 2
        img = img.crop( flat(0, top_cut_line, crop_size[0], top_cut_line + crop_size[1]) )
    # Image is too wide: take some off the sides
    elif target_aspect < original_aspect:
        scale_factor = target[1] / original[1]
        crop_size = (target[0]/scale_factor, original[1])
        side_cut_line = (original[0] - crop_size[0]) / 2
        img = img.crop( flat(side_cut_line, 0,  side_cut_line + crop_size[0], crop_size[1]) )

    return img.resize(size, Image.ANTIALIAS)

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
    base = B.Base(base_path, 100)

    """
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
        the_chosen.append(the_row)
        # print the_row
        print "Row %d of %d" %(len(the_chosen), base.rows)
    """

    the_chosen = [['i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23'], ['i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23'], ['i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i39', 'i39', 'i39', 'i39', 'i39', 'i39', 'i39', 'i39', 'i39', 'i39', 'i39', 'i39', 'i39', 'i39', 'i39', 'i39', 'i39', 'i39', 'i39', 'kiss', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23'], ['i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i02', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i02', 'i02', 'i02', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23'], ['i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'autumn', 'autumn', 'autumn', 'autumn', 'autumn', 'autumn', 'autumn', 'autumn', 'autumn', 'autumn', 'autumn', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'tree', 'pinktree', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'pinktree', 'pinktree', 'purple', 'pinktree', 'pinktree', 'purple', 'purple', 'purple', 'pinktree', 'tree', 'i23', 'i23', 'i02', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23'], ['autumn', 'autumn', 'autumn', 'autumn', 'autumn', 'autumn', 'autumn', 'autumn', 'autumn', 'autumn', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'autumn', 'autumn', 'autumn', 'autumn', 'autumn', 'autumn', 'autumn', 'autumn', 'autumn', 'autumn', 'i23', 'tree', 'purple', 'pinktree', 'pinktree', 'purple', 'purple', 'purple', 'purple', 'purple', 'pinktree', 'pinktree', 'purple', 'pinktree', 'pinktree', 'purple', 'purple', 'purple', 'purple', 'purple', 'i23', 'i23', 'i02', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23'], ['kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'i23', 'purple', 'purple', 'pinktree', 'pinktree', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'pinktree', 'pinktree', 'purple', 'purple', 'i23', 'i02', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23'], ['kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'kiss', 'i23', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'lilies', 'lady', 'lilies', 'pinktree', 'pinktree', 'purple', 'purple', 'i23', 'i02', 'i23', 'i23', 'lady', 'lady', 'lady', 'i23', 'i23'], ['i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'kiss', 'i23', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'pinktree', 'pinktree', 'pinktree', 'purple', 'purple', 'shattered', 'lady', 'gray', 'gray', 'lady', 'purple', 'purple', 'purple', 'i23', 'i02', 'i23', 'lady', 'gray', 'gray', 'lady', 'i23', 'i23'], ['i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i23', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'pinktree', 'magenta', 'pinktree', 'purple', 'purple', 'shattered', 'lady', 'gray', 'gray', 'lady', 'i23', 'purple', 'purple', 'i23', 'i02', 'i23', 'gray', 'gray', 'gray', 'lady', 'i23', 'i23'], ['i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i23', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'pinktree', 'pinktree', 'purple', 'purple', 'shattered', 'lady', 'gray', 'gray', 'gray', 'gray', 'i23', 'i02', 'i02', 'i02', 'gray', 'gray', 'gray', 'gray', 'lady', 'i23', 'i23'], ['i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i23', 'purple', 'purple', 'purple', 'pinktree', 'pinktree', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'shattered', 'lady', 'gray', 'gray', 'gray', 'gray', 'gray', 'gray', 'gray', 'gray', 'gray', 'gray', 'gray', 'gray', 'lady', 'i23', 'i23'], ['i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i26', 'i01', 'i23', 'purple', 'purple', 'purple', 'pinktree', 'pinktree', 'purple', 'purple', 'purple', 'purple', 'pinktree', 'pinktree', 'lilies', 'lilies', 'gray', 'gray', 'gray', 'gray', 'gray', 'gray', 'gray', 'gray', 'gray', 'gray', 'gray', 'gray', 'gray', 'gray', 'lady', 'i23'], ['i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i01', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'purple', 'pinktree', 'pinktree', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'pinktree', 'pinktree', 'i23', 'lady', 'gray', 'gray', 'gray', 'hudson', 'hudson', 'gray', 'gray', 'gray', 'gray', 'gray', 'lady', 'hudson', 'hudson', 'gray', 'lady', 'i23'], ['i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i32', 'i32', 'armchair', 'lady', 'lady', 'lady', 'lady', 'lady', 'lady', 'i23', 'purple', 'pinktree', 'pinktree', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'i23', 'lady', 'gray', 'gray', 'hudson', 'i01', 'lady', 'gray', 'gray', 'gray', 'lady', 'gray', 'lady', 'i01', 'lady', 'gray', 'lady', 'i23'], ['i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i32', 'lady', 'gray', 'gray', 'gray', 'gray', 'lady', 'lady', 'lady', 'i23', 'purple', 'purple', 'purple', 'purple', 'purple', 'pinktree', 'pinktree', 'purple', 'purple', 'purple', 'purple', 'i23', 'lady', 'pinktree', 'lady', 'lady', 'lady', 'lady', 'gray', 'gray', 'gray', 'lady', 'gray', 'lady', 'lady', 'lady', 'lady', 'lady', 'i23'], ['i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'starry', 'lady', 'lady', 'lady', 'lady', 'lady', 'lady', 'i23', 'starry', 'i23', 'purple', 'purple', 'pinktree', 'pinktree', 'purple', 'pinktree', 'pinktree', 'purple', 'purple', 'purple', 'purple', 'i23', 'lady', 'lady', 'i09', 'lady', 'gray', 'gray', 'gray', 'venus', 'lady', 'gray', 'gray', 'gray', 'gray', 'lady', 'i09', 'i06', 'i23'], ['i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i23', 'starry', 'starry', 'starry', 'starry', 'starry', 'starry', 'starry', 'kiss', 'i23', 'tree', 'purple', 'pinktree', 'pinktree', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'lady', 'lady', 'lady', 'lady', 'lady', 'lady', 'lady', 'lady', 'i23', 'lady', 'lady', 'lady', 'gray', 'lady', 'lady', 'i07', 'i23'], ['i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i23', 'i02', 'i23', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'i39', 'venus', 'gray', 'gray', 'gray', 'lady', 'lady', 'lady', 'lady', 'lady', 'lady', 'lady', 'gray', 'gray', 'lady', 'i23', 'i23'], ['i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'lady', 'venus', 'i02', 'i02', 'i02', 'i02', 'i02', 'i02', 'i02', 'i02', 'i02', 'i02', 'i02', 'i02', 'i39', 'lady', 'gray', 'gray', 'gray', 'gray', 'gray', 'gray', 'gray', 'gray', 'gray', 'gray', 'lady', 'i23', 'i23', 'i23'], ['i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'gray', 'lady', 'lady', 'i23', 'i23', 'lady', 'lady', 'lady', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'lady', 'lady', 'lady', 'i23', 'i23', 'i23', 'lady', 'lady', 'lady', 'i23', 'i23', 'i23', 'i23'], ['i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'i31', 'gray', 'gray', 'lady', 'i23', 'i23', 'lady', 'gray', 'gray', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'lady', 'gray', 'gray', 'i23', 'i23', 'i23', 'gray', 'gray', 'lady', 'i23', 'i23', 'i23', 'i23'], ['i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23'], ['i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23', 'i23']]

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
            path = os.path.abspath(str(sys.argv[2]) + "/" + str(tiles[idx].title) + str(sys.argv[3]))
            img = Image.open(path)
            img = crop_square(img, size)
            img = img.resize(size, Image.ANTIALIAS)
            # Optional:
            # img = fill(img, tiles[idx].title)
            mosaic.paste(img, (TILE_WIDTH*colcount, TILE_WIDTH*rowcount))
            colcount += 1
        rowcount += 1
    mosaic.save("mosaic.png")

    print "Okay we're done for now"
    print the_chosen

if __name__ == "__main__": main()

import cv2
import numpy as np
import reduction as R
import tile
import base

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

def main:
	# Check if user has provided a base image and tile library
    if len(sys.argv) < 2:
        sys.exit("Usage: python main.py base-image-path tile-directory-path")

    base_path = sys.argv[1]
    tile_path = sys.argv[2]
    format = ".png"

    base_image = cv2.imread(base_path, cv2.IMREAD_UNCHANGED)
    # TODO: change this hard coded value
    R.resize_by_p(base_image, 3000)
    for :
    	section = crop(image, )
    def crop(image, start_y, end_y, start_x, end_x):
	image = image[start_y:end_y, start_x:end_x]
	return image


	# Parse tile library images first
    if os.path.exists(tile_path):
        imfilelist=[os.path.join(tile_path,f) for f in os.listdir(tile_path) if f.endswith(format)]
        if len(imfilelist) < 1:
            sys.exit ("Need to specify a path containing .ppm files")
        NUM_IM = len(imfilelist) # default is 40
        print "Number of images:", NUM_IM
        for im in imfilelist:
            print(el)
            # Update images and titles list
            image = cv2.imread(el, cv2.IMREAD_UNCHANGED)
            start = len(path)+1
            end = len(format)*-1
            title = el[start:end]
            # Generate color histogram
            # Returned image has its transparent pixels converted to 255,255,255
            image, chist = color_histogram(image, title)
            chist_images.append(plot)
            # chist = color_histogram(image, title)
            chists.append(chist)
            images.append(image)
            titles.append(title)
    else:
        sys.exit("The path name does not exist")


if __name__ == "__main__": main()
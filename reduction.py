import cv2, os, sys, time
import numpy as np

# ============================================================
# Data Reduction
# ============================================================

# resize image to w pixels wide
def resize_by_w(image, new_w):
    r = new_w / float(image.shape[1]) # calculate aspect ratio
    dim = (new_w, int(image.shape[0] * r))
    print r, dim
    image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    return image

# resize image by percentage
def resize_by_p(image, percent):
	w, h = get_dimensions(image)
	desired_w = (percent/100) * w
	image = resize_by_w(image, desired_w)
	return image

# crop image
def crop(image, start_y, end_y, start_x, end_x):
	image = image[start_y:end_y, start_x:end_x]
	return image

def crop_square(image):
	w, h = get_dimensions(image)
	if (w > h):
		offset = (w - h) / 2
		image = crop(image, 0, h, offset, w-offset)
	elif (h > w):
		offset = (h - w) / 2
		image = crop(image, offset, h-offset, 0, w)
	# else it is already square
	image = cv2.resize(image, (15, 15))
	return image

# 270: rotate image 90 degrees counterclockwise
def rotate(image, degrees):
    (h, w) = image.shape[:2]
    center = (w / 2, h / 2) # find center
    M = cv2.getRotationMatrix2D(center, degrees, 1.0)
    image = cv2.warpAffine(image, M, (w, h))
    return image

# convert color image to grayscale
def grayscale(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image

# convert grayscale image to color (to permit color drawing)
def colorize(image):
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    return image

# invert image colors
def invert(image):
    image = (255-image)
    return image

# find otsu's threshold value with median blurring to make image black and white
def binarize(image):
    blur = cv2.medianBlur(image, 5)
    # better for spotty noise than cv2.GaussianBlur(image,(5,5),0)
    ret,thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    image = thresh
    return image

# apply morphological closing to close holes - removed from main as it closes gaps
def close(image):
    kernel = np.ones((5,5), np.uint8)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    return image

# canny edge detection: performs gaussian filter, intensity gradient, non-max
# suppression, hysteresis thresholding all at once
def edge_finder(image):
    image = cv2.Canny(image,100,200) # params: min, max vals
    return image

# Replace all pixels with empty tiles
def blank(image):
    w,h = get_dimensions(image)
    for i in xrange(h):
        for j in xrange(w):
            image[i][j] = [255, 255, 255, 0]
    save(image, './0.png')

# ============================================================
# Helper Functions
# ============================================================

def save(image, name):
    cv2.imwrite(name, image)

# 0 means forever
def show(image, millisec):
    cv2.waitKey(millisec)
    cv2.imshow('Image', image)

# return width, height
def get_dimensions(image):
	return len(image[0]), len(image)

# ============================================================
# Main Method
# ============================================================

def main():
    if len(sys.argv) < 2:
        sys.exit("Need to specify a path from which to read images")

    imageformat=".png"
    path = "./" + sys.argv[1]

    make_blank = True

    # load image sequence
    if os.path.exists(path):
        imfilelist=[os.path.join(path,f) for f in os.listdir(path) if f.endswith(imageformat)]
        if len(imfilelist) < 1:
        	sys.exit ("Need to specify a path containing .png files")
        for el in imfilelist:
            sys.stdout.write(el)
            image = cv2.imread(el, cv2.IMREAD_UNCHANGED) # load original
            # if make_blank is True:
            #     blank(image)
            #     make_blank = False
            # test square crop
            image = resize_by_w(image, 200)
            image = crop_square(image)
            show(image, 1000)
            save(image, el[:-4]+"_square"+".png")
    else:
        sys.exit("The path name does not exist")

    time.sleep(5)

if __name__ == "__main__": main()

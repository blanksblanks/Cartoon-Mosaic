import cv2, os, sys, time
import numpy as np

# ============================================================
# Data Reduction
# ============================================================

# resize image to w pixels wide
def resize(image, new_w):
    r = new_w / image.shape[1] # calculate aspect ratio
    dim = (new_w, int(image.shape[0] * r))
    image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    return image

# crop image
def crop(image, start_y, end_y, start_x, end_x):
	image = image[start_y:end_y, start_x:end_x]
	return image

def crop_square(image, new_w):
	image = resize(image, new_w)
	new_w, new_h = get_dimensions(image)
	if (new_w > new_h):
		offset = (new_w - new_h) / 2
		image = crop(image, 0, new_h, offset, new_w-offset)
	elif (new_h > new_w):
		offset = (new_h - new_w) / 2
		image = crop(image, offset, new_h-offset, 0, new_w)
	# else it is already square
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

    combination = []

    # load image sequence
    if os.path.exists(path):
        imfilelist=[os.path.join(path,f) for f in os.listdir(path) if f.endswith(imageformat)]
        if len(imfilelist) < 1:
        	sys.exit ("Need to specify a path containing .png files")
        for el in imfilelist:
            sys.stdout.write(el)
            image = cv2.imread(el, cv2.IMREAD_UNCHANGED) # load original
            image = crop_square(image, 800)
            show(image, 1000)
            save(image, el[:-4]+'_resized.png')
    else:
        sys.exit("The path name does not exist")

    time.sleep(5)

if __name__ == "__main__": main()

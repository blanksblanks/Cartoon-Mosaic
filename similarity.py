import os
import sys
import cv2
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
from matplotlib import gridspec as gridspec
from sklearn.cluster import KMeans
import operator

# ============================================================
# Constants
# ============================================================

COL_RANGE = 256
BINS = 4
BIN_SIZE = int(COL_RANGE/BINS)
gBINS = BINS*BINS # need more bins for grayscale since there's only one axis
gBIN_SIZE = int(COL_RANGE/gBINS)
DOM_COL_THRESH = 0.3

# ============================================================
# Analysis
# ============================================================

def grayscale_histogram(image, title):
    '''
    Calculate the grayscale / luminescence histogram of an image
    by counting the number of grayscale values in a set number of
    bins
    '''
    grayscale = []
    h = len(image)
    w = len(image[0])
    hist = np.zeros(shape=(gBINS))
    for i in xrange(h):
        for j in xrange(w):
            pixel = image[i, j]
            gray = operator.add(int(pixel[0]), int(pixel[1]))
            gray = operator.add(gray, int(pixel[2]))
            gray = gray/3
            g_bin = gray/gBIN_SIZE
            hist[g_bin] += 1
    return hist

def color_histogram(image, title):
    '''
    Calculate the 3D color histogram of an image by counting the number
    of RGB values in a set number of bins
    image -- pre-loaded image using cv2.imread function
    title -- image title
    '''
    colors = []
    h = len(image)
    w = len(image[0])
    # Create a 3D array - if BINS is 8, there are 8^3 = 512 total bins
    hist = np.zeros(shape=(BINS, BINS, BINS))
    # Traverse each pixel in the image matrix and increment the appropriate
    # hist[r_bin][g_bin][b_bin] - we know which one by floor dividing the
    # original RGB values / BIN_SIZE
    for i in xrange(h):
        for j in xrange(w):
            pixel = image[i][j]
            # Handling different image formats
            try: # If transparent (alpha channel = 0), change to white pixel
                if pixel[3] == 0:
                    pixel[0] = 255
                    pixel[1] = 255
                    pixel[2] = 255
            except (IndexError):
                pass # do nothing if alpha channel is missing
            # Note: pixel[i] is descending since OpenCV loads BGR
            r_bin = pixel[2] / BIN_SIZE
            g_bin = pixel[1] / BIN_SIZE
            b_bin = pixel[0] / BIN_SIZE
            hist[r_bin][g_bin][b_bin] += 1
            # Generate list of color keys for visualization
            if (r_bin,g_bin,b_bin) not in colors:
                colors.append( (r_bin,g_bin,b_bin) )
    # Sort colors from highest count to lowest counts
    colors = sorted(colors, key=lambda c: -hist[(c[0])][(c[1])][(c[2])])
    # Return image in case transparent values were changed
    return hist, image, colors

def l1_color_norm(h1, h2):
    diff = 0
    total = 0
    for r in xrange(0, BINS):
        for g in xrange(0, BINS):
            for b in range(0, BINS):
                diff += abs(h1[r][g][b] - h2[r][g][b])
                total += h1[r][g][b] + h2[r][g][b]
    l1_norm = diff / 2.0 / total
    similarity = 1 - l1_norm
    # print 'diff, sum and distance:', diff, sum, distance
    return l1_norm

def l1_gray_norm(h1, h2):
    diff = 0
    total = 0
    #print h1
    #print h2
    for g in xrange(0, gBINS):
        diff += abs(h1[g]-h2[g])
        total += h1[g]+h2[g]
    l1_norm = diff/2.0/total
    return l1_norm

def dominant_colors(hist, colors):
    """Helper method to determine percentages of color pixels in a picture"""
    num_pixels = 0
    dominant_colors = []
    for (r,g,b) in colors:
        num_pixels += hist[r][g][b]
    for (r,g,b) in colors:
        # Ignore black and white pixels
        if (r,g,b) != (0,0,0) and (r,g,b) != (BINS-1,BINS-1,BINS-1):
            p = round( (float(hist[r][g][b]) / num_pixels), 3)
            # print p,
            if p > DOM_COL_THRESH:
                dominant_colors.append( (r,g,b) )
            else:
                # print 'Dominant colors:', dominant_colors
                return dominant_colors # don't care about the rest
    return dominant_colors # in case

def kmeans_dominance(image):
    # reshape the image to be a list of pixels
    image = image.reshape((image.shape[0] * image.shape[1], 3))
    # cluster the pixel intensities
    clt = KMeans(n_clusters = 3)
    clt.fit(image)
    # grab the number of different clusters and create a histogram
    # based on the number of pixels assigned to each cluster
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins = numLabels)

    # normalize the histogram, such that it sums to one
    hist = hist.astype("float")
    hist /= hist.sum()
    centroids = clt.cluster_centers_
    colors = []
    for (percent, color) in zip(hist, centroids):
        # print percent
        # print color.astype("uint8").tolist()
        color = color.astype("uint8").tolist()
        color = [c/BIN_SIZE for c in color]
        # print color
        colors.append(tuple(color))
    # print colors
    return colors

# ============================================================
# Visualization
# ============================================================

def hexencode(rgb, factor):
    """Convert RGB tuple to hexadecimal color code."""
    r = rgb[0]*factor
    g = rgb[1]*factor
    b = rgb[2]*factor
    return '#%02x%02x%02x' % (r,g,b)

def plot_histogram(hist, title, colors=None, image=None):
    """
    Visualize histograms as bar graphs where each bar is color-coded
    and sorted by greatest count to least count
    """
    # If information not given, deduce list of colors
    if (colors == None):
        colors = []
        for r in xrange(BINS):
            for g in xrange(BINS):
                for b in xrange(BINS):
                    colors.append( (r,g,b) )
        colors = sorted(colors, key=lambda c: -hist[(c[0])][(c[1])][(c[2])])
        # Remove bins from sorted list of colors if their count is 0 in the histogram
        for i in xrange(len(colors)):
            c = colors[i]
            if hist[(c[0])][(c[1])][(c[2])] == 0:
                colors = colors[:i]
                break
    # Generate bar graph
    plt.rcParams['font.family']='Aller Light'
    for idx, c in enumerate(colors):
        r, g, b = c
        # print c, ':', hist[r][g][b], ';',
        plt.subplot(1,2,1).bar(idx, hist[r][g][b], color=hexencode(c, BIN_SIZE), edgecolor=hexencode(c, BIN_SIZE))
        plt.xticks([])
        # Optional, append image on the right
        if image != None:
            plt.subplot(1,2,2),plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            plt.xticks([]),plt.yticks([])
    # Save plot
    dir_name = './color_hist/'
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    path = dir_name+title+'.png'
    plt.savefig(path, bbox_inches='tight')
    plt.clf()
    plt.close('all')
    print path
    return path

# ============================================================
# Intra-set Analysis
# ============================================================

def calc_cdistance(chists):
    """
    Find distance between every image pair in the set by calculating
    L1 norm
    """
    chist_dis = {}
    for i in xrange(NUM_IM):
        for j in xrange(i, NUM_IM):
            if (i,j) not in chist_dis:
                d = l1_color_norm(chists[i], chists[j])
                chist_dis[(i,j)] = d
    # print chist_dis
    return chist_dis

def color_matches(k, chist_dis):
    """
    Find images most like and unlike an image based on color distribution.
    k -- the original image for comparison
    chists -- the list of color histograms for analysis
    """
    results = {}
    indices = []
    distances = []

    for i in xrange(0, NUM_IM):
        if k > i: # because tuples always begin with lower index
            results[i] = chist_dis[(i,k)]
        else:
            results[i] = chist_dis[(k,i)]
    # Ordered list of tuples (dist, idx) from most to least similar
    # -- first value will be the original image with diff of 0
    results = sorted([(v, k) for (k, v) in results.items()])
    # print 'results for image', k, results
    seven = results[:4]
    seven.extend(results[-3:])
    # print 'last seven for image', k, seven
    distances, indices = zip(*seven)
    # print 'distances:',distances
    # print 'indices:',indices
    return indices, distances

def find_four(chist_dis):
    results = {}
    # ensure that a<b, b<c and c<d as order does not matter
    for a in xrange(NUM_IM):
        for b in xrange(a+1,NUM_IM):
            for c in xrange(b+1,NUM_IM):
                for d in xrange(c+1,NUM_IM):
                    results[(a,b,c,d)] = \
                    chist_dis[(a,b)] + chist_dis[(a,c)] + \
                    chist_dis[(a,d)] + chist_dis[(b,c)] + \
                    chist_dis[(b,d)] + chist_dis[(c,d)]
    results = sorted([(v, k) for (k, v) in results.items()])
    best = results[0]
    worst = results[-1]
    indices = list(best[1])
    indices.extend(list(worst[1]))
    # print "results: ", len(results), #results
    # print "best, worst", best, worst
    return indices

# ============================================================
# Intra-Set Visualization
# ============================================================

def septuple_stitch_h(images, titles, dir_name, cresults, cdistances, cvt):
    plt.rcParams['font.family']='Aller Light'
    gs1 = gridspec.GridSpec(1,7)
    gs1.update(wspace=0.05, hspace=0.05) # set the spacing between axes.
    for k in xrange(0, NUM_IM*7, 7):
        for i in xrange(7):
            idx = cresults[k+i]
            ax = plt.subplot(gs1[i])
            plt.axis('on')
            if cvt is 0:
                plt.imshow(images[idx], cmap="Greys_r")
            elif cvt is -1:
                plt.imshow(images[idx], cmap="binary")
            else:
                plt.imshow(cv2.cvtColor(images[idx], cv2.COLOR_BGR2RGB)) # row, col
            plt.xticks([]),plt.yticks([])
            if cdistances:
                if i == 0:
                    plt.xlabel('similarity:')
                else:
                    sim = 1 - round(cdistances[k+i], 5)
                    plt.xlabel(sim)
                plt.title(titles[idx], size=12)
            ax.set_aspect('equal')

        title = titles[k/7]
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        title = dir_name+title+'.png'
        plt.savefig(title, bbox_inches='tight')
        print title
        plt.clf()
        plt.close('all')

def four_stitch_h(images, titles, cresults, dir_name):
    plt.rcParams['font.family']='Aller Light'
    gs1 = gridspec.GridSpec(1,4)
    gs1.update(wspace=0.05, hspace=0.05) # set the spacing between axes.
    for k in xrange(0,8,4):
        for i in xrange(4):
            idx = cresults[i+k]
            ax = plt.subplot(gs1[i])
            plt.axis('on')
            plt.imshow(cv2.cvtColor(images[idx], cv2.COLOR_BGR2RGB)) # row, col
            plt.xticks([]),plt.yticks([])
            plt.title(titles[idx], size=12)
            ax.set_aspect('equal')
        if k is 0:
            title = 'best_match.png'
        else:
            title = 'worst_match.png'
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        plt.savefig(dir_name+title, bbox_inches='tight')
        print title
        plt.clf()
        plt.close('all')

# ============================================================
# Testing
# ============================================================

def main():

    # Check if user has provided a directory argument
    if len(sys.argv) < 2:
        sys.exit("Need to specify a path from which to read images")

    format = ".png"
    if (sys.argv[1] == "./"):
        path = sys.argv[1]
    else:
        path = "./" + sys.argv[1]

    global NUM_IM
    images = []
    titles = []
    chists = []
    chist_images = []
    cresults = []
    cdistances = []

    # Process images from user-provided directory
    if os.path.exists(path):
        imfilelist=[os.path.join(path,f) for f in os.listdir(path) if f.endswith(format)]
        if len(imfilelist) < 1:
            sys.exit ("Need to specify a path containing .ppm files")
        NUM_IM = len(imfilelist) # default is 40
        print "Number of images:", NUM_IM
        for el in imfilelist:
            print(el)
            # Update images and titles list
            image = cv2.imread(el, cv2.IMREAD_UNCHANGED)
            start = len(path)+1
            end = len(format)*-1
            title = el[start:end]
            # Generate color histogram
            chist, image, plot = color_histogram(image, title)
            print chist
            chist_images.append(plot)
            # chist = color_histogram(image, title)
            chists.append(chist)
            images.append(image)
            titles.append(title)
    else:
        sys.exit("The path name does not exist")

    # Calculate lookup table for distances based on color histograms
    chist_dis = calc_cdistance(chists)

    # Determine 3 closest and 3 farthest matches for all images
    for k in xrange(NUM_IM):
        # By color
        results, distances = color_matches(k, chist_dis)
        cresults.extend(results)
        cdistances.extend(distances)

    # Visualize septuples of best and worst matches by image and histogram visualizations
    septuple_stitch_h(images, titles, './color_sim/', cresults, cdistances, 1)
    septuple_stitch_h(chist_images, titles, './color_hist_sim/', cresults, None, 1)

    # Find set of 4 most different and 4 most similar images
    # cfour = find_four(chist_dis)


    # Display four best and four worst, by color and by texture
    # four_stitch_h(images, titles, cfour, path)

if __name__ == "__main__": main()

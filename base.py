import cv2
import reduction as R
import similarity as S

TILE_WIDTH = 30
TILE_COLS = 50

class Base():
	def __init__(self, path):
		self.path = path
		self.image = cv2.imread(path, cv2.IMREAD_UNCHANGED)
		# Will actually discount second value
		self.image = R.resize_by_w(self.image, TILE_WIDTH*TILE_COLS)
		self.height = len(self.image)
		self.width = len(self.image[0])
		self.histograms = []
		self.dominants = []
		# Equivalent to for(int j=0; j<self.height-TILE_WIDTH; j+=TILE_WIDTH)
		# Advantage of this way is if self.width%TILE_WIDTH != 0
		for j in xrange(0, self.height, TILE_WIDTH):
			hist_row = []
			dom_row = []
			for i in xrange(0, self.width, TILE_WIDTH):
				start_y = j
				end_y = j + TILE_WIDTH
				start_x = i
				end_x = i + TILE_WIDTH
				quadrant = R.crop(self.image, start_y, end_y, start_x, end_x)
				title = "base" + str(end_x) + "-" + str(end_y)
				histogram, quadrant, colors = S.color_histogram(quadrant, title)
				# Optional, save histogram as bar graph and return saved path
				# plot_path = S.plot_histogram(histogram, title, colors)
				dominants = S.dominant_colors(histogram, colors)
				# dominants = S.kmeans_dominance(self.image)
				hist_row.append(histogram)
				dom_row.append(dominants)
			self.histograms.append(hist_row)
			self.dominants.append(dom_row)
			print "Row %d of %d" %((j/TILE_WIDTH)+1, self.height/TILE_WIDTH)

		self.rows = len(self.histograms)
		self.cols = len(self.histograms[0])
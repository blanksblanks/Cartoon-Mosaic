import cv2
import reduction as R
import similarity as S

TILE_WIDTH = 15

class Base():
	def __init__(self, path,percent=0):
		self.path = path
		self.image = cv2.imread(path, cv2.IMREAD_UNCHANGED)
		if percent != 0:
			self.image = R.resize_by_p(self.image, percent)
		self.height = len(self.image)
		self.width = len(self.image[0])
	# 	self.histograms = find_quadrants(self) # list of quadrant histograms

	# def find_quadrants(self):
		self.histograms = []
		# Equivalent to for(int j=0; j<self.height-TILE_WIDTH; j+=TILE_WIDTH)
		# Advantage of this way is if self.width%TILE_WIDTH != 0
		for j in xrange(0, self.height-TILE_WIDTH, TILE_WIDTH):
			row = []
			for i in xrange(0, self.width-TILE_WIDTH, TILE_WIDTH):
				start_y = j
				end_y = j + TILE_WIDTH
				start_x = i
				end_x = i + TILE_WIDTH
				quadrant = R.crop(self.image, start_y, end_y, start_x, end_x)
				title = "base" + str(end_x) + "-" + str(end_y)
				histogram, quadrant = S.color_histogram(quadrant, title)
				# Optional, save histogram as bar graph and return saved path
				plot_path = S.plot_histogram(histogram, title)
				row.append(histogram)
			self.histograms.append(row)

		self.rows = len(self.histograms)
		self.cols = len(self.histograms[0])
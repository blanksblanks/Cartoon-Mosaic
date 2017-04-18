import cv2
from PIL import Image
from dominance import colorz

import reduction as R
import similarity as S

TILE_WIDTH = 30
DISPLAY_WIDTH = 50

class Tile():
	def __init__(self, path, title):
		"""Open in Numpy array for histogram analysis"""
		self.path = path
		self.title = title
		size = (TILE_WIDTH, TILE_WIDTH)
		self.image = cv2.imread(path, cv2.IMREAD_UNCHANGED)
		self.image = R.crop_square(self.image, size)
		self.height = len(self.image)
		self.width = len(self.image[0])
		self.histogram, self.image, self.colors = S.color_histogram(self.image, self.title)
		self.gray = S.grayscale_histogram(self.image, self.title)

		"""Open with PIL format for display purposes"""
		self.display = Image.open(path)
		self.display = R.resize_square(self.display, (DISPLAY_WIDTH, DISPLAY_WIDTH) )
		# Crop image to square (simply set size for last param if you want 30x30 tiles)
		# (width, height) = self.display.size
		# if (width < height):
		# 	self.display = R.resize_square(self.display, (width, width) )
		# elif (height < width):
		# 	self.display = R.resize_square(self.display, (height, height) )
		# self.display = R.fill(self.display, self.title)

		"""Additional options (extra runtime)"""
		# Optional: generate bar chart to visualize histogram
		# plot_path = S.plot_histogram(self.histogram, self.title, self.colors)

		# Optional: find dominant colors
		# print 'Title: ', title,
		self.dominants = S.dominant_colors(self.histogram, self.colors)
		# self.dominants = S.kmeans_dominance(self.image)
		# self.dominants = colorz(self.image)
		# print self.dominants

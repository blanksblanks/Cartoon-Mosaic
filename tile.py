import cv2
import reduction as R
import similarity as S

TILE_WIDTH = 30

class Tile():
	def __init__(self, path, title):
		self.path = path
		self.title = title
		self.image = cv2.imread(path, cv2.IMREAD_UNCHANGED)
		# So that tile image is 30 x 30
		# if len(self.image[0]) != TILE_WIDTH:
		# 	self.image = R.resize_by_w(self.image, TILE_WIDTH)
		self.image = R.crop_square(self.image)
		self.height = len(self.image)
		self.width = len(self.image[0])
		self.histogram, self.image, self.colors = S.color_histogram(self.image, self.title)
		plot_path = S.plot_histogram(self.histogram, self.title, self.colors)
		self.dominants = S.dominant_colors(self.histogram, self.colors)
		print self.dominants
		self.uses = 0
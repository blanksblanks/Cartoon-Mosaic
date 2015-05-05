import cv2
import reduction as R
import similarity as S
from PIL import Image

TILE_WIDTH = 30

class Tile():
	def __init__(self, path, title):
		self.path = path
		self.title = title
		size = (TILE_WIDTH, TILE_WIDTH)
		self.display = Image.open(path) # PIL format for display
		self.display = R.resize_square(self.display, size)
		# Optional:
		# self.display = R.fill(self.display, self.title)
		self.image = cv2.imread(path, cv2.IMREAD_UNCHANGED)
		self.image = R.crop_square(self.image, size)
		self.height = len(self.image)
		self.width = len(self.image[0])
		self.histogram, self.image, self.colors = S.color_histogram(self.image, self.title)
		plot_path = S.plot_histogram(self.histogram, self.title, self.colors)
		self.dominants = S.dominant_colors(self.histogram, self.colors)
		print self.dominants
		self.uses = 0
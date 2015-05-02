import cv2
import reduction as R
import similarity as S

class Tile():
	def __init__(self, path, title):
		self.path = path
		self.title = title
		self.image = cv2.imread(path, cv2.IMREAD_UNCHANGED)
		# So that tile image is 30 x 30
		self.image = R.crop_square(self.image)
		self.height = len(self.image)
		self.width = len(self.image[0])
		# Image is returned as well because its transparent pixels are adjusted
		self.histogram, self.image = S.color_histogram(self.image, self.title)
		self.uses = 0
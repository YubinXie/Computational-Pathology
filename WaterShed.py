import numpy as np
from skimage import data
from skimage.morphology import watershed
from scipy import ndimage as ndi
coins = data.coins()
#histo = np.histogram(coins, bins=np.arange(0, 256))
markers = np.zeros_like(coins)
markers[coins < 30] = 1
markers[coins > 150] = 2
from skimage.filters import sobel
elevation_map = sobel(coins)
segmentation = watershed(elevation_map, markers)
segmentation = ndi.binary_fill_holes(segmentation - 1)
labeled_coins, _ = ndi.label(segmentation)

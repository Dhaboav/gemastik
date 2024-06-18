import os
import cv2
from src.python.Storage import Storage
from src.python.ImageClassifier import ImageClassifier


storage = Storage()
image_class = ImageClassifier()

image_datasets = storage.set_image_datasets('datasets')
loader = storage.load_image_dataset()
for fn in loader:
    # Read image in grayscale for variance calculation
    im_gray = cv2.imread(fn, cv2.IMREAD_GRAYSCALE)
    if im_gray is None:
        print(f'Failed to load image {fn}')
        continue

    var = image_class.image_classification(im_gray)
    print(f'{os.path.basename(fn)} {var}')
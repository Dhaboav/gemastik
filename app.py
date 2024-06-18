import os
import cv2
from src.python.Storage import Storage
from src.python.ImageClassifier import ImageClassifier


storage = Storage()
storage.set_image_path('datasets')
# image_class = ImageClassifier()

# image_datasets = storage.set_image_datasets('datasets')
# loader = storage.load_image_dataset()
# for fn in loader:
#     # Read image in grayscale for variance calculation
#     im_gray = cv2.imread(fn, cv2.IMREAD_GRAYSCALE)
#     if im_gray is None:
#         print(f'Failed to load image {fn}')
#         continue

#     var = image_class.image_classification(im_gray)
#     print(f'{os.path.basename(fn)} {var}')

cap = cv2.VideoCapture(0)
capture = 0
while cap.isOpened():
    _, frame = cap.read()
    cv2.imshow('rt', frame)
    key = cv2.waitKey(1) & 0xFF
    if key == 13:
        print(capture)
        storage.save_image_dataset(frame)
        capture +=1

    if key == 27:  # ESC
        cap.release()
        cv2.destroyWindow('rt')
        break
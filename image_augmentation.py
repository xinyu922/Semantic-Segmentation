import random

import cv2 as cv
import numpy as np
from imgaug import augmenters as iaa

from config import img_rows, img_cols
from data_generator import get_image, get_category, to_bgr

if __name__ == '__main__':
    with open('names.txt', 'r') as f:
        names = f.read().splitlines()

    filename = 'valid_ids.txt'
    with open(filename, 'r') as f:
        ids = f.read().splitlines()
        ids = list(map(int, ids))
    id = random.choice(ids)
    name = names[id]
    image = get_image(name)
    category = get_category(id)

    image = cv.resize(image, (img_rows, img_cols), cv.INTER_CUBIC)
    category = cv.resize(category, (img_rows, img_cols), cv.INTER_NEAREST)

    seq = iaa.Sequential([
        iaa.Crop(px=(0, 16)),
        iaa.Fliplr(0.5)
    ])
    seq_det = seq.to_deterministic()

    images = np.zeros((1, img_rows, img_cols, 3))
    images[0] = image
    categories = np.zeros((1, img_rows, img_cols, 1))
    categories[0, :, :, 0] = category
    images_aug = seq_det.augment_images(images)
    categories_aug = seq_det.augment_images(categories)

    image = images_aug[0]
    category_bgr = to_bgr(categories_aug[0])

    cv.imshow('image', image)
    cv.imshow('category_bgr', category_bgr)
    cv.waitKey(0)
    cv.destroyAllWindows()

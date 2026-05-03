import cv2
import numpy as np
import time
from multiprocessing import Pool, cpu_count

IMG_SIZE = 224


# -------------------------
# Single Image Processing
# -------------------------
def process_image(img_path):
    img = cv2.imread(img_path)
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    img = img / 255.0
    return img


# -------------------------
# SERIAL PROCESSING
# -------------------------
def serial_processing(image_paths):
    start = time.time()

    results = [process_image(p) for p in image_paths]

    end = time.time()
    return results, end - start


# -------------------------
# PARALLEL PROCESSING
# -------------------------
def parallel_processing(image_paths):
    start = time.time()

    with Pool(cpu_count()) as p:
        results = p.map(process_image, image_paths)

    end = time.time()
    return results, end - start
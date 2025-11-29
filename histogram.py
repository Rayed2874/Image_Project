from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

def histogram_difference(paths):
    for path in paths:
# Load images using PIL and convert to grayscale
        img1 = Image.open("cat.jpg").convert("L")
        img2 = Image.open("dog.jpg").convert("L")

        # Convert to NumPy arrays
        arr1 = np.array(img1)
        arr2 = np.array(img2)

        # Compute histograms using numpy
        hist1, _ = np.histogram(arr1, bins=256, range=(0,256))
        hist2, _ = np.histogram(arr2, bins=256, range=(0,256))

        # SIMPLE HISTOGRAM DIFFERENCE
        hist_diff = np.abs(hist1 - hist2)
        total_difference = hist_diff.sum()

    print("Total Histogram Difference:", total_difference)

    # SHOW HISTOGRAMS
    plt.figure(figsize=(10,4))

    plt.subplot(1,2,1)
    plt.plot(hist1, color='black')
    plt.title("Histogram – Image 1")

    plt.subplot(1,2,2)
    plt.plot(hist2, color='black')
    plt.title("Histogram – Image 2")

    plt.tight_layout()
    plt.show()
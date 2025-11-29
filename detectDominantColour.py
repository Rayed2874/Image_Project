
import cv2
import numpy as np
from sklearn.cluster import KMeans

def dominant_colour(paths):
    for path in paths:

        # Load the image
        img = cv2.imread(path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Reshape the image to a list of pixels
        pixels = img.reshape((-1, 3))

        # Use KMeans to find dominant colors
        k = 3   # number of dominant colors to detect
        kmeans = KMeans(n_clusters=k)
        kmeans.fit(pixels)

        # Get the dominant color (the largest cluster)
        unique, counts = np.unique(kmeans.labels_, return_counts=True)
        dominant_color = kmeans.cluster_centers_[unique[np.argmax(counts)]]

        # Convert to integer RGB
        dominant_color = dominant_color.astype(int)

        print("Dominant Color (R, G, B):", dominant_color)

        # Show the color as an image
        color_preview = np.zeros((100, 300, 3), dtype=np.uint8)
        color_preview[:] = dominant_color

        import matplotlib.pyplot as plt
        plt.imshow(color_preview)
        plt.title(f"Dominant Color: {dominant_color}")
        plt.axis('off')
        plt.show()

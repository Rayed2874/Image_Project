
import cv2
import numpy as np

def count_pixels(paths):
    """
    Count red pixels in images passed from the GUI.
    """
    for path in paths:
        img = cv2.imread(path)

        if img is None:
            print("Could not load:", path)
            continue

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        lower_red1 = np.array([0, 120, 70])
        upper_red1 = np.array([10, 255, 255])

        lower_red2 = np.array([170, 120, 70])
        upper_red2 = np.array([180, 255, 255])

        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

        red_mask = mask1 + mask2

        red_pixels = cv2.countNonZero(red_mask)
        print(f"{path} → Red pixels: {red_pixels}")

        red_highlight = cv2.bitwise_and(img, img, mask=red_mask)
        cv2.imshow("Red Pixels Highlight", red_highlight)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

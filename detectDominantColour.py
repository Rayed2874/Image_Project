import cv2
import numpy as np
import wx
from PIL import Image

# -------------------------------------------------
# Helper: Convert numpy RGB color → wx.Bitmap
# -------------------------------------------------
def numpy_color_to_wx_bitmap(color, width=300, height=100):
    # color = array([R, G, B])
    img = Image.new("RGB", (width, height), tuple(color))

    wx_img = wx.Image(width, height)
    wx_img.SetData(img.tobytes())

    return wx.Bitmap(wx_img)


# -------------------------------------------------
# Main Function (called from front_end)
# -------------------------------------------------
def dominant_colour(paths, panel):
    panel.DestroyChildren()  # Clear previous content
    sizer = wx.BoxSizer(wx.VERTICAL)

    for path in paths:

        # ---- Load and convert image ----
        img = cv2.imread(path)
        if img is None:
            print(f"Error loading image: {path}")
            continue

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # ---- Flatten pixels (Nx3) ----
        pixels = img_rgb.reshape((-1, 3)).astype(np.float32)

        # ---- OpenCV KMeans (accurate dominant colour) ----
        k = 3
        criteria = (
            cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,
            20,
            1.0
        )
        _, labels, centers = cv2.kmeans(
            pixels,
            k,
            None,
            criteria,
            10,
            cv2.KMEANS_RANDOM_CENTERS
        )

        # Find the largest cluster (dominant colour)
        _, counts = np.unique(labels, return_counts=True)
        dominant_color = centers[np.argmax(counts)].astype(int)

        print("Dominant Color (R, G, B):", dominant_color)

        # ---- Create colour preview box ----
        bmp = numpy_color_to_wx_bitmap(dominant_color)
        img_ctrl = wx.StaticBitmap(panel, bitmap=bmp)
        sizer.Add(img_ctrl, 0, wx.ALL | wx.CENTER, 10)

        # ---- RGB Label ----
        label = wx.StaticText(panel, label=f"Dominant Color: {(dominant_color)}")
        label.SetFont(
            wx.Font(
                12,
                wx.FONTFAMILY_SWISS,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_BOLD
            )
        )
        label.SetForegroundColour("black")

        sizer.Add(label, 0, wx.ALL | wx.CENTER, 5)

    panel.SetSizer(sizer)
    panel.Layout()

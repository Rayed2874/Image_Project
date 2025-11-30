'''
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
'''

import cv2
import numpy as np
import wx
from PIL import Image

# Helper: Convert OpenCV image (BGR or RGB) to wx.Bitmap
def cv_to_wx_bitmap(cv_img):
    height, width = cv_img.shape[:2]

    # Convert BGR → RGB
    rgb_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)

    # Convert to PIL Image
    pil_img = Image.fromarray(rgb_img)

    # Convert PIL → wx.Image
    wx_img = wx.Image(width, height)
    wx_img.SetData(pil_img.tobytes())

    # Convert wx.Image → wx.Bitmap
    return wx.Bitmap(wx_img)


def count_pixels(paths, panel):
    panel.DestroyChildren()  # clear previous content
    sizer = wx.BoxSizer(wx.VERTICAL)

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

        # Count red pixels
        red_pixels = cv2.countNonZero(red_mask)

        # Create highlight image
        red_highlight = cv2.bitwise_and(img, img, mask=red_mask)

        # Resize highlight image for GUI display
        display_img = cv2.resize(red_highlight, (400, 300))

        # Convert for display on wxPython panel
        bmp = cv_to_wx_bitmap(display_img)

        # Add image to panel
        img_ctrl = wx.StaticBitmap(panel, bitmap=bmp)
        sizer.Add(img_ctrl, 0, wx.ALL | wx.CENTER, 10)

        # Add text showing the number of red pixels
        text = wx.StaticText(panel, label=f"Red Pixels in {path} : {red_pixels}")
        text.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        text.SetForegroundColour("black")

        sizer.Add(text, 0, wx.ALL | wx.CENTER, 5)

    panel.SetSizer(sizer)
    panel.Layout()

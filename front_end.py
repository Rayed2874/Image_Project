import wx
import countRedPixels
import detectObjects
import detectDominantColour
import histogram
from PIL import Image

def choose_image(event):
    global paths
    paths = []
    wildcard = "Image files(.jpg, .jpeg, .png)|*.jpg;*.jpeg;*.png"
    choose_window = wx.FileDialog(None, "Select an image",wildcard = wildcard, style=wx.FD_MULTIPLE)
    if choose_window.ShowModal() == wx.ID_OK:#checks whether i clicked ok 
        paths = choose_window.GetPaths()#list

    panel2.DestroyChildren()#to remove the previous used picture if any 

    sizer1 = wx.GridSizer(3,3,10,10)
    for path in paths:
        img = wx.Image(path, wx.BITMAP_TYPE_ANY)
        img = img.Scale(300, 200)  
        bmp = wx.Bitmap(img)
        img_ctrl = wx.StaticBitmap(panel2, bitmap=bmp)

        sizer1.Add(img_ctrl, 1, wx.ALL, 3)
    panel2.SetSizer(sizer1)
    panel2.Layout()# because we are adding one by one 

    choose_window.Destroy()

def to_greyscale(event):
    for path in paths:
        image = Image.open(path)
        grey = image.convert("L")
        grey.show()
    
def count_red_pixels_button(event):
    if not paths:
        print("No images selected!")
        return None

    # Call the external file's function
    countRedPixels.count_pixels(paths)

def detect_object_button(event):
    if not paths:
        print("No images selected!")
        return None
    detectObjects.detect_object(paths)

def dominant_colour_button(event):
    if not paths:
        print("No image is selected!")
        return None
    detectDominantColour.dominant_colour(paths)

def histogram_button(event):
    global image_paths_for_hist
    paths_histo = []
    path1 = image_paths_for_hist.get("image1")
    path2 = image_paths_for_hist.get("image2")
    paths_histo.append(path1) 
    paths_histo.append(path2) 
    if not path1 or not path2:
        print("Please load both Image 1 and Image 2!")
        return None
    histogram.histogram_difference(paths_histo)
'''
def load_image(event):
    wildcard = "Image files(.jpg, .jpeg, .png)|*.jpg;*.jpeg;*.png"
    choose_window = wx.FileDialog(None, "Select an image",wildcard = wildcard, style=wx.FD_OPEN)
    if choose_window.ShowModal() == wx.ID_OK:#checks whether i clicked ok 
        path = choose_window.GetPath()#list
    choose_window.Destroy()

    sizer3 = wx.BoxSizer(wx.VERTICAL)
    sizer3.Add(btn6, 1, wx.ALL, 10)
    sizer3.Add(sizer5,1, wx.ALL, 10)
    sizer5 = wx.GridSizer(2,2,20,20)
    sizer5.Add(btn8,1,wx.ALL,10)
    sizer5.Add(btn7,1,wx.ALL,10)

    # sizer5 = wx.GridSizer(2,2,10,10)
    img = wx.Image(path, wx.BITMAP_TYPE_ANY)
    img = img.Scale(300, 200)  
    bmp = wx.Bitmap(img)
    img_ctrl = wx.StaticBitmap(panel3, bitmap=bmp)
    sizer5.Add(img_ctrl, 1, wx.ALL, 3)

    sizer3.SetSizer(sizer5)
    sizer3.Layout()




    panel3.SetSizer(sizer3)
'''
def load_image(event):
    # Determine which button was clicked (btn7 for image 1, btn8 for image 2)
    # The control to update will be img_ctrl1 or img_ctrl2
    # The key for the global dictionary will be "image1" or "image2"
    if event.GetEventObject() == btn7:
        key = "image1"
    elif event.GetEventObject() == btn8:
        key = "image2"
    else:
        # Should not happen
        return

    wildcard = "Image files(.jpg, .jpeg, .png)|*.jpg;*.jpeg;*.png"
    choose_window = wx.FileDialog(None, f"Select {key}", wildcard=wildcard, style=wx.FD_OPEN)
    
    path = None
    if choose_window.ShowModal() == wx.ID_OK:
        path = choose_window.GetPath()
    choose_window.Destroy()

    if path:
        # Store the path globally for histogram_button to use
        global image_paths_for_hist
        image_paths_for_hist[key] = path

        # Load and display the image in the correct control
        img = wx.Image(path, wx.BITMAP_TYPE_ANY)
        # Scale to fit, but preserve aspect ratio for better look (using Scale)
        img = img.Scale(300, 200, quality=wx.IMAGE_QUALITY_HIGH)
        bmp = wx.Bitmap(img)
        
        # Get the correct image control and update its bitmap
        img_ctrl = image_controls_for_hist[key]
        img_ctrl.SetBitmap(bmp)

        # Force panel3 to re-layout to display the new image
        panel3.Layout()
   


app1 = wx.App()
frame1 = wx.Frame(None, title = "Jackfruit Problem", size = (1500,900))
panel1 = wx.Panel(frame1)
panel1.SetBackgroundColour("#E37CDC")


panel2 = wx.Panel(frame1)
panel2.SetBackgroundColour("#ADF185")

panel3 = wx.Panel(frame1)
panel3.SetBackgroundColour("#F1C485")

sizer = wx.BoxSizer(wx.HORIZONTAL)
sizer.Add(panel1, 1, wx.EXPAND | wx.ALL, 5)
sizer.Add(panel2, 2, wx.EXPAND | wx.ALL, 5)
sizer.Add(panel3, 1, wx.EXPAND | wx.ALL, 5)

frame1.SetSizer(sizer)

               


font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
btn1 = wx.Button(panel1,label = "Select image")
btn2 = wx.Button(panel1,label = "Convert to \n GreyScale")
btn3 = wx.Button(panel1,label = "Count Number of \n Red Pixels")
btn5 = wx.Button(panel1,label = "Detect the \n dominant colour")
btn4 = wx.Button(panel1,label = "Detect Objects")
btn6 = wx.Button(panel3,label = "Histogram difference")
text = wx.StaticText(panel1,label = "Picture to GreyScale")
btn7 = wx.Button(panel3,label = "Load image 1")
btn8 = wx.Button(panel3,label = "Load image 2")

text.SetFont(font)
btn1.SetFont(font)
btn2.SetFont(font)
btn3.SetFont(font)
btn4.SetFont(font)
btn5.SetFont(font)
btn6.SetFont(font)
btn7.SetFont(font)
btn8.SetFont(font)



btn1.Bind(wx.EVT_BUTTON, choose_image)
btn2.Bind(wx.EVT_BUTTON, to_greyscale)
btn3.Bind(wx.EVT_BUTTON, count_red_pixels_button)
btn5.Bind(wx.EVT_BUTTON, dominant_colour_button)
btn4.Bind(wx.EVT_BUTTON, detect_object_button)
btn6.Bind(wx.EVT_BUTTON, histogram_button)
btn7.Bind(wx.EVT_BUTTON, load_image)
btn8.Bind(wx.EVT_BUTTON, load_image)


sizer4=wx.GridSizer(7,1,50,50)
# sizer =wx.BoxSizer(wx.VERTICAL)
sizer4.Add(text, 1,wx.EXPAND | wx.ALL,5)
sizer4.Add(btn1, 1,wx.EXPAND | wx.ALL,5)
sizer4.Add(btn2, 1,wx.EXPAND | wx.ALL,5)
sizer4.Add(btn3, 1,wx.EXPAND | wx.ALL,5)
sizer4.Add(btn5, 1,wx.EXPAND | wx.ALL,5)
sizer4.Add(btn4, 1,wx.EXPAND | wx.ALL,5)


# sizer3 = wx.BoxSizer(wx.VERTICAL)
# # sizer5 = wx.GridSizer(2,2,20,20)
# sizer5.Add(btn7,1,wx.ALL,10)
# sizer5.Add(btn8,1,wx.ALL,10)



# sizer3.Add(btn6, 1, wx.ALL, 10)
# sizer3.Add(sizer5,1, wx.ALL, 10)
# panel3.SetSizer(sizer3)


sizer5 = wx.GridSizer(2, 2, 20, 20)  # The sizer for the images/buttons
sizer5.Add(btn7, 1, wx.ALL, 10)  # Load image 1 button
sizer5.Add(btn8, 1, wx.ALL, 10)  # Load image 2 button

# Placeholder StaticBitmaps for the images
# We need these controls to exist so we can update them later
# We'll use None for the bitmap initially.
img_ctrl1 = wx.StaticBitmap(panel3, bitmap=wx.NullBitmap)
img_ctrl2 = wx.StaticBitmap(panel3, bitmap=wx.NullBitmap)

sizer5.Add(img_ctrl1, 1, wx.ALL | wx.EXPAND, 3)
sizer5.Add(img_ctrl2, 1, wx.ALL | wx.EXPAND, 3)

sizer3 = wx.BoxSizer(wx.VERTICAL) # The main vertical sizer for panel3
sizer3.Add(btn6, 0, wx.ALL | wx.EXPAND, 10) # Histogram difference button (not expanding by default)
sizer3.Add(sizer5, 1, wx.EXPAND | wx.ALL, 10) # The image/button sizer

panel3.SetSizer(sizer3)

# Global variables to store the loaded image paths and controls
image_paths_for_hist = {"image1": None, "image2": None}
image_controls_for_hist = {"image1": img_ctrl1, "image2": img_ctrl2}




panel1.SetSizer(sizer4)


frame1.Show() 
app1.MainLoop()
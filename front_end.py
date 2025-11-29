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
    if not paths:
        print("No image selected!")
        return None
    histogram.histogram_difference(paths)


app1 = wx.App()
frame1 = wx.Frame(None, title = "Jackfruit Problem", size = (1500,900))
panel1 = wx.Panel(frame1)
panel1.SetBackgroundColour("#E37CDC")


panel2 = wx.Panel(frame1)
panel2.SetBackgroundColour("#ADF185")

sizer = wx.BoxSizer(wx.HORIZONTAL)
sizer.Add(panel1, 1, wx.EXPAND | wx.ALL, 5)
sizer.Add(panel2, 2, wx.EXPAND | wx.ALL, 5)

frame1.SetSizer(sizer)

               


font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
btn1 = wx.Button(panel1,label = "Select image")
btn2 = wx.Button(panel1,label = "Convert to \n GreyScale")
btn3 = wx.Button(panel1,label = "Count Number of \n Red Pixels")
btn5 = wx.Button(panel1,label = "Detect the \n dominant colour")
btn4 = wx.Button(panel1,label = "Detect Objects")
btn6 = wx.Button(panel1,label = "Histogram difference")

text = wx.StaticText(panel1,label = "Picture to GreyScale")
text.SetFont(font)
btn1.SetFont(font)
btn2.SetFont(font)
btn3.SetFont(font)
btn4.SetFont(font)
btn5.SetFont(font)
btn6.SetFont(font)



btn1.Bind(wx.EVT_BUTTON, choose_image)
btn2.Bind(wx.EVT_BUTTON, to_greyscale)
btn3.Bind(wx.EVT_BUTTON, count_red_pixels_button)
btn5.Bind(wx.EVT_BUTTON, dominant_colour_button)
btn4.Bind(wx.EVT_BUTTON, detect_object_button)
btn6.Bind(wx.EVT_BUTTON, histogram_button)


sizer =wx.GridSizer(7,1,50,50)
# sizer =wx.BoxSizer(wx.VERTICAL)
sizer.Add(text, 1,wx.EXPAND | wx.ALL,5)
sizer.Add(btn1, 1,wx.EXPAND | wx.ALL,5)
sizer.Add(btn2, 1,wx.EXPAND | wx.ALL,5)
sizer.Add(btn3, 1,wx.EXPAND | wx.ALL,5)
sizer.Add(btn5, 1,wx.EXPAND | wx.ALL,5)
sizer.Add(btn4, 1,wx.EXPAND | wx.ALL,5)
sizer.Add(btn6, 1,wx.EXPAND | wx.ALL,5)





panel1.SetSizer(sizer)
frame1.Show() 
app1.MainLoop()
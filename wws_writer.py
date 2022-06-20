"""

"""

import wx
import cv2
import tensorflow as tf
import numpy as np


# Initialize Camera and list of positions
cam = cv2.VideoCapture(0)

pos = []
for j in range(5):
    for k in range(4):
        pos.append([j,k])


class MyFrame(wx.Frame):
    '''
    Sets the frame with the GRID
    '''
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, "Write with Sight")
        
        self.panel = MyPanel(self)
        self.panel.SetBackgroundColour(wx.Colour(255,255,255))
        self.panel.SetForegroundColour(wx.Colour(0,0,0))
        
        # Inialize panel  options
        self.panel.xx = [4,3]
        self.panel.pos_hist = []
        self.panel.cell_mode = True
               
        # Horizontal sizer
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer.Add(self.panel, 1, wx.EXPAND | wx.ALL, 0)

        Snap_button = wx.Button(self.panel, label = 'Snap', pos = (10, 10))
        Snap_button.Bind(wx.EVT_BUTTON, self.OnSnap)
        
        Stop_button = wx.Button(self.panel, label = 'Stop', pos = (10, 40))
        Stop_button.Bind(wx.EVT_BUTTON, self.OnStop)
        
        Draw_button = wx.Button(self.panel, label = 'Draw', pos = (10, 70))
        Draw_button.Bind(wx.EVT_BUTTON, self.OnDraw)
        
        self.SetSizer(main_sizer)
        self.Layout()
                      
    def OnSnap(self, event):
        'Starts the timer'
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.UpdatePanel)
        self.timer.Start(40)
        
    def OnStop(self, event):
        'Stops the timer'
        self.timer = wx.Timer(self)
        self.timer.Stop()
        cam.release()
        cv2.destroyAllWindows()
        
    def OnDraw(self, event):
        'Draws the outcome'
        self.panel.cell_mode = False
        self.panel.Refresh()
        
    def UpdatePanel(self, event):
        'Updates the panel to show the lighted cell'
        model = tf.keras.models.load_model('Models/eye_tracker')
        ret, cam_frame = cam.read()
        # Crop and flip the image
        scale = 10
        #get the webcam size
        height, width, channels = cam_frame.shape
        centerX, centerY = int(height/2), int(width/2)
        radiusX, radiusY = int(scale*height/100), int(scale*width/100)
        minX, maxX = centerX - radiusX, centerX + radiusX
        minY, maxY = centerY - radiusY, centerY + radiusY
        cropped = cam_frame[minX:maxX, minY:maxY]
        resized_cropped = cv2.resize(cropped, (width, height))           
        cam_img = cv2.cvtColor(cv2.flip(resized_cropped,1), 
                                 cv2.COLOR_BGR2GRAY)
        pred = np.argmax(model.predict(np.expand_dims(cam_img, axis=0)))
        xx = pos[pred]
        print(xx)
        self.panel.pos_hist.append(xx)
        self.panel.xx = xx
        self.panel.Refresh()
        
class MyPanel(wx.Panel):
    '''
    Panel with tracking cell
    '''
    def __init__(self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, 
                 size = wx.DefaultSize, style = 0, name = "MyPanel"):
        super(MyPanel, self).__init__(parent, id, pos, size, style, name)
        
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
    
    def OnSize(self, event):
        self.Refresh()
        event.Skip()
        
    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        rect = self.GetClientRect()
        height = int(rect[3]/5)
        base = int(rect[2]/4)
        for col in range(4):
            for row in range(5):
                
                if self.cell_mode:
                    cond = [row, col] == self.xx
                else:
                    cond = [row, col] in self.pos_hist
                # Select the right color for the cell
                if cond:
                    dc.SetBrush(wx.BLACK_BRUSH) 
                else:
                    dc.SetBrush(wx.WHITE_BRUSH) 
                dc.DrawRectangle(1 + col*base, 1 + row*height, base, height) 
    

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame(None)
    app.SetTopWindow(frame)
    frame.Show()
    frame.Maximize(True)
    app.MainLoop()
# -*- coding: utf-8 -*-
"""
Program to get data from camera
"""

import wx
import cv2
import os
import random

# Generate List of positions to aquire data:
list_flag = True
pos_list = []

def list_of_positions():
    global list_flag
    global pos_list
        
    if list_flag:
        L = []
        for n in range(10):
            for row in range(5):
                for col in range(4):
                    L.append([row+1,col+1])
        random.shuffle(L)
        pos_list = L
        list_flag = False
    
    return pos_list

# Create dataset Directories
from pathlib import Path
pathx = "C:/Users/jguil/Documents/Codes/CV_Tobii/Data_set/"
for row in range(5):
    for col in range(4):
        Path((pathx + "{0}{1}/").format(row + 1, col + 1)).mkdir(parents=True, 
                                                                 exist_ok=True)


# Initialize Camera
cam = cv2.VideoCapture(0)
rr, cc = cam.read()

class MyFrame(wx.Frame):
    '''
    Sets the frame with the GRID
    '''
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, "Write with Sight")
        
        self.panel = MyPanel(self)
        self.panel.SetBackgroundColour(wx.Colour(255,255,255))
        self.panel.SetForegroundColour(wx.Colour(0,0,0))
        # Horizontal sizer
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer.Add(self.panel, 1, wx.EXPAND | wx.ALL, 0)
        
        Snap_button = wx.Button(self.panel, label = 'Snap', pos = (10, 10))
        Snap_button.Bind(wx.EVT_BUTTON, self.OnSnap)
        
        self.SetSizer(main_sizer)
        self.Layout()
               
        self.panel.snap_number = 0
        self.panel.Lst = list_of_positions()
    
    def OnSnap(self, event):
        if self.panel.snap_number + 1 > len(self.panel.Lst):
            print('Finished list')
            cam.release()
            cv2.destroyAllWindows()
        else:
            row = self.panel.Lst[self.panel.snap_number][0]
            col = self.panel.Lst[self.panel.snap_number][1]
            path = (pathx + "{0}{1}/").format(row,col)
            img_name = "F{0}{1}_{2}.png".format(row,col,self.panel.snap_number)
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
            print(img_name)
            cv2.imwrite(os.path.join(path, img_name), cam_img)
            self.panel.snap_number += 1
            if self.panel.snap_number + 1 <= len(self.panel.Lst):
                self.Refresh()


class MyPanel(wx.Panel):
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
        
        row_on = self.Lst[self.snap_number][0] - 1
        col_on = self.Lst[self.snap_number][1] - 1
        height = int(rect[3]/5)
        base = int(rect[2]/4)
        
        for col in range(4):
            for row in range(5):
                if col == col_on and row == row_on:
                    dc.SetBrush(wx.BLACK_BRUSH) 
                else:
                    dc.SetBrush(wx.WHITE_BRUSH) 
                dc.DrawRectangle(1 + col*base, 1 + row*height, base, height) 
        
        if self.snap_number + 1 == len(self.Lst):
            dc.SetBrush(wx.RED_BRUSH) 
            dc.DrawRectangle(1 + col_on*base, 1 + row_on*height, base, height)


if __name__ == '__main__':   
    
    app = wx.App()
    frame = MyFrame(None)
    app.SetTopWindow(frame)
    frame.Show()
    frame.Maximize(True)
    app.MainLoop()
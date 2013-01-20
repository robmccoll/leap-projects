################################################################################
# Copyright (C) 2012-2013 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################

import Leap, sys, wx

DEBUG_VERBOSE = False

class OneFinger(Leap.Listener):
    def __init__(self, location):
        Leap.Listener.__init__(self)
        self.location = location

    def on_frame(self, controller):
        frame = controller.frame()
        if not frame.hands.empty and not frame.hands[0].fingers.empty:
            fingers = frame.hands[0].fingers
            if len(fingers) == 1:
                self.location.set_location(fingers[0].tip_position[0],
                                           fingers[0].tip_position[1],
                                           fingers[0].tip_position[2])
            

class Location:
    def __init__(self, panel):
        self.loc = Leap.Vector(200,100,-200)
        self.x = 200
        self.y = 100
        self.z = -200
        self.bmp = wx.EmptyBitmap(1000,800)
        self.dc = wx.MemoryDC()
        self.dc.SelectObject(self.bmp)
        self.panel = panel

    def set_location(self, x,y,z):
        if DEBUG_VERBOSE:
            print "set_loc: %d,%d, %d)" % (x, y, z)
        self.x = x*3 + 500
        self.y = 1270 - y*3
        self.z = - z - 30
        self.panel.Refresh()

    def paint_location(self, event):
        dc = wx.PaintDC(event.GetEventObject())
        dc.Blit(0,0,1000,800,self.dc,0,0,wx.COPY)
        if(self.z < 0):
            if(self.z > -150):
                dc.SetPen(wx.Pen("RED", self.z))
                dc.DrawLine(self.x,self.y, self.x, self.y)
        else:
            self.dc.SetPen(wx.Pen("BLUE", 10))
            self.dc.DrawLine(self.x,self.y, self.x, self.y)

def main():
    # Create the wxApp and frame
    app = wx.App(False)
    frame = wx.Frame(None, title = "Drawing")
    frame.SetSizeWH(1000,800)
    panel = wx.Panel(frame)
    panel.SetDoubleBuffered(True)
    
    loc = Location(panel)
    panel.Bind(wx.EVT_PAINT, loc.paint_location)
    
    # Create a sample listener and controller
    listener = OneFinger(loc)
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Display window and start main loop
    frame.Show(True)
    app.MainLoop()
    
    # Remove the sample listener when done
    controller.remove_listener(listener)


if __name__ == "__main__":
    main()

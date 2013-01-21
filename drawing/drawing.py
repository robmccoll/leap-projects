################################################################################
# Copyright Rob and Mark McColl 2012
# This source code is available under the terms of the 3-part BSD Open Source
# license. http://opensource.org/licenses/BSD-3-Clause
################################################################################

import Leap, sys, wx

class ScaledVector(Leap.Vector):
    def __init__(self, init, scale, in_min, in_max):
        Leap.Vector.__init__(self, init)
        self.scale = scale
        self.in_min = in_min
        self.in_max = in_max
        self.in_range = in_max - in_min

    def interpolate(self, val, scale, in_max, in_min, in_range):
        if(val > max(in_max,in_min)):
            return scale
        elif(val < min(in_min,in_max)):
            return 0
        else:
            return scale * ((val - in_min) / in_range)
    def set(self, val):
        self.x = self.interpolate(val.x, self.scale.x, self.in_max.x, self.in_min.x, self.in_range.x)
        self.y = self.interpolate(val.y, self.scale.y, self.in_max.y, self.in_min.y, self.in_range.y)
        self.z = self.interpolate(val.z, self.scale.z, self.in_max.z, self.in_min.z, self.in_range.z)

    def copy_to_vec(self, vec):
        vec.x = self.x
        vec.y = self.y
        vec.z = self.z

class OneFinger(Leap.Listener):
    def __init__(self, location):
        Leap.Listener.__init__(self)
        self.location = location

    def on_frame(self, controller):
        frame = controller.frame()
        if not frame.hands.empty and not frame.hands[0].fingers.empty:
            fingers = frame.hands[0].fingers
            self.location.set_location(fingers[0].tip_position, len(fingers) == 1)

class LocationPainter:
    def __init__(self, panel, scaledvec):
        self.loc = scaledvec
        self.prev = Leap.Vector(scaledvec)
        self.on = self.loc.scale.z * 0.5
        self.bmp = wx.EmptyBitmap(self.loc.scale.x, self.loc.scale.y)
        self.dc = wx.MemoryDC()
        self.dc.SelectObject(self.bmp)
        self.panel = panel

    def set_location(self, new_loc, erase):
        self.loc.set(new_loc)
        self.panel.Refresh()

    def paint_location(self, event):
        dc = wx.PaintDC(event.GetEventObject())
        dc.Blit(0,0,self.loc.scale.x, self.loc.scale.y,self.dc,0,0,wx.COPY)
        if(self.loc.z > self.on):
            dc.SetPen(wx.Pen("RED", self.loc.z - self.on + 10))
            dc.DrawLine(self.loc.x,self.loc.y, self.loc.x, self.loc.y)
        else:
            self.dc.SetPen(wx.Pen("BLUE", 10))
            self.dc.DrawLine(self.prev.x,self.prev.y, self.loc.x, self.loc.y)
        self.loc.copy_to_vec(self.prev)

def main():
    init_pos = Leap.Vector(500, 400, 100)
    img_size = Leap.Vector(1000, 800, 100)
    phys_min = Leap.Vector(-70, 360, -180)
    phys_max = Leap.Vector(100, 130, 60)
    scaled_vec = ScaledVector(init_pos, img_size, phys_min, phys_max)
    
    # Create the wxApp and frame
    app = wx.App(False)
    frame = wx.Frame(None, title = "Drawing")
    frame.SetSizeWH(img_size.x, img_size.y)
    panel = wx.Panel(frame)
    panel.SetDoubleBuffered(True)
    
    loc = LocationPainter(panel, scaled_vec)
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

#!/usr/bin/env python

# example progressbar.py

import pygtk
pygtk.require('2.0')
import gtk, gobject
import pexpect
import threading, re, sys
# Update the value of the progress bar so that we get
# some movement

progressFraction=0.0

gtk.gdk.threads_init()


def progress_timeout(pbobj):
    
    return True

class ProgressBar:
    # Callback that toggles the text display within the progress
    # bar trough
    def toggle_show_text(self, widget, data=None):
        if widget.get_active():
            self.pbar.set_text("some text")
        else:
            self.pbar.set_text("")

    # Callback that toggles the activity mode of the progress
    # bar
    def hello(self, widget, data=None):
        self.hilo = threading.Thread(target=self.run_script)
        self.hilo.start()

    def toggle_activity_mode(self, widget, data=None):
        if widget.get_active():
            self.pbar.pulse()
        else:
            self.pbar.set_fraction(0.0)

    # Callback that toggles the orientation of the progress bar
    def toggle_orientation(self, widget, data=None):
        if self.pbar.get_orientation() == gtk.PROGRESS_LEFT_TO_RIGHT:
            self.pbar.set_orientation(gtk.PROGRESS_RIGHT_TO_LEFT)
        elif self.pbar.get_orientation() == gtk.PROGRESS_RIGHT_TO_LEFT:
            self.pbar.set_orientation(gtk.PROGRESS_LEFT_TO_RIGHT)

    # Clean up allocated memory and remove the timer
    def destroy_progress(self, widget, data=None):
        # gobject.source_remove(self.timer)
        # self.timer = 0
        gtk.main_quit()

    def run_script(self):
        
        command = './frames'

        #~ print command
        #~ return
        # if self.started:
        #     self.button1.set_label(gtk.STOCK_GO_DOWN)
        #     self.child.sendline(chr(3))
        #     self.started = False
        #     return
        # else:
        #     self.button1.set_label(gtk.STOCK_STOP)
        #     self.started = True

        self.set_progress(0, 'Still working')
        self.child = pexpect.spawn(command)

        cpl = self.child.compile_pattern_list([pexpect.EOF,
                                   'frame (\d+)',
                                   'number (\d+)'])
        while True:
            i = self.child.expect_list(cpl, timeout=None)
            if i == 0: # EOF
                print "the sub process exited"
                break
            elif i == 1:
                frame_number = self.child.match.group(1)
                self.set_progress(float(frame_number)/float(total_frames),"Still working man");
                print "frame number is %d" % int(frame_number)
            elif i ==2:
                total_frames = self.child.match.group(1)

                print "total frames are %d" % int(total_frames)
        self.set_progress(1,"I am finished");
        self.child.close()
        
    def set_progress(self, percent, text):
        self.pbar.set_text('%s' % text)
        self.pbar.set_fraction(percent)
        return True

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_resizable(True)

        self.window.connect("destroy", self.destroy_progress)
        self.window.set_title("ProgressBar")
        self.window.set_border_width(0)

        vbox = gtk.VBox(False, 5)
        vbox.set_border_width(10)
        self.window.add(vbox)
        vbox.show()
  
        # Create a centering alignment object
        align = gtk.Alignment(0.5, 0.5, 0, 0)
        vbox.pack_start(align, False, False, 5)
        align.show()

        # Create the ProgressBar
        self.pbar = gtk.ProgressBar()

        align.add(self.pbar)
        self.pbar.show()
        
        # Add a timer callback to update the value of the progress bar
        # self.timer = gobject.timeout_add (100, progress_timeout, self)

        separator = gtk.HSeparator()
        vbox.pack_start(separator, False, False, 0)
        separator.show()

        # rows, columns, homogeneous
        table = gtk.Table(2, 2, False)
        vbox.pack_start(table, False, True, 0)
        table.show()

        # Add a check button to select displaying of the trough text
        check = gtk.CheckButton("Show text")
        table.attach(check, 0, 1, 0, 1,
                     gtk.EXPAND | gtk.FILL, gtk.EXPAND | gtk.FILL,
                     5, 5)
        check.connect("clicked", self.toggle_show_text)
        check.show()

        # Add a check button to toggle activity mode
        self.activity_check = check = gtk.CheckButton("Activity mode")
        table.attach(check, 0, 1, 1, 2,
                     gtk.EXPAND | gtk.FILL, gtk.EXPAND | gtk.FILL,
                     5, 5)
        check.connect("clicked", self.toggle_activity_mode)
        check.show()

        # Add a check button to toggle orientation
        check = gtk.CheckButton("Right to Left")
        table.attach(check, 0, 1, 2, 3,
                     gtk.EXPAND | gtk.FILL, gtk.EXPAND | gtk.FILL,
                     5, 5)
        check.connect("clicked", self.toggle_orientation)
        check.show()

        button1 = gtk.Button("Run!")
    
        # When the button receives the "clicked" signal, it will call the
        # function hello() passing it None as its argument.  The hello()
        # function is defined above.
        button1.connect("clicked",self.hello, None)
        vbox.pack_start(button1, False, False, 0)
        # Add a button to exit the program
        button2 = gtk.Button("close")
        button2.connect("clicked", self.destroy_progress)
        vbox.pack_start(button2, False, False, 0)

        # This makes it so the button is the default.
        button1.set_flags(gtk.CAN_DEFAULT)

        # This grabs this button to be the default button. Simply hitting
        # the "Enter" key will cause this button to activate.
        button1.grab_default ()
        button1.show()
        button2.show()

        self.window.show()

def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    ProgressBar()
    main()
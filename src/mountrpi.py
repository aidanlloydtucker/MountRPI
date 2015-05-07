# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "aidan"
__date__ = "$May 4, 2015 7:37:26 PM$"

import ttk
import Tkinter as tk
import platform
import urllib
import time
import threading
#piversion = 0

LARGE_FONT= ("Verdana", 12)

def combine_funcs(*funcs):
    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)
    return combined_func

def download():
    print "hello world"
    if piversion.get() == 1:
        print "1"
        #urllib.urlretrieve ("http://downloads.sourceforge.net/project/runeaudio/Images/Raspberry%20Pi/RuneAudio_rpi_0.3-beta_20141029_2GB.img.gz?r=http%3A%2F%2Fwww.runeaudio.com%2Fdownload%2F&ts=1430927551&use_mirror=iweb", "RPI.img.gz")
        time.sleep(5)
    elif piversion.get() == 2:
        print "2"
        #urllib.urlretrieve ("http://downloads.sourceforge.net/project/runeaudio/Images/Raspberry%20Pi%202/RuneAudio_rpi2_0.3-beta_20150304_2GB.img.gz?r=http%3A%2F%2Fwww.runeaudio.com%2Fdownload%2F&ts=1430927581&use_mirror=superb-dca2", "RPI.img.gz")
        time.sleep(5)
    else:
        print "Broken download()"

def start_download_thread():
    global download_thread
    download_thread = threading.Thread(target=download)
    download_thread.daemon = True
    
    downBar.start()
    pg2labeltop.set("Downloading...")
    canceldownload.config(state="tk.normal")
    canceldownload.update()
    startdownload.config(state="tk.disabled")
    startdownload.update()
    
    download_thread.start()
    app.after(20, check_download_thread)

def check_download_thread():
    if download_thread.is_alive():
        app.after(20, check_download_thread)
    else:
        downBar.stop()

def osApp():
    if platform.system() == "Darwin":
        print "Mac"
    elif platform.system() == "Windows":
        print "Windows"
    elif platform.system() == "Linux":
        print "Linux"
    else:
        print "Unknown OS"

class Installgui(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Raspberry Pi Music Player Install", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button = tk.Button(self, text="Start",
                            command=lambda: controller.show_frame(PageOne))
        button.pack()


class PageOne(tk.Frame):
    
    def __init__(self, parent, controller):
        
        global piversion
        piversion = tk.IntVar()
        piversion.set(1)
        
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Raspberry Pi Version:", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        tk.Radiobutton(self, text="Raspberry Pi v1 (Model A/B/A+/B+)", variable=piversion, value=1).pack()
        tk.Radiobutton(self, text="Raspberry Pi v2 (Model B)", variable=piversion, value=2).pack()


        button1 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = tk.Button(self, text="Download",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        
        global pg2labeltop
        pg2labeltop = tk.StringVar()
        pg2labeltop.set("")
        
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, textvariable=pg2labeltop, font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        
        global downBar
        downBar = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=200, mode='indeterminate')
        downBar.pack()
        
        global startdownload
        startdownload = tk.Button(self, text="Start Download", state=tk.NORMAL, command=start_download_thread)
        startdownload.pack()
        
        global canceldownload
        canceldownload = tk.Button(self, state=tk.DISABLED, text="Cancel Download", command=lambda: controller.show_frame(PageOne))
        canceldownload.pack()


class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Finished!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = tk.Button(self, text="Open Installer",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = tk.Button(self, text="Exit (No Installer)",
                            command=lambda: controller.show_frame(PageOne))
        button2.pack()


app = Installgui()
app.title("RPI Install")
app.mainloop()
import imgurScraper as IS
import Tkinter, Tkconstants, tkFileDialog

class Interface:
    def __init__(self, top):

        frame = Tkinter.Frame(top, borderwidth=3)
        
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=3)

        #create all elements
        Tkinter.Label(frame, text="Folder: ").grid(row=0, sticky=Tkinter.W, padx=3, pady=3)
        self.folderEntry = Tkinter.Entry(frame)
        self.folderEntry.insert(0, "defaultDownloadFolder")
        self.folderEntry.grid(row=0, column=1, padx=3, pady=3)

        Tkinter.Label(frame, text="Search: ").grid(row=1, sticky=Tkinter.W, padx=3, pady=3)
        self.searchEntry = Tkinter.Entry(frame)
        self.searchEntry.grid(row=1, column=1, padx=3, pady=3)

        self.b1 = Tkinter.Button(frame, text="Download Images", command=self.startDownload)
        self.b1.grid(row=2, sticky=Tkinter.W, columnspan=2)

        Tkinter.Label(frame, text="Start Page: ").grid(row=0, column=2, sticky=Tkinter.E)
        self.startSpinner = Tkinter.Spinbox(frame, width=4, from_=0, to=1000)
        self.startSpinner.grid(row=0, column=3)
        
        Tkinter.Label(frame, text="End Page: ").grid(row=1, column=2, stick=Tkinter.E)
        self.endSpinner = Tkinter.Spinbox(frame, width=4, from_=1, to=1000)
        self.endSpinner.grid(row=1, column=3)

        self.slowDownloadCheckbox = Tkinter.Checkbutton(frame, text="Slow download")
        self.slowDownloadCheckbox.grid(row=2, column=2, columnspan=2, sticky=Tkinter.E)
        
        frame.grid()

    def startDownload(self):
        print(self.slowDownloadCheckbox.var)
        #IS.changeDownloadFolder(self.folderEntry.get())
        #IS.downloadAllImagesFromSearch(self.searchEntry.get(), )
    
        
master = Tkinter.Tk();
interface = Interface(master)
master.mainloop()

import imgurScraper as IS
import Tkinter, Tkconstants, tkFileDialog, tkMessageBox, thread

class Interface:
    def __init__(self, top):
        self.downloadThread = None
        top.resizable(0, 0)
        frame = Tkinter.Frame(top, borderwidth=3)
        
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=3)

        #create all elements
        #who needs good design :P
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
        self.startSpinner = Tkinter.Spinbox(frame, width=4, from_=1, to=1000)
        self.startSpinner.grid(row=0, column=3)

        Tkinter.Label(frame, text="End Page: ").grid(row=1, column=2, stick=Tkinter.E)
        self.endVar = Tkinter.StringVar(top)
        self.endVar.set("300")
        self.endSpinner = Tkinter.Spinbox(frame, width=4, from_=1, to=1000, textvariable=self.endVar)
        self.endSpinner.grid(row=1, column=3)
        self.var = Tkinter.IntVar()
        self.slowDownloadCheckbox = Tkinter.Checkbutton(frame, text="Slow download", variable=self.var)
        self.slowDownloadCheckbox.grid(row=2, column=2, columnspan=2, sticky=Tkinter.E)
        
        frame.grid()

    def displayError(self, title, errorBody):
        tkMessageBox.showwarning(title, errorBody)

    def closeWindow():
        if self.downloadThread != None:
            IS.stopDownload()

    def downloadImages(args):
        self.downloadThread = thread.start_new_thread(IS.downloadAllImagesFromSearch, (self.searchEntry.get(), bool(self.var.get()), start, end))
            
    def startDownload(self):
        if IS.isDownloading():
            self.displayError("Downloading", "You are allready downloading something")
        start = int(self.startSpinner.get())
        end = int(self.endSpinner.get())
        if start > end:
            self.displayError("Page Error!", "Start page must be larger than the end page.")
            return
        IS.changeDownloadFolder(self.folderEntry.get())
        self.downloadThread = thread.start_new_thread(IS.downloadAllImagesFromSearch, (self.searchEntry.get(), bool(self.var.get()), start, end))
    
        
master = Tkinter.Tk();
interface = Interface(master)
master.mainloop()

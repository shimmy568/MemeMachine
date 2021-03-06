import imgurScraper as IS
import Tkinter, Tkconstants, tkFileDialog, tkMessageBox, tkFileDialog, threading, os

class Interface:
    def __init__(self, top):
        self.downloadThread = None
        top.resizable(0, 0)
        frame = Tkinter.Frame(top, borderwidth=3)
        self.scraper = IS.scraperObject()
        
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=3)

        #create all elements
        #who needs good design :P
        Tkinter.Label(frame, text="Folder: ").grid(row=0, sticky=Tkinter.W, padx=3, pady=3)
        text = os.path.dirname(os.path.realpath(__file__)) + "/defaultDownloadFolder"
        self.folderEntryVar = Tkinter.StringVar()
        self.folderEntryVar.set(text)
        self.folderEntry = Tkinter.Entry(frame, textvariable=self.folderEntryVar)
        self.folderEntry.grid(row=0, column=1, padx=3, pady=3, columnspan=2)

        Tkinter.Label(frame, text="Search: ").grid(row=1, sticky=Tkinter.W, padx=3, pady=3)
        self.searchEntry = Tkinter.Entry(frame)
        self.searchEntry.grid(row=1, column=1, padx=3, pady=3, columnspan=2)

        self.albumIntoFolders = Tkinter.IntVar()
        self.albumIntoFolders.set(1)
        albumIntoFoldersCheckbox = Tkinter.Checkbutton(frame, text="Put albums into folders", variable=self.albumIntoFolders)
        albumIntoFoldersCheckbox.grid(row=2, sticky=Tkinter.W, columnspan=2) 

        self.imageType = Tkinter.IntVar()
        r1 = Tkinter.Radiobutton(frame, text="All", variable=self.imageType, value=0)
        r2 = Tkinter.Radiobutton(frame, text="Only images", variable=self.imageType, value=1)
        r3 = Tkinter.Radiobutton(frame, text="Only gifs", variable=self.imageType, value=2)
        r1.grid(row=3, sticky=Tkinter.W, column=0)
        r2.grid(row=3, sticky=Tkinter.W, column=1)
        r3.grid(row=3, sticky=Tkinter.W, column=2)

        self.frontPage = Tkinter.IntVar()
        frontPage = Tkinter.Checkbutton(frame, text="FP", variable=self.frontPage, command=self.toggleFrontPage)
        frontPage.grid(row=1, column=3, sticky=Tkinter.W)
        
        self.b1 = Tkinter.Button(frame, text="Download Images", command=self.startDownload)
        self.b1.grid(row=4, sticky=Tkinter.W, columnspan=2)

        self.b2 = Tkinter.Button(frame, text="Select", command=self.selectFolder)
        self.b2.grid(row=0, column=3)

        self.downloadAllVar = Tkinter.IntVar()
        downloadAllCheckbox = Tkinter.Checkbutton(frame, text="Download All", command=self.toggleDownloadAll, variable=self.downloadAllVar)
        downloadAllCheckbox.grid(row=0, column=4, columnspan=2)
        
        Tkinter.Label(frame, text="Num of Images: ").grid(row=1, column=4, sticky=Tkinter.E)
        spinnerDe = Tkinter.StringVar()
        spinnerDe.set("5000")
        self.imageNumSpinner = Tkinter.Spinbox(frame, textvariable=spinnerDe, width=4, from_=1, to=999999)
        self.imageNumSpinner.grid(row=1, column=5)   
        
        self.downloadText = Tkinter.StringVar()
        Tkinter.Label(frame, textvariable=self.downloadText).grid(row=4, column=2, columnspan=4, sticky=Tkinter.E)
        self.downloadText.set("Not Downloading...")
        
        frame.grid()

    def displayError(self, title, errorBody):
        tkMessageBox.showwarning(title, errorBody)

    def finsihedDownload(self):
        try:
            self.downloadMoniter(False, 0)
        except RuntimeError:
            return
        tkMessageBox.showinfo("Done", "All the images have been downloaded.")
        
    def toggleDownloadAll(self):
        if self.downloadAllVar.get() == 1:
            self.imageNumSpinner.config(state=Tkinter.DISABLED)
        else:
            self.imageNumSpinner.config(state="normal")

    def toggleFrontPage(self):
        if self.frontPage.get() == 1:
            self.searchEntry.config(state=Tkinter.DISABLED)
        else:
            self.searchEntry.config(state="normal")
    
    def closeWindow():
        if self.downloadThread != None:
            self.scraper.stopDownload()

    def downloadImages(self, search, limit, settings, done, updateCallback):
        self.scraper.downloadAllImagesFromSearch(search, limit, settings, updateCallback)
        done()

    def downloadMoniter(self, downloading, downloadNum):
        if(downloading):
            self.downloadText.set("Downloading Image: " + str(downloadNum))
        else:
            self.downloadText.set("Not Downloading...")
        
    def startDownload(self):
        if self.scraper.isDownloading():
            self.displayError("Downloading", "You are allready downloading something")
        limit = int(self.imageNumSpinner.get())
        if self.downloadAllVar.get() == 1:
            limit = -1
        searchQ = self.searchEntry.get()
        settings = IS.settingsObject()
        if self.frontPage.get() == 1:
            settings.setFP(True)
        settings.setDownloadType(self.imageType.get())
        if self.albumIntoFolders.get() == 0:
            settings.setAlbumsInFolders(False)
        self.scraper.changeDownloadFolder(self.folderEntryVar.get())
        self.downloadThread = threading.Thread(target=self.downloadImages, args=(searchQ, limit, settings, self.finsihedDownload, self.downloadMoniter))
        self.downloadThread.start()

    def selectFolder(self):
        directoryName = tkFileDialog.askdirectory()
        self.folderEntryVar.set(directoryName)
        
master = Tkinter.Tk();
interface = Interface(master)
master.wm_title("Meme Machine")
master.mainloop()

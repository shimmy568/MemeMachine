import imgurScraper as IS
import Tkinter, Tkconstants, tkFileDialog, tkMessageBox, tkFileDialog, thread, os

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
        self.folderEntry.grid(row=0, column=1, padx=3, pady=3)

        Tkinter.Label(frame, text="Search: ").grid(row=1, sticky=Tkinter.W, padx=3, pady=3)
        self.searchEntry = Tkinter.Entry(frame)
        self.searchEntry.grid(row=1, column=1, padx=3, pady=3)

        self.albumIntoFolders = Tkinter.IntVar()
        self.albumIntoFolders.set(1)
        albumIntoFoldersCheckbox = Tkinter.Checkbutton(frame, text="Put albums into folders", variable=self.albumIntoFolders)
        albumIntoFoldersCheckbox.grid(row=2, sticky=Tkinter.W, columnspan=2) 

        self.gifsOnly = Tkinter.IntVar()
        gifsOnlyCheckbox = Tkinter.Checkbutton(frame, text="Gifs only", variable=self.gifsOnly)
        gifsOnlyCheckbox.grid(row=3, sticky=Tkinter.W, columnspan=2)

        self.frontPage = Tkinter.IntVar()
        frontPage = Tkinter.Checkbutton(frame, text="FP", variable=self.frontPage, command=self.toggleFrontPage)
        frontPage.grid(row=1, column=2, sticky=Tkinter.W)
        
        self.b1 = Tkinter.Button(frame, text="Download Images", command=self.startDownload)
        self.b1.grid(row=4, sticky=Tkinter.W, columnspan=2)

        self.b2 = Tkinter.Button(frame, text="Select", command=self.selectFolder)
        self.b2.grid(row=0, column=2)

        self.downloadAllVar = Tkinter.IntVar()
        downloadAllCheckbox = Tkinter.Checkbutton(frame, text="Download All", command=self.toggleDownloadAll, variable=self.downloadAllVar)
        downloadAllCheckbox.grid(row=0, column=3, columnspan=2)
        
        Tkinter.Label(frame, text="Num of Images: ").grid(row=1, column=3, sticky=Tkinter.E)
        spinnerDe = Tkinter.StringVar()
        spinnerDe.set("5000")
        self.imageNumSpinner = Tkinter.Spinbox(frame, textvariable=spinnerDe, width=4, from_=1, to=999999)
        self.imageNumSpinner.grid(row=1, column=4)   
        
        self.downloadText = Tkinter.StringVar()
        Tkinter.Label(frame, textvariable=self.downloadText).grid(row=4, column=2, columnspan=3, sticky=Tkinter.E)
        self.downloadText.set("Not Downloading...")
        
        frame.grid()

    def displayError(self, title, errorBody):
        tkMessageBox.showwarning(title, errorBody)

    def finsihedDownload(self):
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

    def downloadImages(self, search, limit, settings, done):
        self.scraper.downloadAllImagesFromSearch(search, limit, settings)
        done()

    def downloadMoniter(self):
        while True:
            if(self.scraper.isDownloading()):
                self.downloadText.set("Downloading Image: " + str(self.scraper.getDownloadNum()))
            else:
                self.downloadText.set("Not Downloading...")
        
    def startDownload(self):
        if self.scraper.isDownloading():
            self.displayError("Downloading", "You are allready downloading something")
        limit = int(self.imageNumSpinner.get())
        if self.downloadAllVar.get() == 1:
            limit = -1
        searchQ = self.searchEntry.get()
        settings = IS.settingObject()
        if self.frontPage.get() == 1:
            settings.setFP(True)
        if self.gifsOnly.get() == 1:
            settings.setGifsOnly(True)
        if self.albumIntoFolders.get() == 0:
            settings.setAlbumsInFolders(False)
        self.scraper.changeDownloadFolder(self.folderEntryVar.get())
        self.downloadThread = thread.start_new_thread(self.downloadImages, (searchQ, limit, settings, self.finsihedDownload))

    def selectFolder(self):
        directoryName = tkFileDialog.askdirectory()
        self.folderEntryVar.set(directoryName)
        
master = Tkinter.Tk();
interface = Interface(master)
thread.start_new_thread(interface.downloadMoniter, ())
master.wm_title("Meme Machine")
master.mainloop()

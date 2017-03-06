
import requests, re, shutil, os, time, thread

class scraperObject:
    def __init__(self):
        self.downloadFolder = None
        self.downloading = False
        self.downloadNum = 0
        self.galHashes =[]
        #gets a webpage
    def getPage(self, url):
        page = requests.get(url)
        page = page.content
        return page

    def getImageNameWhenJSONFails(self, galHash):
        page = self.getPage("http://imgur.com/gallery/" + galHash)
        index = page.index('itemprop="contentURL"')
        cur = index
        start = -1
        end = -1
        numberOfQuotes = 0
        while True:
            cur -= 1
            if page[cur] == '"':
                if numberOfQuotes < 2:
                    numberOfQuotes += 1
                else:
                    if start == -1:
                        start = cur
                    elif end == -1:
                        end = cur
                        break
        url = page[end + 15:start]
        if url != "thumbnailUrl":
            return url
        return None

    #a method that gets all the image names from a gallery hash in array format
    def getImagesNamesFromGalHash(self, galHash):
        reqJson = requests.get("http://imgur.com/ajaxalbums/getimages/" + galHash + "/hit.json")
        try:
            imageData = reqJson.json()["data"]["images"]
        except TypeError: #this will occur if the gif gallery only has one gif in it
            return [self.getImageNameWhenJSONFails(galHash)]
        except ValueError:
            print("****ERROR****")
            time.sleep(5)
            return self.getImagesNamesFromGalHash(galHash)
        names = []
        for x in imageData:
            names.append(x["hash"] + x["ext"])
        return names

    #replaces a * in a url with numbers from start to end and returns the array of them all
    def getScrollPageUrl(self, url, pageNum):
        index = url.index("*")
        newUrl = url[:index] + str(pageNum) + url[index + 1:]
        return newUrl

    #gets the gallary hashes from the scroll page
    def getGalHashesFromScrollPageUrl(self, url):
        page = self.getPage(url)
        pageCodes = []
        for x in re.finditer('class="image-list-link"', page):
            cur = x.end()
            start = -1
            end = -1
            while True:
                cur += 1
                if page[cur] == '"':
                    if start == -1:
                        start = cur
                    elif end == -1:
                        end = cur
                        break    
            pageCodes.append(page[start + 9 + 1:end])
        return pageCodes

    #A method that checks if the image is allready in the downloads folder
    #---------------------------------------------------------------------
    #TODO make this process more effeicent by storing a list of all
    #the file names so you dont have to list the entire dir each time you get an image
    def checkIfImageIsDownloaded(self, imageName, path=None):
        if path == None:
            path = self.downloadFolder
        items = os.listdir(path) #gets all the items inside the download folder
        if imageName in items:
            return True
        return False

    #A method that sets the folder that the images will be downloaded to
    def changeDownloadFolder(self, folderName):
        self.downloadFolder = folderName + "/"
        items = os.listdir(".")
        self.makeFolderIfNotThere(folderName)

    def makeFolderIfNotThere(self, folderName):
        if not os.path.exists(folderName):
            os.mkdir(folderName)

    #A method that downloads a single image from imgur given it's name (hash + extension)
    def downloadImage(self, name, path=None):
        if path == None:
            path = self.downloadFolder
        if name == None or name == "":
            return
        url = "http://i.imgur.com/" + name
        response = requests.get(url, stream=True)
        print("Name: " + name)
        with open(path + name, "wb") as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response

    def stopDownload(self):
        self.downloading = False

    def getGalHashes(self):
        return self.galHashes

    #gets the next hash but with threading taken into account
    def getGalHash(self, index):
        curHash = ""
        while True:
            try:
                curHash = self.getGalHashes()[index]
            except IndexError:
                pass
        return curHash

    # a method that downloads all images given a search querry
    def downloadAllImagesFromSearch(self, search, limit):
        self.downloading = True
        self.downloadNum = 0
        pageNum = 0
        searchUrl = "http://imgur.com/search/score/all/page/*?scrolled&q=" + search + "&q_size_is_mpx=off"
        currentHash = "first"
        while True:
            scrollPageUrl = self.getScrollPageUrl(searchUrl, pageNum)
            galHashes = self.getGalHashesFromScrollPageUrl(scrollPageUrl)
            if len(galHashes) == 0:
                break
            for galHash in galHashes:
                names = self.getImagesNamesFromGalHash(galHash)
                if len(names) > 1:
                    self.downloadAlbum(galHash, names, limit)
                else:
                    if not self.checkIfImageIsDownloaded(names[0]):
                        if self.downloading:
                            self.downloadNum += 1
                            self.downloadImage(names[0])
                        else:
                            print("done")
                            return
        self.downloading = False
        print("done")
        
        while currentHash != "<DONE>":
            if self.downloadNum > limit:
                self.downloading = False
                print("done")
                return
            currentHash = self.getGalHash(galNum)
            galNum += 1
            

    def downloadAlbum(self, name, imageHashes, limit):
        albumPath = self.downloadFolder + name + "/"
        self.makeFolderIfNotThere(albumPath)
        for x in imageHashes:
            if not self.checkIfImageIsDownloaded(x, path=albumPath):
                if self.downloading or self.downloadNum > limit:
                    self.downloadNum += 1
                    self.downloadImage(x, path=albumPath)
                else:
                    return

    def isDownloading(self):
        return self.downloading

    def getDownloadNum(self):
        return self.downloadNum

#changeDownloadFolder("defaultDownloadFolder")

#downloadAllImagesFromSearch("memes")

#print(getGalHashesFromScrollPageUrl("http://imgur.com/search/score/all/page/1?scrolled&q=dank%20memes&q_size_is_mpx=off"))

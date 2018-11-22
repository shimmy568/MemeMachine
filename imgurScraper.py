
import requests, re, shutil, os, time

class settingsObject:
    def __init__(self):
        self.downloadType = 0
        self.FP = False
        self.albumsInFolders = True

    def setDownloadType(self, val):
        self.downloadType = val
        
    def setFP(self, val):
        self.FP = val
        
    def setAlbumsInFolders(self, val):
        self.albumsInFolders = val

    def getDownloadType(self):
        return self.downloadType
    
    def getFP(self):
        return self.FP

    def getAlbumsInFolders(self):
        return self.albumsInFolders

class scraperObject:
    def __init__(self):
        self.downloadFolder = None
        self.downloading = False
        self.downloadNum = 0
        self.galHashes = []
        #gets a webpage
    def getPage(self, url):
        page = requests.get(url)
        page = page.content
        return page

    def getImageNameWhenJSONFails(self, galHash):
        page = self.getPage("http://imgur.com/gallery/" + galHash)
        try:
            index = page.index('itemprop="contentURL"')
        except:
            return None
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
    def downloadImage(self, name, downloadType, updateCallback, path=None):
        if path == None:
            path = self.downloadFolder
        if name == None or name == "":
            return

        if name[len(name) - 1] != "g" and name[len(name) - 1] != "f":
            name = name[:len(name) - 2]

        #filters out all images of the set type
        if downloadType == 1 and name[len(name) - 1] == "f":
            return
        elif downloadType == 2 and name[len(name) - 1] != "f":
            return

        #downloads the image
        self.downloadNum += 1
        updateCallback(self.downloading, self.downloadNum)
        url = "http://i.imgur.com/" + name
        response = requests.get(url, stream=True)
        
        with open(path + name, "wb") as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response

    #stop the downloading
    def stopDownload(self):
        self.downloading = False

    #a method that was used to divide a number into a whole number as equal as possible
    def divideIntoEqualParts(self, num, n):
        nums = []
        extra = num % n
        minimum = int(num / n)
        for x in range(n): #create the base array with the minimum value for all spots
            nums.append(minimum)

        for x in range(extra): #add the extra on to the numbers
            nums[x] += 1

        return nums

    #download all images from the search querry while keeping each search from the full search
    #(sepperated with ,) having an equal amount of images downloaded
    def downloadAllImagesFromSearch(self, search, totalLimit, settings, updateCallback):
        updateCallback(True, 0)
        tags = search.split(",")
        limits = self.divideIntoEqualParts(totalLimit, len(tags))
        for x in range(len(tags)):
            currentTag = tags[x].strip()
            try:
                self.downloadAllImagesFromTag(currentTag, limits[x], settings, updateCallback)
            except RuntimeError:
                print("Finishing downloads... (To exit now press CTRL+C)")
                return #program has stopped
            if not self.downloading:
                return
                
    # a method that downloads all images given a tag search thing
    def downloadAllImagesFromTag(self, search, limit, settings, updateCallback): #gifs only, folder album, front page
        self.downloading = True
        self.downloadNum = 0
        pageNum = 0
        setNum = 0
        searchUrl = "http://imgur.com/search/score/all/page/*?scrolled&q=" + search + "&q_size_is_mpx=off"
        if settings.getFP():
            searchUrl = "http://imgur.com/t/funny/viral/page/*/hit?scrolled&set="
        downloadType = settings.getDownloadType()
        currentHash = "first"
        while True:
            scrollPageUrl = None
            if settings.getFP(): #having a sepprate if path from the normal one for the front page bc of the set thing
                scrollPageUrl = self.getScrollPageUrl(searchUrl, pageNum) + str(setNum) 
                if setNum == 10:
                    setNum = 0
                    pageNum += 1
                else:
                    setNum += 1
            else:
                scrollPageUrl = self.getScrollPageUrl(searchUrl, pageNum)
                pageNum += 1 
            galHashes = self.getGalHashesFromScrollPageUrl(scrollPageUrl)
            if len(galHashes) == 0:
                break
            for galHash in galHashes:
                if not self.downloading or (self.downloadNum >= limit and limit != -1):
                    self.doneDownloading(updateCallback)
                    return
                names = self.getImagesNamesFromGalHash(galHash)
                if len(names) > 1 and settings.getAlbumsInFolders():
                    self.downloadAlbum(galHash, names, limit, downloadType, updateCallback)
                else:
                    for name in names:
                        if not self.checkIfImageIsDownloaded(name):
                            if self.downloading:
                                self.downloadImage(name, downloadType, updateCallback)
                            else:
                                self.doneDownloading(updateCallback)
                                return
        self.doneDownloading(updateCallback)          

    def doneDownloading(self, updateCallback):
        self.downloading = False
        updateCallback(False, 0)
        
    def downloadAlbum(self, name, imageHashes, limit, downloadType, updateCallback):
        albumPath = self.downloadFolder + name + "/"
        self.makeFolderIfNotThere(albumPath)
        for x in imageHashes:
            if not self.checkIfImageIsDownloaded(x, path=albumPath):
                if self.downloading and (self.downloadNum < limit or limit == -1):
                    self.downloadImage(x, downloadType, updateCallback, path=albumPath)
                else:
                    return

    def isDownloading(self):
        return self.downloading

    def getDownloadNum(self):
        return self.downloadNum



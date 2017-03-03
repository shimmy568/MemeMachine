import requests, json, re, shutil, os, time

downloadFolder = None
downloading = False

#gets a webpage
def getPage(url):
    page = requests.get(url)
    page = page.content
    return page

#a method that gets all the image names from a gallery hash in array format
def getImagesNamesFromGalHash(galHash):
    reqJson = requests.get("http://imgur.com/ajaxalbums/getimages/" + galHash + "/hit.json")
    try:
        imageData = reqJson.json()["data"]["images"]
    except TypeError: #this will occur if the gif gallery only has one gif in it
        return [galHash + ".gif"]
    except ValueError:
        print("****ERROR****")
        time.sleep(5)
        return getImagesNamesFromGalHash(galHash)
    names = []
    for x in imageData:
        names.append(x["hash"] + x["ext"])
    return names

#replaces a * in a url with numbers from start to end and returns the array of them all
def iterateUrl(url, start = 0, end = 300):
    index = url.index("*")
    urls = []
    for x in range(end - start):
        urls.append(url[:index] + str(x + start) + url[index + 1:])
    return urls

#gets the gallary hashes from the scroll page
def getGalHashesFromScrollPageUrl(url):
    page = getPage(url)
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
def checkIfImageIsDownloaded(imageName):
    global downloadFolder
    items = os.listdir(downloadFolder) #gets all the items inside the download folder
    if imageName in items:
        return True
    return False

#A method that sets the folder that the images will be downloaded to
def changeDownloadFolder(folderName):
    global downloadFolder
    downloadFolder = folderName + "/"
    items = os.listdir(".")
    if not os.path.exists(folderName):
        os.mkdir(folderName)

#A method that downloads a single image from imgur given it's name (hash + extension)
def downloadImage(name, fuckBandwidth = True):
    global downloadFolder
    url = "http://i.imgur.com/" + name
    response = requests.get(url, stream=fuckBandwidth)
    with open(downloadFolder + name, "wb") as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response

def stopDownload():
    downloading = False
    
# a method that downloads all images given a search querry
def downloadAllImagesFromSearch(search, slow, startp, endp):
    speedOpt = not slow
    downloading = False
    scrollUrls = iterateUrl("http://imgur.com/search/score/all/page/*?scrolled&q=" + search + "&q_size_is_mpx=off")
    for scrollUrl in scrollUrls:
        galHashes = getGalHashesFromScrollPageUrl(scrollUrl)
        for galHash in galHashes:
            names = getImagesNamesFromGalHash(galHash)
            for name in names:
                if not checkIfImageIsDownloaded(name):
                    if downloading:
                        downloadImage(name, fuckBandwidth=speedOpt)
                    else:
                        return
    downloading = False

def isDownloading():
    return downloading
    
#changeDownloadFolder("defaultDownloadFolder")

#downloadAllImagesFromSearch("memes")

#print(getGalHashesFromScrollPageUrl("http://imgur.com/search/score/all/page/1?scrolled&q=dank%20memes&q_size_is_mpx=off"))

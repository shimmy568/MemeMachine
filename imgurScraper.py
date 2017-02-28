import requests

changeDownloadFolder("defaultDownloadFolder")

#gets a webpage
def getPage(url):
    page = requests.get(url)
    page = page.content
    return page

#TODO code method that gets JSON file from the backend
def getImagesFromGalHash(hash):
    pass

#replaces a * in a url with numbers from start to end and returns the array of them all
def iterateUrl(url, start = 0, end = 300):
    index = url.index("*")
    urls = []
    for x in range(end - start):
        urls.append(url[:index] + str(x + start) + url[index + 1:])
    return urls

#gets the gallary hashes from the scroll page
def getGalHashesFromScrollPage(page):
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
	    pageCodes.append(page[start + 1:end])
    return pageCodes

#TODO make method that checks if a image is allready downloaded
def checkIfImageIsDownloaded(imageName):
    pass

#TODO change the folder that the images download to
def changeDownloadFolder(folderName):
    pass

#TODO make method that downloads the image to the folder
def downloadImage(url):
    pass

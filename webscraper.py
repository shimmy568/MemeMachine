from lxml import html
import requests, re, shutil, DatabaseManager, os.path, sys

#this function returns the tree of a webpage
def getWeb(url):
	page = requests.get(url)
	page = page.content

	return page

#the * will be replaced with numbers from 0 to max
#returns with a list of all the urls
def iterateUrl(url, max = 300):
	index = url.index("*")
	urls = []
	for x in range(max):
		urls.append(url[:index] + str(x) + url[index + 1:])
	return urls

#this function returns an array that contains the tree for a selection of pages
#urlBase is the base url with all variable contents replaced by *
#for each element in vars it is to replace the next *
def getPages(urlBase, vars, M):
	pages = []
	splitUrl = urlBase.split("*")
	i = 0
	for x in range(M):
		newUrl = ''
		for y in splitUrl:
			newUrl.append(y)
			newUrl.append(vars[i])
			i += 1
		tree = getWeb(newUrl)
		pages.append(tree)
	return pages

def imgurGetPostsFromPostsPage(page):
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

def imgurGetImageUrlFromIndex(index, page):
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
	url = page[end + 1:start]
	if url != "thumbnailUrl":
		return "https:" + url
	return None

#url is string, host is string, code is string
def downloadImageFromUrl(url, path):
	response = requests.get(url, stream=True)
	with open(path, 'wb') as out_file:
		shutil.copyfileobj(response.raw, out_file)
	del response

#this method only works for data infront of the index provided and must be surrounded by ""
def imgurGetPostInfoFromIndex(index, page):
	cur = index
	start = -1
	end = -1
	numberOfQuotes = 0
	while True:
		cur += 1
		if page[cur] == '"':
			if start == -1:
				start = cur
			elif end == -1:
				end = cur
				break
	if page[start + 1:end] != "is_hot":
		return page[start + 1:end]
	return -1

def imgurGetNumberDataFromIndex(index, page):
	start = index
	end = index
	while True:
		if page[end] == ",":
			break
		end += 1
	return int(page[start:end])

def loadImgurImageImageObjectsFromPageCodes(pageCodes):
	urls = []
	dates = []
	views = []
	points = []
	commentCounts = []
	i = 0
	for x in pageCodes:
		urls.append([])
		page = getWeb("http://imgur.com" + x)
		#get the all the image urls from a page
		for x in re.finditer('itemprop="contentURL"', page):
			urls[i].append(imgurGetImageUrlFromIndex(x.start(), page))
		i += 1
	imageObjects = []
	for i in range(len(urls)):
		for o in urls[i]:
			if(o != None):
				#name = o[20:]
				#path = os.path.join("images", "imgur-" + name)
				imageObjects.append(DatabaseManager.imageData(o, "imgur", dates[i], views = views[i], commentCount = commentCounts[i], pointCount = points[i]))
				#downloadImageFromUrl(o, path)
	return imageObjects

tags = ["me_irl", "dank memes", "memes", "meme", "meirl", "me irl", "dankmemes"]

if __name__ == "__main__":
	for y in tags:
		urls = iterateUrl('http://imgur.com/search/score/all/page/*?scrolled&q='+ y +'&q_size_is_mpx=off')
		for x in urls:
			print(urls.index(x))
			page = getWeb(x)
			a = imgurGetPostsFromPostsPage(page)
			a = loadImgurImageImageObjectsFromPageCodes(a)

			DatabaseManager.addImagesToDatabase(a, y)


#iterateUrl('http://imgur.com/search/score/all/page/*?scrolled&q=memes&q_size_is_mpx=off')

#page = getWeb("http://imgur.com/search/score/all/page/2?scrolled&q=memes&q_size_is_mpx=off")
#links = imgurGetPostsFromPostsPage(page)

#print links
#print(page.index("class=\"post\""))

		


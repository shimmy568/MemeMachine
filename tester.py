import requests

def getWeb(url):
    page = requests.get(url)
    page = page.content
    return page

print(getWeb("http://imgur.com/gallery/6Nz1a"))

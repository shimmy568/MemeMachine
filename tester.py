import requests

def getWeb(url):
    page = requests.get(url)
    page = page.content
    return page

print(getWeb("http://imgur.com/ajaxalbums/getimages/foTJK/hit.json"))

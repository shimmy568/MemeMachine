import requests

def getWeb(url):
    page = requests.get(url)
    page = page.content
    return page

print(getWeb("http://imgur.com/search/score/all/page/1?scrolled&q=dank%20memes&q_size_is_mpx=off"))

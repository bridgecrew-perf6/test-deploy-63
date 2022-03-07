from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

class Content:
    def __init__(self, url, title, body):
        self.url = url
        self.title = title
        self.body = body

def getPage(url):
    req = requests.get(url)
    return BeautifulSoup(req.text, 'html.parser')

def scrapeBrookings(url):
    bs = getPage(url)
    title = bs.find("h1").text
    body = bs.find("div",{"class","post-body"}).text
    return Content(url, title, body)
url = 'https://www.brookings.edu/blog/future-development/2018/01/26/delivering-inclusive-urban-access-3-uncomfortable-truths/'
content = scrapeBrookings(url)
# print('Title: {}'.format(content.title))
# print('URL: {}\n'.format(content.url))
# print(content.body)

@app.route('/')
def index():
    return render_template("index.html",title=content.title, body=content.body, url=content.url)

@app.route('/api')
def api():
    r = requests.get('https://opentdb.com/api.php?amount=20')
    return r.json()


if __name__ == '__main__':
    app.debug = True
    app.run()
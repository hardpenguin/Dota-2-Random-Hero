# pip
import requests

class WebDocument(object):
    def __init__(self, link):
        self.link = link
        self.contents = None

    def _download(self):
        response = requests.get(self.link)
        html = response.text
        self.contents = html

    def get_contents(self):
        self._download()
        return(self.contents)
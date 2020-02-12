import bs4 as bs
import urllib.request
import sys
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
import pytube


class Page(QWebEnginePage):
    def __init__(self, url):
        self.app = QWebEnginePage(sys.argv)
        QWebEnginePage.__init__(self)
        self.html = ''
        self.loadFinished.connect(self._on_load_finished)
        self.load(QUrl(url))
        self.app.exec_()

    def _on_load_finished(self):
        self.html = self.toHtml(self.Callable)
        print('load Finished')

    def Callable(self, html_str):
        self.html = self.html_str
        self.app.quit()


links = []


def exact_link(link):
    vid_id = link.split('=')
    str = ""
    for i in vid_id[0:2]:
        str += i + "="

    str_new = str[0:len(str) - 1]
    index = str_new.find("&")

    new_link = "https://www.youtube.com" + str_new[0:index]
    return new_link

url = input("past valid playlist Link")
print(url)

page = Page(url)
count = 0

soup = bs.BeautifulSoup(page.html, 'html.parser')
for link in soup.find_all('a', id='thumbnail'):
    if count == 0:
        count += 1
        continue
    else:
        vid_src = link['href']
        new_link = exact_link(vid_src)
        links.append(new_link)

for link in links:
    yt = pytube.YouTube(link)

    stream = yt.streams.filter(progressive=True,
                               file_extension='mp4').order_by(
        'resolution').desc().first()
    try:
        stream.download()
        # printing the links downloaded
        print("Downloaded: ", link)
    except:
        print('Some error in downloading: ', link)
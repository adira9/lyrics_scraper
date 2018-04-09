import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import os
import http

def get_songs(artist):
    artist=artist.lower().replace(" ","_")
    song_url="http://www.songfacts.com/artist-"+artist+".php"
    try:
        url_getter=urlopen(song_url)
        page_source=url_getter.read()
        url_getter.close()
    except urllib.error.HTTPError:
        print("Incorrect download link")
        os.exit(1)
    soup_reader=soup(page_source,"html.parser")
    songs=soup_reader.select("div.wrapper > ul.songullist-orange > li > a[href]")

    song_names=[]
    for song in songs:
        song_names.append(soup.get_text(song))
    #print(song_names)
    return song_names


def download_lyrics(artist,song_name):
    title=song_name
    artist=artist.lower().replace(" ","")
    song_name2=song_name.lower().replace(" ","_")
    song_name=song_name.lower().replace(" ","")
    my_url="https://www.azlyrics.com/lyrics/"

    try:
        my_url=my_url+artist+"/"+song_name+".html"
        url_getter=urlopen(my_url)
        page_source=url_getter.read()
        url_getter.close()
        soup_reader=soup(page_source,"html.parser")
        title=soup.get_text(soup_reader.h1)
        print("Downloading: ",title)
        unnamed_divs=soup_reader.findAll("div",{"class":None})
        stripped=soup.get_text(unnamed_divs[1])
        lyric_file=open((song_name2+".txt"),"w")
        lyric_file.write(stripped)
        lyric_file.close()

    except urllib.error.HTTPError:
        print("Failed to download:", title)
    except http.client.RemoteDisconnected:
        print("Failed to download:", title)


def main():
    artist=input("Artist: ")
    newpath = os.path.join(os.environ["HOMEPATH"], "Desktop")+"\\"+artist
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    os.chdir(newpath)
    for song in get_songs(artist):
        download_lyrics(artist,song)

if __name__ == "__main__":
    main()

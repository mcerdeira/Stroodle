import sys
import os
import traceback
from urllib.request import urlopen
from urllib import robotparser
from bs4 import BeautifulSoup
from multiprocessing import Process
import db_actions
from multiprocessing import Process

movie_url_format = "https://www.imdb.com/title/tt%s"
os_url_format = "https://www.imdb.com/title/tt%s/soundtrack"
already_fetched = []
index = 1
PROCESSES = 25
process_list = []

def start_crawl():
    global index
    global PROCESSES
    global process_list
    intial_url_load()
    while(True):
        process_list = []
        for i in range(PROCESSES):
            process_list.append(Process(target=crawl, args=(index, str(index).zfill(7),)))
            process_list[i].start()
            index += 1
        
        for i in range(PROCESSES):
            process_list[i].join()            


def intial_url_load():
    global index
    rows = db_actions.get_intial_url_load()
    for r in rows:
        if r[0] == None:
            index = 1 #120338
        else:
            index = int(r[0]) + 1


def crawl(index, str_index):    
    urlm = (movie_url_format % str_index)
    urlo = (os_url_format % str_index)
    url = (urlo, urlm)

    try:
        print(url[1])
        html_m = urlopen(url[1]) # Try to get movie info
        html_o = urlopen(url[0]) # If pass, now go for the soundtrack
        dump(index, str_index, url, html_m, html_o)

    except Exception as e:
        write_log(url[1] + ": " + str(e) + " " + repr(e) +
                        " " + traceback.format_exc() + "\n\n")

        print("ERROR: " + str(e))
        print(repr(e))
        traceback.print_exc()


def dump(index, str_index, url, content_m, content_o): 
    try:	
        soup_m = BeautifulSoup(content_m, 'html.parser')
        soup_o = BeautifulSoup(content_o, 'html.parser')

        if(soup_m.title):
            title = soup_m.title.text
        else:
            title = ""

        description = soup_m.find("meta",  property="og:description")
        desc = ""
        if description["content"]:
            desc = description["content"]

        tracks = soup_o.find_all("div", {"id":"soundtracks_content"})    

        db_actions.insert_movie((str_index, url[1], title, desc, ))        
        if len(tracks) == 0:
            print("NO SONGS FOR " + str_index)
            db_actions.insert_song((str_index, "NO SONGS ON IMDB"))
        else:
            tracks_l = tracks[0].find_all("div", {"class": "list" })[0]            
            tracks_snd = tracks_l.find_all("div", {"class": "soundTrack soda odd"})                    
            if len(tracks_snd) > 0:
                for tr in tracks_snd:
                    song = tr.text
                    print(song)
                    db_actions.insert_song((str_index, song))
            else:
                print("NO SONGS FOR " + str_index)
                db_actions.insert_song((str_index, "NO SONGS ON IMDB"))
        
    except Exception as e:
        write_log(url[1] + ": " + str(e) + " " + repr(e) +
                       " " + traceback.format_exc() + "\n\n")
        
        print("ERROR: " + str(e))
        print(repr(e))
        traceback.print_exc()

def write_log(log):
    LOG_FILE = open("log.txt", "w+")
    LOG_FILE.write(log)
    LOG_FILE.write("---------------------------------------------")
    LOG_FILE.close()

if __name__ == '__main__':
    try:
        sys.setrecursionlimit(1000000000)        
        start_crawl()        
        db_actions.close_all()
    except KeyboardInterrupt:
        print('Interrupted!!!!!!!!!!!')
        print('Closing processes...')
        for i in range(PROCESSES):
            process_list[i].join()
        
        print('All process closed')
        db_actions.close_all()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

import sys
import os
import traceback
from urllib.request import urlopen
from urllib import robotparser
from bs4 import BeautifulSoup
from multiprocessing import Process
import db_actions
from multiprocessing import Process, Manager
import xml.etree.ElementTree as ET
root = ET.parse('data/albums-1.xml').getroot()

index = 1
PROCESSES = 200
process_list = []
urls_list = []

def test_method(SQL_INSERTS):
    # TESTS
    #15 songs
    crawl(0, SQL_INSERTS, 'https://www.soundtrack.net/album/godzilla-soundtrack/')
    #14 songs
    crawl(0, SQL_INSERTS, 'https://www.soundtrack.net/album/james-horner-the-classics/') 
    #15 songs
    crawl(0, SQL_INSERTS, 'https://www.soundtrack.net/album/titanic')
    #10 songs
    crawl(0, SQL_INSERTS, 'https://www.soundtrack.net/album/blown-away/')
    db_actions.exec_inserts(SQL_INSERTS)
    db_actions.clean_up()

def start_crawl():
    global index
    global PROCESSES
    global process_list
    manager = Manager()

    SQL_INSERTS = manager.list()
    intial_url_load()
    
    #test_method(SQL_INSERTS)

    for child in root:
        urls_list.append(child[0].text)

    index = 0
    stop = False

    while(True):
        if stop:
            break

        process_list = []
        for i in range(PROCESSES - 1):
            process_list.append(Process(target=crawl, args=(0, SQL_INSERTS, urls_list[index],)))
            process_list[i].start()            
            if index + 1 > len(urls_list) - 1:
                stop = True
                break
            else:
                index += 1
        
        for i in range(len(process_list)):
            process_list[i].join() 
        
        print("BATCH ENDED: " + str(index + 1) + " of " + str(len(urls_list)) + " " + str(round((index + 1)* 100 / (len(urls_list)), 2)) + "%")
        db_actions.exec_inserts(SQL_INSERTS)
        db_actions.clean_up()
        SQL_INSERTS = manager.list()

def debug_print(what):
    pass
    #print(what)

def intial_url_load():
    pass
"""     global index
    rows = db_actions.get_intial_url_load()
    for r in rows:
        if r[0] == None:
            index = 1 #120338
        else:
            index = int(r[0]) + 1 """


def crawl(index, SQL_INSERTS, _url):        
    url = _url

    try:
        debug_print(url)
        html_o = urlopen(url) # If pass, now go for the soundtrack
        dump(index, SQL_INSERTS, url, html_o)

    except Exception as e:
        write_log("[URL] " + url + "\n " + str(e) + " " + repr(e) +
                        " " + traceback.format_exc() + "\n\n")

        debug_print("ERROR: " + str(e))
        debug_print(repr(e))        
        traceback.print_exc()
        print("############## - " + url + " - ##############")

def reduce_title(titles):
    full_title = ""
    for t in titles:
        if(t and t != "Music From"):
            full_title += t + "|"
    
    return full_title[:-1]

def dump(index, SQL_INSERTS, url, content_o): 
    try:	
        soup_o = BeautifulSoup(content_o, 'html.parser')

        if(soup_o.title):
            desc = soup_o.title.text
        else:
            desc = ""
        
        #title = reduce_title(soup_o.find_all("li", {"class":"list-group-item"}))
        title = reduce_title(soup_o.find_all("div", {"class":"card card--success"})[0].text.split('\n'))
        tracks = soup_o.find_all("table", {"class":"cbox_table"})    

        SQL_INSERTS.append(db_actions.insert_movie((url, url, title, desc, )))

        if len(tracks) > 0:
            songs = tracks[0].text.split('\n')
            #for song in list(tracks[0].next_elements):        
            #    if hasattr(song, "text"):
            #        songs = song.text.split('\n')
            #        break

            skip = 3 #2

            for e in range(0, len(songs)):
                try:
                    if skip == 0:
                        skip = 5
                        song_text = songs[e]                    
                        SQL_INSERTS.append(db_actions.insert_song((url, song_text)))
                    
                    skip -= 1 

                except Exception as e:
                    pass

    except Exception as e:
        write_log(url[1] + ": " + str(e) + " " + repr(e) +
                       " " + traceback.format_exc() + "\n\n")
        
        debug_print("ERROR: " + str(e))
        debug_print(repr(e))
        traceback.print_exc()

def write_log(log):
    LOG_FILE = open("log.txt", "a+")
    LOG_FILE.write(log)
    LOG_FILE.write("--------------------------------------------- \n")
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

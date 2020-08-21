import requests
import pandas as pd
from bs4 import BeautifulSoup
import os 
import sys , subprocess
import json
from torrent import Movie

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class web_controller():
    session = requests.Session()
    
    def get_table_movies(self, movie_to_search):
        movies = list()
        search_movie_url = "https://www.1337x.to/category-search/"+movie_to_search+"/Movies/1/"
        page_search = requests.get(search_movie_url)
        soup_search = BeautifulSoup(page_search.content, 'html.parser')
        
        try:
            name_column = soup_search.find_all('td', class_ = 'name')
            seeds_column = soup_search.find_all('td', class_ = 'seeds')
            leechs_column = soup_search.find_all('td', class_ = 'leeches')
            size_column = soup_search.find_all('td', class_ = 'size')
            #links_column = soup_search.find_all('a')
        except:
            print(bcolors.WARNING+"Table cells not founded"+bcolors.ENDC)
            

        links_list = list()
        names_list = list()
        seeds_list = list()
        leechs_list = list()
        sizes_list = list()


        for n in name_column:
            names_list.append(n.text)
        for s in seeds_column:
            seeds_list.append(s.text)
        for l in leechs_column:
            leechs_list.append(l.text)
        for z in size_column:
            sizes_list.append(z.text)
        for a in name_column:
            for k in a.find_all('a'):
                if '/torrent' in k.get('href'):
                    links_list.append(k.get('href'))


        movies_count = len(names_list)
        for x in range(movies_count):
            insert_movie = Movie(names_list[x], "https://www.1337x.to"+links_list[x], seeds_list[x], sizes_list[x])
            movies.append(insert_movie)
       
        
        return movies


"""
    def post_login(self,username, password):
        link_login = "http://192.168.1.6:8080/api/v2/auth/login"
        data_login = {'username': username, 'password': password}
        
        post_login = self.session.post(link_login, data=data_login)
        print(bcolors.UNDERLINE+"LOGIN_POST: "+bcolors.ENDC+post_login.text)
        #print(bcolors.UNDERLINE+"LOGIN_POST WITHOUT PARSE: "+bcolors.ENDC+str(login_post))

    def get_default_save_path(self):
        link_default_save_path = "http://192.168.1.6:8080/api/v2/app/defaultSavePath"
        get_default_save_path = self.session.get(link_default_save_path)
        default_save_path = str(get_default_save_path.text)
        return default_save_path
    
    def post_add_torrent(self,movie):
        qbit_add_torrent = "http://192.168.1.6:8080/api/v2/torrents/add"
        data_add_torrent = {'urls': movie.link, 'rename': movie.name}

        post_add_torrent = self.session.post(qbit_add_torrent,data= data_add_torrent)
        print(bcolors.UNDERLINE+"ADD_POST: "+bcolors.ENDC+post_add_torrent.text)
        #print(bcolors.UNDERLINE+"ADD_POST WITHOUT PARSE: "+bcolors.ENDC+str(add_post))
   """


    

    

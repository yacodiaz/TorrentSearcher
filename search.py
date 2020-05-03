from bs4 import BeautifulSoup
import requests
import pandas as pd
import os 
import sys , subprocess

os.system("cls")

def open_magnet(magnet):
    """Open magnet according to os."""
    if sys.platform.startswith('linux'):
        subprocess.Popen(['xdg-open', magnet],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    elif sys.platform.startswith('win32'):
        os.startfile(magnet)
    elif sys.platform.startswith('cygwin'):
        os.startfile(magnet)
    elif sys.platform.startswith('darwin'):
        subprocess.Popen(['open', magnet],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        subprocess.Popen(['xdg-open', magnet],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


print(bcolors.WARNING + "This is an alpha version of a torrent-searcher thats why it sucks"+ bcolors.ENDC)


movie_input = input(bcolors.HEADER+"What movie do you want to look for: "+bcolors.ENDC)
url_search = "https://www.1337x.to/category-search/"+movie_input+"/Movies/1/"
#print("URL: "+url)


#Doing GET i think
page_search = requests.get(url_search)

 #Parsing the html file
soup_search = BeautifulSoup(page_search.content, 'html.parser')

#Get the rows of a table
rows_search = soup_search.find_all('tr')

#Get the columns(cells) that im interested
for row in rows_search:
    name_column = soup_search.find_all('td', class_ = 'name')
    seeds_column = soup_search.find_all('td', class_ = 'seeds')
    leechs_column = soup_search.find_all('td', class_ = 'leeches')
    size_column = soup_search.find_all('td', class_ = 'size')

link_file = list()
name_file = list()
seeds_file = list()
leechs_file = list()
size_file = list()

#Parsing only the text of the tag
for n in name_column:
    name_file.append(n.text)
for s in seeds_column:
    seeds_file.append(s.text)
for l in leechs_column:
    leechs_file.append(l.text)
for z in size_column:
    size_file.append(z.text)
for a in name_column:
    for k in a.find_all('a'):
        if '/torrent' in k.get('href'):
            link_file.append(k.get('href'))

#Main table with data
table_files = pd.DataFrame({'Movie: ': name_file, '/t Movie seeds: ' : seeds_file, 'Movie Size: ' : size_file})
print(table_files.iloc[0:10])

selection = input("select a movie by index: ")

#Select row in table
row_selected = table_files.iloc[ int(selection) , 0 ]
link_selected_torrent = link_file[int(selection)]
name_selected = name_file[int(selection)]

link_selected = "https://www.1337x.to"+link_selected_torrent

print(bcolors.OKGREEN+"You selected this movie: "+bcolors.ENDC,name_selected)
#print("Link selected:",link_selected)



#Inside the torrent
torrent_page = requests.get(link_selected)
torrent_soup = BeautifulSoup(torrent_page.content, 'html.parser')

downladButton = torrent_soup.findAll("a")

magnet_link_list = list()
for a in downladButton:
    if 'magnet:' in a.get('href'):
            magnet_link_list.append(a.get('href'))
magnet_link = magnet_link_list[0]
#print("Link download: ",magnet_link)
#open_magnet(magnet_link)

##Qbitorrent
##Session
session = requests.Session()

qbit_login = "http://192.168.1.6:8080/api/v2/auth/login"
qbit_add_torrent = "http://192.168.1.6:8080/api/v2/torrents/add"
data_login = {'username': 'admin', 'password': 'adminadmin'}
data_add_torrent = {'urls': magnet_link}

login_post = session.post(qbit_login, data=data_login)
add_post = session.post(qbit_add_torrent,data= data_add_torrent)
#login
print(bcolors.UNDERLINE+"LOGIN_POST: "+bcolors.ENDC+login_post.text)
#print(bcolors.UNDERLINE+"LOGIN_POST WITHOUT PARSE: "+bcolors.ENDC+str(login_post))
#add torrent
print(bcolors.UNDERLINE+"ADD_POST: "+bcolors.ENDC+add_post.text)
#print(bcolors.UNDERLINE+"ADD_POST WITHOUT PARSE: "+bcolors.ENDC+str(add_post))

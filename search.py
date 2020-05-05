from bs4 import BeautifulSoup
import requests
import pandas as pd
import os 
import sys , subprocess
import json
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
try:
    rows_search = soup_search.find_all('tr')
except:
    print(bcolors.WARNING+"Table row not founded"+bcolors.ENDC)
#Get the columns(cells) that im interested
for row in rows_search:
    try:
        name_column = soup_search.find_all('td', class_ = 'name')
        seeds_column = soup_search.find_all('td', class_ = 'seeds')
        leechs_column = soup_search.find_all('td', class_ = 'leeches')
        size_column = soup_search.find_all('td', class_ = 'size')
    except:
        print(bcolors.WARNING+"Table cells not founded"+bcolors.ENDC)

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

selection = input("Select a movie by index: ")
selection_parsed = int(selection)
selection_parsed = int(selection)
flag = True

while flag:
    if selection_parsed >9 or selection_parsed < 0:
        selection= input(bcolors.WARNING+"There is no movie with index higher than 9 or lower than 0. Please select a movie again: "+bcolors.ENDC)
        selection_parsed = int(selection)
    else:
        flag = False

#Select row in table
row_selected = table_files.iloc[ int(selection_parsed) , 0 ]
link_selected_torrent = link_file[int(selection_parsed)]
name_selected = name_file[int(selection_parsed)]

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
qbit_defaultSavePath = "http://192.168.1.6:8080/api/v2/app/defaultSavePath"
qbit_get_torrentlist = "http://192.168.1.6:8080/api/v2/torrents/info"
qbit_rename_torrent = "http://192.168.1.6:8080/api/v2/torrents/remame"

data_get_torrentlist = {'hashes'}
data_login = {'username': 'admin', 'password': 'adminadmin'}
data_add_torrent = {'urls': magnet_link, 'rename': name_selected}
##LOGIN
try:
    login_post = session.post(qbit_login, data=data_login)
    #login
    print(bcolors.UNDERLINE+"LOGIN_POST: "+bcolors.ENDC+login_post.text)
    #print(bcolors.UNDERLINE+"LOGIN_POST WITHOUT PARSE: "+bcolors.ENDC+str(login_post))
except:
    print(bcolors.FAIL+"ERROR: While login"+bcolors.ENDC)
##GET DEFAULT SAVE PATH
try:
    defaultSavePath_get = session.get(qbit_defaultSavePath)
    defaultSavePath = str(defaultSavePath_get.text)
    #print("default save path: "+defaultSavePath)
except:
    print(bcolors.FAIL+"ERROR: While getting default save path"+bcolors.ENDC)
#ADD TORRENT BY MAGNET
try:
    add_post = session.post(qbit_add_torrent,data= data_add_torrent)
    #add torrent
    print(bcolors.UNDERLINE+"ADD_POST: "+bcolors.ENDC+add_post.text)
    #print(bcolors.UNDERLINE+"ADD_POST WITHOUT PARSE: "+bcolors.ENDC+str(add_post))
except:
    print(bcolors.FAIL+"ERROR: While adding torrent"+bcolors.ENDC)
#try:
torrent_list_get = session.get(qbit_get_torrentlist)
torrent_list = json.loads(torrent_list_get.text)
json_hash = torrent_list[0]['hash']
print("TORRENT LIST:"+ json_hash)
#except:
   # print(bcolors.WARNING+"ERROR WHILE GETTING LIST TORRENTS"+bcolors.ENDC)
data_rename_torrent = {'hash': json_hash,'name': name_selected}

rename_post = session.post(qbit_rename_torrent, data = data_rename_torrent)
print("Rename post response: "+rename_post.text)


try:
    movie_url = defaultSavePath+name_selected
    print("movie url: "+movie_url)
    open(movie_url)
except:
     print(bcolors.WARNING+"ERROR: While opening movie"+bcolors.ENDC)


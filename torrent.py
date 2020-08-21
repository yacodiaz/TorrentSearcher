class Torrent():
    def __init__(self,name, link, seeds, size):
        self.name = name
        self.link = link
        self.seeds = seeds
        self.size = size
    
class Movie(Torrent):
    def getSubtitles(self):    
        print("sub")